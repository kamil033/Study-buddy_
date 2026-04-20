from typing import TypedDict, List


class CapstoneState(TypedDict):
    # ── Input ──────────────────────────────────────────────
    question:      str          # user's current question

    # ── Memory ─────────────────────────────────────────────
    messages:      List[dict]   # conversation history (role/content dicts)

    # ── Routing ────────────────────────────────────────────
    route:         str          # "retrieve", "memory_only", or "tool"

    # ── RAG ────────────────────────────────────────────────
    retrieved:     str          # ChromaDB context chunks
    sources:       List[str]    # source topic names

    # ── Tool ───────────────────────────────────────────────
    tool_result:   str          # output from tool call

    # ── Answer ─────────────────────────────────────────────
    answer:        str          # final LLM response

    # ── Quality control ────────────────────────────────────
    faithfulness:  float        # eval score 0.0–1.0
    eval_retries:  int          # safety valve counter

    # ── Domain-specific ────────────────────────────────────
    user_name:     str          # extracted user name if provided
