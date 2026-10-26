"""Streamlit chat UI. Run: streamlit run src/app.py"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import streamlit as st
from dotenv import load_dotenv

from src.chat import ChatError, ChatSession, user_error_message

load_dotenv()
CHAT_PATH = pathlib.Path(__file__).resolve().parents[1] / "data" / "chat_history.json"
st.set_page_config(page_title="AI Chatbot", page_icon=":speech_balloon:")
st.title("AI Chatbot")

if "session" not in st.session_state:
    st.session_state.session = ChatSession()
session: ChatSession = st.session_state.session
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = session.system
if "max_tokens" not in st.session_state:
    st.session_state.max_tokens = session.max_tokens
if "temperature" not in st.session_state:
    st.session_state.temperature = session.temperature


def load_saved_conversation() -> None:
    """Load a chat before Streamlit recreates widgets on the next run."""
    try:
        loaded = ChatSession.load(CHAT_PATH)
    except FileNotFoundError:
        st.session_state.load_notice = ("warning", "No saved conversation was found.")
        return
    except (OSError, ValueError):
        st.session_state.load_notice = ("error", "The saved conversation could not be loaded.")
        return

    st.session_state.session = loaded
    st.session_state.system_prompt = loaded.system
    st.session_state.max_tokens = loaded.max_tokens
    st.session_state.temperature = loaded.temperature
    st.session_state.load_notice = ("success", "Conversation loaded.")


with st.sidebar:
    st.header("Settings")
    session.system = st.text_area("System prompt", height=140, key="system_prompt")
    session.max_tokens = st.slider("Max reply tokens", 128, 2048, step=64, key="max_tokens")
    session.temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        step=0.1,
        help="Lower values make replies more focused; higher values add variety.",
        key="temperature",
    )
    if st.button("New conversation"):
        session.clear()
        st.rerun()
    st.divider()
    if st.button("Save conversation"):
        try:
            session.save(CHAT_PATH)
            st.success("Conversation saved locally.")
        except OSError:
            st.error("Could not save the conversation file.")
    st.button("Load saved conversation", on_click=load_saved_conversation)

if notice := st.session_state.pop("load_notice", None):
    level, message = notice
    getattr(st, level)(message)

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
                st.write_stream(session.stream(prompt))
        except ChatError as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error(user_error_message(exc))
