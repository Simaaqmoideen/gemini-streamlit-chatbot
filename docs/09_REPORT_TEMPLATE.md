# Final Report: AI Chatbot using Generative AI

## 1. Title, author, date

- **Title:** AI Chatbot using Generative AI
- **Author:** Project owner (name not provided)
- **Date:** 2026-10-26

## 2. Abstract

This project builds a small conversational study helper using a Gemini model. A Streamlit interface sends the system instruction and local conversation turns to the Gemini API through Google's Gen AI Python SDK. No training dataset is used, and conversations can optionally be saved as local JSON. The automated test suite passes 12 tests, and the interface was opened and visually checked. A short live streaming check returned a temporary-unavailable error, so live answer quality and latency were not measured.

## 3. Introduction

Conversational assistants can help users explore questions and follow up without repeating context. This project provides a small, inspectable example of a chat UI, configurable instructions, conversation history, and an LLM API call. It is a learning demo; users should verify important answers.

## 4. Data

- **Source and size:** No training or evaluation dataset is specified or used.
- **Inference input:** User messages and conversation history are sent to the Gemini API.
- **Persistence:** The user may save one conversation to `data/chat_history.json` on the local machine. The file is unencrypted and excluded from Git.
- **Limitations:** No fixed question set was evaluated. Do not save sensitive messages.

## 5. Method

The Streamlit UI keeps a `ChatSession` in session state. `ChatSession` sends the configured system instruction, temperature, output limit, low-by-default Gemini thinking level, and prior user/model turns through Google's Gen AI SDK. Assistant turns are translated to Gemini's `model` role. UI replies use the SDK streaming call; transient failures are retried a bounded number of times, and displayed errors omit provider details. A rough character-based estimate trims old history. Local JSON save/load preserves conversation settings and validates message roles/content.

## 6. Results

| Measure | Starter baseline | Implemented project | Interpretation |
|---|---:|---:|---|
| Automated tests passing | 3 of 3 (0.14s) | 12 of 12 (3.12s; one SDK deprecation warning) | Unit coverage grew; this is not a measure of model quality. |
| Live answer quality on 10 prompts | Not measured | Not measured | Short live request returned a temporary-unavailable error; manual set remains pending. |
| Context recall across 5 turns | Not measured | Not measured | Request construction is unit-tested; live Gemini recall is unverified. |
| Response latency | Not measured | Not measured | Speed-tuned to low thinking; live stream test returned a temporary-unavailable error, so no latency result was recorded. |

## 7. Discussion

The unit tests confirm conversation request construction, retry behavior, user-safe error conversion, streaming chunk handling, low thinking-level configuration, and local JSON persistence. They use fake clients and do not measure Gemini's generated answers. The Streamlit app opened successfully in a local browser and its interface is shown in `reports/chatbot-ui.png`. A response demo recording was not captured because the live streaming check did not produce an answer.

## 8. Limitations and ethics

- LLM responses can be wrong or overconfident; the UI tells users to check important information.
- Live API behavior, five-turn recall, answer quality, and latency remain unverified; a short request returned a temporary-unavailable error.
- Local chat JSON is unencrypted. Users should avoid saving sensitive content.
- History token counts are approximate and may not match Gemini's actual tokenizer.
- Gemini API terms, availability, quotas, and billing apply to requests.

## 9. Future work

Retry the terminal smoke test when Gemini is available, manually assess a 10-question set, verify five-turn recall, test a network failure, and record the required UI demo. Deployment is a Could-have stretch item and is not part of this build.

## 10. References

- [Gemini API text generation documentation](https://ai.google.dev/gemini-api/docs/generate-content/text-generation?hl=en)
- [Google Gen AI Python SDK documentation](https://googleapis.github.io/python-genai/)
- Streamlit, `python-dotenv`, and pytest package documentation.

## 11. Appendix: setup

Follow the PowerShell quick-start in the project README. Copy `.env.example` to `.env`, add `GEMINI_API_KEY` locally, install `requirements.txt`, then run `streamlit run src/app.py`. Run automated tests with `python -m pytest -q` from this project directory.
