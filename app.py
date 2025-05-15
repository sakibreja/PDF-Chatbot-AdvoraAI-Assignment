# app.py
import streamlit as st
import os
from groq_chain import PDFQueryAgent
from tempfile import NamedTemporaryFile

st.set_page_config(page_title="PDF Chatbot (AdvoraAI)", layout="wide")
st.title("📄 Ask Questions from Your PDF")

# API Key Input
if "GROQ_API_KEY" not in os.environ:
    api_key = st.text_input("🔐 Enter your GROQ API key", type="password")
    if api_key:
        os.environ["GROQ_API_KEY"] = api_key

# Upload PDF
pdf_file = st.file_uploader("📤 Upload a PDF", type=["pdf"])
if pdf_file and "agent" not in st.session_state:
    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(pdf_file.read())
        st.session_state.agent = PDFQueryAgent(tmp_file.name)
        st.success("✅ PDF successfully processed!")

# Chat memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat box
if "agent" in st.session_state:
    question = st.text_input("💬 Ask a question about the PDF:")
    if question:
        with st.spinner("Thinking..."):
            answer = st.session_state.agent.query(question)
            st.session_state.chat_history.append({"user": question, "ai": answer})
            st.session_state.chat_history = st.session_state.chat_history[-5:]

# Display chat
if st.session_state.chat_history:
    st.markdown("### 🕒 Chat History (Last 5)")
    for msg in reversed(st.session_state.chat_history):
        st.markdown(f"**You:** {msg['user']}")
        st.markdown(f"**AI:** {msg['ai']}")
