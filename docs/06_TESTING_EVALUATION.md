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
