"""Streamlit chat UI.  Run:  streamlit run src/app.py"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # allow `python src/x.py`
import streamlit as st
from dotenv import load_dotenv

from src.chat import ChatSession, DEFAULT_SYSTEM

load_dotenv()
st.set_page_config(page_title="AI Chatbot", page_icon=":speech_balloon:")
st.title("AI Chatbot")

if "session" not in st.session_state:
    st.session_state.session = ChatSession()
session: ChatSession = st.session_state.session

with st.sidebar:
    st.header("Settings")
    session.system = st.text_area("System prompt", value=session.system or DEFAULT_SYSTEM, height=140)
    session.max_tokens = st.slider("Max reply tokens", 128, 2048, session.max_tokens, 64)
    if st.button("New conversation"):
        session.clear()
        st.rerun()

for m in session.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Ask something..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                st.markdown(session.send(prompt))
        except Exception as exc:  # show a friendly error instead of a stack trace
            session.messages.pop()  # remove the unanswered user turn
            st.error(f"Sorry, something went wrong: {exc}")
