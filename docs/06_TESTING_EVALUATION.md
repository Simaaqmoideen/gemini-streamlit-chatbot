# Testing and Evaluation: AI Chatbot using Generative AI

## Success metrics
- Answers a 10-question test set sensibly (manual review)
- Remembers context across at least 5 turns
- Handles API failure without crashing
- Response starts in under ~3 s (streaming)

## Test plan
- [x] Unit: history trimming keeps the newest messages and respects the budget
- [x] Unit: empty input is rejected
- [x] Unit: Gemini request includes prior turns and the system prompt
- [x] Unit: Gemini API key is read from the environment
- [x] Unit: transient failures retry within a bound and errors are safe to display
- [x] Unit: streaming returns chunks and stores the completed reply
- [x] Unit: saved chats preserve settings and validate loaded JSON
- [ ] Manual: 10-question evaluation sheet (question, answer, correct Y/N)
- [ ] Manual: kill the network and confirm a friendly error appears

## How to run tests
```bash
python -m pytest -q
```

## Results log
| Date | Experiment / test | Result | Conclusion |
|---|---|---|---|
| 2026-10-26 | `python -m pytest -q` (Phase 1 setup) | 3 passed in 0.14s. Gemini API smoke test not run because no `GEMINI_API_KEY` is configured. | Existing unit tests pass; API connectivity and authentication are not yet verified. |
| 2026-10-26 | `python -m pytest -q` (Phase 2 core chat loop) | 4 passed in 0.08s. Mock verifies Gemini receives the system prompt and all prior turns. No live API call was made. | Request construction and local history updates pass; live model context retention is unverified. |
| 2026-10-26 | `python -m pytest -q` (Phase 3 UI controls) | 4 passed in 0.11s. Mock verifies the selected temperature is sent in Gemini configuration. | Session controls and request configuration pass; the Streamlit interface has not been manually exercised against a live API. |
| 2026-10-26 | `python -m pytest -q` (Phase 4 robustness) | 7 passed in 0.87s. Mocks verify rate-limit messaging, transient retry success and bounded retries, and removal of failed turns from history. | Error and retry paths pass unit tests; manual network failure test remains pending. |
| 2026-10-26 | `python -m pytest -q` (Phase 5 streaming and local save/load) | 12 passed in 4.96s with one SDK deprecation warning. `py_compile` passed for `src/app.py` and `src/chat.py`; mocks cover the key path and streaming, and temporary-directory tests cover JSON persistence and validation. | Core logic and source compilation pass; live Gemini and visual UI checks remain pending. |
