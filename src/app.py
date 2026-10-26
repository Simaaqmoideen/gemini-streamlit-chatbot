"""Streamlit chat UI.  Run:  streamlit run src/app.py"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # allow `python src/x.py`
import streamlit as st
from dotenv import load_dotenv

from src.chat import ChatError, ChatSession, DEFAULT_SYSTEM

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
    session.temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=float(session.temperature),
        step=0.1,
        help="Lower values make replies more focused; higher values add variety.",
    )
    if st.button("New conversation"):
        session.clear()
        st.rerun()

st.caption("AI can make mistakes. Check important information.")

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
        except ChatError as exc:
            st.error(str(exc))
        except Exception:
            st.error("The chat could not complete that request. Please try again.")
