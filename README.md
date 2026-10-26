# Project 1: AI Chatbot using Generative AI

> A simple chat app that answers user questions with a large language model.

**What you will learn:** How tools like ChatGPT work at a basic level: prompts, context windows, tokens, system prompts, streaming and conversation memory.

## Quick start
```powershell
python -m venv .venv
\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Edit .env and set GEMINI_API_KEY from https://aistudio.google.com/app/apikey
streamlit run src/app.py
```
On macOS or Linux, activate with `source .venv/bin/activate` and copy the template with `cp .env.example .env`.
`THINKING_LEVEL` defaults to `low` for faster everyday chat replies; set it to `medium` or `high` in `.env` when a task needs more reasoning (which can add delay).
Run the tests with `python -m pytest -q` from this folder.
For a terminal API smoke test, set `GEMINI_API_KEY` in `.env` and run `python -m src.chat`. In the app, use the sidebar to set assistant instructions, reply length, and temperature, or start a new conversation.
Temporary rate-limit, server, and network failures are retried a limited number of times; errors shown in the UI avoid exposing provider details.
Replies stream into the chat. The sidebar can save or load one conversation at `data/chat_history.json`; this file is local, unencrypted, and excluded from Git.

## Results and evaluation

The Streamlit interface was manually opened and visually inspected. The screenshot below shows the chat composer and settings sidebar. A later short live streaming check returned a temporary-unavailable error, so no generated-answer evaluation was recorded.

![AI Chatbot Streamlit interface](reports/chatbot-ui.png)

| Check | Result |
|---|---|
| Starter test suite | 3 passed in 0.14s |
| Current test suite | 13 passed in 3.04s (1 SDK deprecation warning) |
| Live Gemini answer quality, five-turn memory, and response latency | Gemini 3.8 Flash returned HTTP 503 (3.58s). Flash-Lite replied, but its first chunk took 33.06s with minimal thinking. No answer-quality evaluation was recorded. |

The app now defaults Gemini reasoning to `low` through `THINKING_LEVEL` to favor faster first output. Google's docs note that Gemini 3.8 Flash defaults to medium and that lower thinking effort reduces time-to-answer. The measured slow/failed live requests indicate provider latency or availability is also a factor. The test-suite comparison reports automated test health, not model answer quality. Complete the manual evaluation before drawing conclusions about generated answers.

## Folder map
| Path | Purpose |
|---|---|
| `docs/01_PROJECT_BRIEF.md` | Problem, users, scope, success criteria |
| `docs/02_REQUIREMENTS.md` | Must / should / could requirements and non-functional needs |
| `docs/03_ARCHITECTURE.md` | Design, components, tech stack |
| `docs/04_DATA.md` | Data sources, schema and data rules |
| `docs/05_ROADMAP.md` | Phase-by-phase build plan with checklists |
| `docs/06_TESTING_EVALUATION.md` | Test plan and evaluation metrics |
| `docs/07_RISKS_ETHICS.md` | Risks, mitigations, ethics notes |
| `docs/08_DELIVERABLES_CHECKLIST.md` | Definition of done |
| `docs/09_REPORT_TEMPLATE.md` | Final report / presentation outline |
| `src/` | Starter source code |
| `tests/` | Automated tests |
| `data/` | Datasets (git-ignored except samples) |
| `notebooks/` | Exploration notebooks |
| `reports/` | Generated charts and metrics |

## Tech stack
- Python 3.10+
- Streamlit (UI)
- Google Gen AI Python SDK (`google-genai`)
- python-dotenv
- pytest
