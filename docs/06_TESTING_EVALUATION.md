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
| 2026-10-26 | `python -m pytest -q` (Phase 5 streaming and local save/load) | 12 passed in 4.96s with one SDK deprecation warning. `py_compile` passed for `src/app.py` and `src/chat.py`; mocks cover the key path and streaming, and temporary-directory tests cover JSON persistence and validation. Streamlit app opened; `reports/chatbot-ui.png` captured. | Core logic, source compilation, and initial UI rendering verified; live Gemini evaluation and manual network failure test remain pending. |
| 2026-10-26 | `python -m pytest -q --basetemp .pytest-temp/run` (final rerun in the project virtual environment) | 12 passed in 2.61s with one SDK deprecation warning. Streamlit UI was visually inspected in the local browser. | Unit suite and app rendering pass; live Gemini evaluation and manual network failure test remain pending. |
| 2026-10-26 | `python -m pytest -q --basetemp .pytest-temp/speed-fix` after adding low thinking config to normal and streaming requests | 12 passed in 3.12s with one SDK deprecation warning. A short live stream returned the app's safe temporary-unavailable error, so no latency number was recorded. | Request configuration is unit-tested; actual provider latency remains unmeasured. |
| 2026-10-26 | Live API diagnostic with a one-word prompt | Gemini 3.8 Flash returned HTTP 503 in 3.58s. Gemini 3.5 Flash-Lite returned a chunk after 33.06s with minimal thinking. | The key can reach Gemini, but provider availability/latency is currently poor; the model change alone did not make responses fast. |
| 2026-10-26 | `python -m pytest -q --basetemp .pytest-temp/provider-error` after improving escaped-error mapping | 13 passed in 3.04s with one SDK deprecation warning. | Provider errors now map to safe, actionable UI messages. |
| 2026-10-26 | End-to-end Streamlit smoke check using Gemini 3.5 Flash-Lite with minimal thinking | Prompt asked for exact text `READY_OK`; the app displayed `READY_OK`. Exact response latency was not measured. | The restarted app can reach Gemini and render a short response; this does not evaluate answer quality or latency. |
| 2026-10-26 | `python -m pytest -q --basetemp .pytest-temp/lite-default-rerun` | 13 passed in 3.22s with one SDK deprecation warning. | Unit suite passes with the tested Flash-Lite/minimal defaults. |
