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

## Module responsibilities
See the files in `src/`. Keep logic (testable functions) separate from UI and scripts.
