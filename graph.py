"""
graph.py — LangGraph StateGraph assembly for the AWS Cloud Assistant
Initialises ChromaDB knowledge base and compiles the full agent graph.
"""
import os
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
import chromadb
from sentence_transformers import SentenceTransformer

from app.state import CapstoneState
from app.knowledge_base import DOCUMENTS
from app.nodes import (
    memory_node, router_node, retrieval_node, skip_retrieval_node,
    tool_node, answer_node, eval_node, save_node,
    FAITHFULNESS_THRESHOLD, MAX_EVAL_RETRIES
)

# ── Embedder and ChromaDB (module-level, initialised once) ──
print("Loading embedding model (all-MiniLM-L6-v2)...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

chroma_client = chromadb.Client()
try:
    chroma_client.delete_collection("aws_kb")
except Exception:
    pass
collection = chroma_client.create_collection("aws_kb")

texts      = [d["text"] for d in DOCUMENTS]
ids        = [d["id"]   for d in DOCUMENTS]
embeddings = embedder.encode(texts).tolist()

collection.add(
    documents=texts,
    embeddings=embeddings,
    ids=ids,
    metadatas=[{"topic": d["topic"]} for d in DOCUMENTS]
)
print(f"✅ Knowledge base ready: {collection.count()} documents")
for d in DOCUMENTS:
    print(f"   • {d['topic']}")


# ── Routing functions ─────────────────────────────────────

def route_decision(state: CapstoneState) -> str:
    """After router_node: decide which retrieval path to take."""
    route = state.get("route", "retrieve")
    if route == "tool":        return "tool"
    if route == "memory_only": return "skip"
    return "retrieve"


def eval_decision(state: CapstoneState) -> str:
    """After eval_node: retry answer if below threshold, otherwise save."""
    score   = state.get("faithfulness", 1.0)
    retries = state.get("eval_retries", 0)
    if score >= FAITHFULNESS_THRESHOLD or retries >= MAX_EVAL_RETRIES:
        return "save"
    return "answer"   # retry


# ── Build and compile the graph ───────────────────────────

def build_graph():
    graph = StateGraph(CapstoneState)

    # Add all 8 nodes
    graph.add_node("memory",    memory_node)
    graph.add_node("router",    router_node)
    graph.add_node("retrieve",  retrieval_node)
    graph.add_node("skip",      skip_retrieval_node)
    graph.add_node("tool",      tool_node)
    graph.add_node("answer",    answer_node)
    graph.add_node("eval",      eval_node)
    graph.add_node("save",      save_node)

    # Entry point
    graph.set_entry_point("memory")

    # Fixed edges
    graph.add_edge("memory", "router")

    # Conditional: router → retrieve / skip / tool
    graph.add_conditional_edges(
        "router", route_decision,
        {"retrieve": "retrieve", "skip": "skip", "tool": "tool"}
    )

    # All paths converge at answer
    graph.add_edge("retrieve", "answer")
    graph.add_edge("skip",     "answer")
    graph.add_edge("tool",     "answer")

    # Eval gate: retry or save
    graph.add_edge("answer", "eval")
    graph.add_conditional_edges(
        "eval", eval_decision,
        {"answer": "answer", "save": "save"}
    )

    graph.add_edge("save", END)

    checkpointer = MemorySaver()
    app = graph.compile(checkpointer=checkpointer)
    print("✅ Graph compiled successfully!")
    return app


# Compile once at import time
app = build_graph()
