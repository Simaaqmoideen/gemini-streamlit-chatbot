# Roadmap: AI Chatbot using Generative AI

Suggested pace: one phase every 2-4 days (about 2-3 weeks in total).

## Phase 1: Setup
Create virtual env, install requirements, get an API key, put it in `.env`. Run `python -m src.chat` for a one-shot terminal test.

- [ ] Task completed
- [x] Notes written in the project log
- [x] Changes committed

## Phase 2: Core chat loop
Implement `ChatSession.send()` with history. Verify the model remembers earlier turns.

- [ ] Task completed
- [x] Notes written in the project log
- [x] Changes committed

## Phase 3: UI
Build the Streamlit chat page. Add sidebar controls: persona, temperature, clear chat.

- [x] Task completed
- [x] Notes written in the project log
- [x] Changes committed

## Phase 4: Robustness
History trimming, retries / error messages, input validation. Write the unit tests.

- [x] Task completed
- [x] Notes written in the project log
- [x] Changes committed

## Phase 5: Polish and ship
Streaming, save/load chats, README screenshots, deploy, record a 2-minute demo.

- [ ] Task completed
- [x] Notes written in the project log
- [x] Changes committed

## Project log
| Date | What I did | Blockers | Next |
|---|---|---|---|
| 2026-10-26 | Added Gemini SDK dependency and environment configuration; suite passed (3 tests). | No local `GEMINI_API_KEY`; Phase 1 one-shot smoke test pending. | Set key locally and run `python -m src.chat`. |
| 2026-10-26 | Implemented Gemini `ChatSession.send()` with local conversation context; suite passed (4 tests). | No local API key; live five-turn memory check pending. | Verify context across five turns when the key is configured. |
| 2026-10-26 | Added persona, reply length, temperature, and new-conversation controls to the Streamlit UI; suite passed (4 tests). | Live UI/API interaction not verified without an API key. | Phase 4: add validation and friendly API error handling. |
| 2026-10-26 | Added retry handling for transient Gemini failures, safe error messages, input type validation, and rollback of failed turns; suite passed (7 tests). | No local API key, so a real network failure check remains pending. | Phase 5: consider Should-have features after Must-have checks are complete. |
| 2026-10-26 | Added streaming, local JSON save/load, save-file validation, explicit environment-key handling, and README evaluation results; final test suite passed (12 tests). Opened the Streamlit app and captured `reports/chatbot-ui.png`. | No local API key; live Gemini evaluation and response demo remain incomplete. | Configure a key, complete manual evaluation, and record a demo with a real answer. |
| 2026-10-26 | Re-ran the full suite in the project virtual environment (12 passed in 2.61s; one SDK deprecation warning), confirmed the app UI in the browser, and added the screenshot to the README. | Default system Python lacks pytest; project virtual environment works. No local Gemini API key, so live answer evaluation and response demo remain pending. | Configure a key locally, complete the manual evaluation, then record the response demo. |
