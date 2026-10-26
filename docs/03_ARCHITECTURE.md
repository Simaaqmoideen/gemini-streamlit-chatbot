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

## Module responsibilities
See the files in `src/`. Keep logic (testable functions) separate from UI and scripts.
