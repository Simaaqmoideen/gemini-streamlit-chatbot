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
The default is Gemini 3.5 Flash-Lite with minimal reasoning because Gemini 3.8 Flash returned HTTP 503 during a live check. Change `MODEL` in `.env` to select another available Gemini model. For more reasoning, set `THINKING_LEVEL=low` or `medium`, which can add delay.
Run the tests with `python -m pytest -q` from this folder.
For a terminal API smoke test, set `GEMINI_API_KEY` in `.env` and run `python -m src.chat`. In the app, use the sidebar to set assistant instructions, reply length, and temperature, or start a new conversation.
Temporary rate-limit, server, and network failures are retried a limited number of times; errors shown in the UI avoid exposing provider details.
Replies stream into the chat. The sidebar can save or load one conversation at `data/chat_history.json`; this file is local, unencrypted, and excluded from Git.

## Results and evaluation

The Streamlit interface was manually opened and visually inspected. The screenshot below shows a successful short UI smoke test. Gemini 3.8 Flash returned HTTP 503 in a direct check; the app now defaults to Gemini 3.5 Flash-Lite, which returned the test reply. The UI run's exact latency was not measured.

![AI Chatbot Streamlit interface](reports/chatbot-ui.png)

| Check | Result |
|---|---|
| Starter test suite | 3 passed in 0.14s |
| Current test suite | 13 passed in 3.22s (1 SDK deprecation warning) |
| Live Gemini answer quality, five-turn memory, and response latency | Short Flash-Lite UI smoke test succeeded. One direct check took 33.06s to first chunk; exact UI latency and answer quality were not measured. |

The app uses Gemini 3.5 Flash-Lite with minimal reasoning by default. A direct one-off request took 33.06s to first chunk; the later UI smoke test succeeded, but its exact latency was not measured. Treat these as diagnostics, not a stable benchmark. Google's docs describe minimal reasoning as the latency-oriented setting for Flash-Lite. The test-suite comparison reports automated test health, not model answer quality. Complete the manual evaluation before drawing conclusions about generated answers.

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
