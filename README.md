# AWS Cloud Assistant — Agentic AI Capstone Project
**Roll Number:** 23051192 | **Course:** Agentic AI 2026

## Project Overview
An intelligent LangGraph-based agent that answers questions about Amazon Web Services using a curated knowledge base, conversation memory, self-reflection quality gating, and tool use.

## 6 Mandatory Capabilities
1. ✅ **LangGraph StateGraph** — 8 nodes: memory → router → retrieve/skip/tool → answer → eval → save
2. ✅ **ChromaDB RAG** — 12 domain documents with SentenceTransformer embeddings
3. ✅ **MemorySaver + thread_id** — persistent multi-turn conversation memory
4. ✅ **Self-reflection eval node** — faithfulness scoring with retry loop (threshold 0.7)
5. ✅ **Tool use** — `get_current_datetime()` and `calculator()` tools
6. ✅ **Streamlit deployment** — fully functional chat UI with sidebar

## Project Structure
```
AGENTIC-PROJECT_23051192/
├── app/
│   ├── state.py           # CapstoneState TypedDict
│   ├── knowledge_base.py  # 12 AWS domain documents
│   ├── tools.py           # datetime + calculator tools
│   ├── nodes.py           # All 8 node functions
│   └── graph.py           # StateGraph + ChromaDB init
├── api/
│   └── main.py            # FastAPI endpoint
├── ui/
│   └── app.py             # Streamlit UI (alternate path)
├── tests/
│   └── test_agent.py      # 10 tests (2 red-team)
├── Data/
│   └── AWS (1).pdf        # Source document
├── agent.py               # Shared ask() helper
├── capstone_streamlit.py  # Main Streamlit app
├── day13_capstone.ipynb   # Completed notebook
├── requirements.txt
└── .env.example
```

## Setup & Run
```bash
# 1. Create .env file
cp .env.example .env
# Edit .env and add your GROQ_API_KEY from https://console.groq.com

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run Streamlit UI
streamlit run capstone_streamlit.py

# 4. Run tests
python tests/test_agent.py
```

## Domain
**AWS Cloud Services** — covers EC2, S3, Lambda, DynamoDB, VPC, CloudWatch, Aurora, EBS, EFS, Snowball, CodeBuild, and more.
