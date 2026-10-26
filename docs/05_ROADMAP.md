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

- [ ] Task completed
- [ ] Notes written in the project log
- [ ] Changes committed

## Phase 4: Robustness
History trimming, retries / error messages, input validation. Write the unit tests.

- [ ] Task completed
- [ ] Notes written in the project log
- [ ] Changes committed

## Phase 5: Polish and ship
Streaming, save/load chats, README screenshots, deploy, record a 2-minute demo.

- [ ] Task completed
- [ ] Notes written in the project log
- [ ] Changes committed

## Project log
| Date | What I did | Blockers | Next |
|---|---|---|---|
| 2026-10-26 | Added Gemini SDK dependency and environment configuration, then implemented `ChatSession.send()` with Gemini conversation context; test suite passed (4 tests). | No local `GEMINI_API_KEY`, so the terminal smoke test and live five-turn memory check remain pending. | Add the key locally, run `python -m src.chat`, then verify context across five turns. |
