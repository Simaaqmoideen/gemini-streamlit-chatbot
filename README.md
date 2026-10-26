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
Run the tests with `python -m pytest -q` from this folder.
For a terminal API smoke test, set `GEMINI_API_KEY` in `.env` and run `python -m src.chat`. In the app, use the sidebar to set assistant instructions, reply length, and temperature, or start a new conversation.
Temporary rate-limit, server, and network failures are retried a limited number of times; errors shown in the UI avoid exposing provider details.

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
