"""
nodes.py — All LangGraph node functions for the AWS Cloud Assistant
Each node is independently testable and writes only to its own State fields.
"""
import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from app.state import CapstoneState
from app.tools import get_current_datetime, calculator

# ── LLM ──────────────────────────────────────────────────
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# ── Faithfulness settings ─────────────────────────────────
FAITHFULNESS_THRESHOLD = 0.7
MAX_EVAL_RETRIES       = 2


# ── Node 1: Memory ───────────────────────────────────────
def memory_node(state: CapstoneState) -> dict:
    """
    Appends user question to conversation history and applies sliding window.
    Also extracts user name if 'my name is' is in the question.
    """
    msgs = list(state.get("messages", []))
    msgs = msgs + [{"role": "user", "content": state["question"]}]

    # Sliding window — keep last 6 messages (3 turns)
    if len(msgs) > 6:
        msgs = msgs[-6:]

    # Extract user name if mentioned
    user_name = state.get("user_name", "")
    q_lower = state["question"].lower()
    if "my name is" in q_lower:
        parts = q_lower.split("my name is")
        if len(parts) > 1:
            name_candidate = parts[1].strip().split()[0].capitalize()
            user_name = name_candidate

    return {"messages": msgs, "user_name": user_name}


# ── Node 2: Router ────────────────────────────────────────
def router_node(state: CapstoneState) -> dict:
    """
    Routes the question to: retrieve, memory_only, or tool.
    Uses LLM to decide based on question content.
    """
    question = state["question"]
    messages = state.get("messages", [])
    recent   = "; ".join(
        f"{m['role']}: {m['content'][:60]}" for m in messages[-3:-1]
    ) or "none"

    prompt = f"""You are a router for an AWS Cloud Services chatbot.

Available routes:
- retrieve: search the AWS knowledge base (for questions about AWS services, features, pricing, storage, compute, databases, networking, migration, developer tools, management)
- memory_only: answer from conversation history only (e.g. "what did you just say?", "repeat that", "what was my first question?")
- tool: use a tool — datetime tool for current date/time questions, calculator for math/arithmetic

Recent conversation: {recent}
Current question: {question}

Reply with ONLY one word: retrieve / memory_only / tool"""

    response = llm.invoke(prompt)
    decision = response.content.strip().lower()

    if "memory" in decision:
        decision = "memory_only"
    elif "tool" in decision:
        decision = "tool"
    else:
        decision = "retrieve"

    return {"route": decision}


# ── Node 3: Retrieval ─────────────────────────────────────
def retrieval_node(state: CapstoneState) -> dict:
    """
    Queries ChromaDB for relevant chunks using semantic similarity.
    Returns top 3 chunks with topic labels.
    """
    # Import here so the graph module controls initialisation
    from app.graph import embedder, collection

    q_emb   = embedder.encode([state["question"]]).tolist()
    results = collection.query(query_embeddings=q_emb, n_results=3)
    chunks  = results["documents"][0]
    topics  = [m["topic"] for m in results["metadatas"][0]]

    context = "\n\n---\n\n".join(
        f"[{topics[i]}]\n{chunks[i]}" for i in range(len(chunks))
    )

    return {"retrieved": context, "sources": topics}


# ── Node 4: Skip Retrieval ───────────────────────────────
def skip_retrieval_node(state: CapstoneState) -> dict:
    """Returns empty context for memory-only queries."""
    return {"retrieved": "", "sources": []}


# ── Node 5: Tool ──────────────────────────────────────────
def tool_node(state: CapstoneState) -> dict:
    """
    Handles datetime and calculator tool calls.
    Never raises exceptions — always returns strings.
    """
    question = state["question"].lower()

    if any(word in question for word in ["time", "date", "today", "now", "day", "month", "year"]):
        tool_result = get_current_datetime()
    else:
        # Attempt to extract and evaluate arithmetic expression
        import re
        expr_match = re.search(r"[\d\s\+\-\*\/\(\)\.]+", state["question"])
        if expr_match:
            tool_result = calculator(expr_match.group().strip())
        else:
            tool_result = calculator(state["question"])

    return {"tool_result": tool_result}


# ── Node 6: Answer ────────────────────────────────────────
def answer_node(state: CapstoneState) -> dict:
    """
    Generates a grounded answer using retrieved context + conversation history.
    Respects the grounding rule: ONLY answer from provided context.
    """
    question     = state["question"]
    retrieved    = state.get("retrieved", "")
    tool_result  = state.get("tool_result", "")
    messages     = state.get("messages", [])
    eval_retries = state.get("eval_retries", 0)
    user_name    = state.get("user_name", "")

    greeting = f" You are speaking with {user_name}." if user_name else ""

    # Build context sections
    context_parts = []
    if retrieved:
        context_parts.append(f"AWS KNOWLEDGE BASE:\n{retrieved}")
    if tool_result:
        context_parts.append(f"TOOL RESULT:\n{tool_result}")
    context = "\n\n".join(context_parts)

    if context:
        system_content = f"""You are a helpful AWS Cloud Services assistant.{greeting}
Answer using ONLY the information provided in the context below.
If the answer is not in the context, respond: "I don't have that information in my knowledge base. For more details, please visit https://aws.amazon.com/documentation/"
Do NOT add information from your training data. Do NOT fabricate services, prices, or features.
Always be accurate and concise.

{context}"""
    else:
        system_content = f"""You are a helpful AWS Cloud Services assistant.{greeting}
Answer based on the conversation history. If unsure, ask the user to rephrase."""

    # On retry, add stronger grounding instruction
    if eval_retries > 0:
        system_content += "\n\nIMPORTANT: Your previous answer may not have been fully grounded. Use ONLY information explicitly stated in the context above."

    # Build LangChain message list
    lc_msgs = [SystemMessage(content=system_content)]
    for msg in messages[:-1]:
        if msg["role"] == "user":
            lc_msgs.append(HumanMessage(content=msg["content"]))
        else:
            lc_msgs.append(AIMessage(content=msg["content"]))
    lc_msgs.append(HumanMessage(content=question))

    response = llm.invoke(lc_msgs)
    return {"answer": response.content}


# ── Node 7: Eval ──────────────────────────────────────────
def eval_node(state: CapstoneState) -> dict:
    """
    Rates faithfulness of the answer against retrieved context.
    Below FAITHFULNESS_THRESHOLD triggers a retry (up to MAX_EVAL_RETRIES).
    """
    answer  = state.get("answer", "")
    context = state.get("retrieved", "")[:500]
    retries = state.get("eval_retries", 0)

    if not context:
        # No retrieval — skip faithfulness check
        return {"faithfulness": 1.0, "eval_retries": retries + 1}

    prompt = f"""Rate faithfulness: does this answer use ONLY information from the context?
Reply with ONLY a decimal number between 0.0 and 1.0.
1.0 = fully faithful to context. 0.5 = some extra information added. 0.0 = mostly hallucinated.

Context: {context}
Answer: {answer[:300]}"""

    result = llm.invoke(prompt).content.strip()
    try:
        score = float(result.split()[0].replace(",", "."))
        score = max(0.0, min(1.0, score))
    except Exception:
        score = 0.5

    gate = "✅" if score >= FAITHFULNESS_THRESHOLD else "⚠️"
    print(f"  [eval] Faithfulness: {score:.2f} {gate}")

    return {"faithfulness": score, "eval_retries": retries + 1}


# ── Node 8: Save ──────────────────────────────────────────
def save_node(state: CapstoneState) -> dict:
    """Appends the assistant answer to conversation history."""
    messages = list(state.get("messages", []))
    messages = messages + [{"role": "assistant", "content": state["answer"]}]
    return {"messages": messages}
