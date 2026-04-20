"""
capstone_streamlit.py — AWS Cloud Assistant Streamlit UI
Run: streamlit run capstone_streamlit.py
"""
import streamlit as st
import uuid
import os
import sys

# Ensure the project root is in sys.path
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="AWS Cloud Assistant",
    page_icon="☁️",
    layout="centered"
)

st.title("☁️ AWS Cloud Assistant")
st.caption("Your intelligent guide to Amazon Web Services — asks answered from real AWS documentation.")


# ── Load agent (cached so models load once) ──────────────
@st.cache_resource
def load_agent():
    from app.graph import app, collection
    return app, collection


try:
    agent_app, collection = load_agent()
    st.success(f"✅ Knowledge base loaded — {collection.count()} AWS documents")
except Exception as e:
    st.error(f"Failed to load agent: {e}")
    st.stop()


# ── Session state ─────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())[:8]


# ── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.header("About")
    st.write(
        "This agent answers questions about Amazon Web Services (AWS) "
        "using a curated knowledge base. It remembers your conversation "
        "and uses a self-reflection quality gate."
    )
    st.write(f"**Session ID:** `{st.session_state.thread_id}`")
    st.divider()
    st.write("**Topics Covered:**")
    topics = [
        "AWS Overview & Regions",
        "EC2 Compute",
        "Lambda & Elastic Beanstalk",
        "Amazon S3 Storage",
        "EBS & EFS Storage",
        "Aurora & RDS Databases",
        "DynamoDB NoSQL",
        "Amazon Snowball Migration",
        "VPC & Direct Connect",
        "AWS CodeBuild",
        "CloudWatch Monitoring",
        "AWS Service Categories",
    ]
    for t in topics:
        st.write(f"• {t}")
    st.divider()
    if st.button("🗑️ New Conversation"):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())[:8]
        st.rerun()


# ── Display conversation history ──────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# ── Chat input ────────────────────────────────────────────
if prompt := st.chat_input("Ask about AWS services..."):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            config = {"configurable": {"thread_id": st.session_state.thread_id}}
            result = agent_app.invoke({"question": prompt}, config=config)
            answer = result.get("answer", "Sorry, I could not generate an answer.")
        st.write(answer)

        # Show metadata in caption
        faith    = result.get("faithfulness", 0.0)
        sources  = result.get("sources", [])
        route    = result.get("route", "")
        meta_str = f"Route: {route}"
        if faith > 0:
            meta_str += f" | Faithfulness: {faith:.2f}"
        if sources:
            meta_str += f" | Sources: {', '.join(sources[:2])}"
        st.caption(meta_str)

    st.session_state.messages.append({"role": "assistant", "content": answer})
