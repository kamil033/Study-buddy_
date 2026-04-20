"""
agent.py — Shared agent module for the AWS Cloud Assistant
Exposes the compiled LangGraph app and helper ask() function.
"""
import os, sys
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from dotenv import load_dotenv
load_dotenv()

from app.graph import app, collection, embedder

def ask(question: str, thread_id: str = "default") -> dict:
    """Run the agent for a single question. Returns full result dict."""
    config = {"configurable": {"thread_id": thread_id}}
    result = app.invoke({"question": question}, config=config)
    return result

if __name__ == "__main__":
    print("=== AWS Cloud Assistant — Quick Test ===\n")
    r = ask("What is Amazon EC2?", thread_id="smoke-test")
    print(f"Q: What is Amazon EC2?")
    print(f"A: {r['answer'][:300]}")
    print(f"Route: {r['route']} | Faithfulness: {r.get('faithfulness', 0):.2f}")
