# Architecture: AI Chatbot using Generative AI

## Overview
```
User -> Streamlit UI (src/app.py)
          |
          v
   ChatSession (src/chat.py)
     - holds message history
     - trims history to a budget
     - builds request (system prompt + messages)
          |
          v
   Gemini API (Google Gen AI Python SDK)
          |
          v
   Reply -> appended to history -> rendered in UI
```

## Tech stack
- Python 3.10+
- Streamlit (UI)
- Google Gen AI Python SDK (`google-genai`)
- python-dotenv
- pytest

## Design decisions (fill in as you go)
| Decision | Options considered | Choice | Why |
|---|---|---|---|
| LLM provider | Anthropic, Gemini, OpenAI | Gemini API | Selected by the project owner; authenticate with `GEMINI_API_KEY`. |
| Conversation context | Provider-managed session, local history | Send local history with each request | Keeps `ChatSession` testable and lets the app control its conversation history. Assistant turns map to Gemini's `model` role. |
| Reply variation | Fixed, user-configurable | Temperature control in the Streamlit sidebar | Lets users tune response variation per session. |
| Saved chats | No persistence, local JSON | `data/chat_history.json` | Simple local save/load for the demo; the key is never stored in the chat file. |

Gemini 3.8 Flash uses `THINKING_LEVEL=low` by default to reduce first-token latency for everyday chat; users can choose `medium` or `high` in `.env` for more reasoning.

## Module responsibilities
See the files in `src/`. Keep logic (testable functions) separate from UI and scripts.
