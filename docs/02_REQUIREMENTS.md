# Requirements: AI Chatbot using Generative AI

## Functional requirements (MoSCoW)

### Must have
- [x] Chat UI with message history
- [x] Calls an LLM API with the full conversation context
- [x] Configurable system prompt (persona / rules)
- [x] API key read from environment, never hard-coded
- [x] Graceful error handling (rate limit, network, empty input)

### Should have
- [x] Streaming responses
- [x] Trim old history to stay inside the context window
- [x] Clear / new conversation button
- [x] Save and load chats to a local JSON file

### Could have (stretch)
- [ ] Retrieval over your own PDFs (RAG)
- [ ] Multiple personas
- [ ] Token and cost counter
- [ ] Deployment on Streamlit Cloud / Render

## Non-functional requirements
- **Reproducible:** a fresh clone runs end to end with the commands in README.md.
- **Secure:** secrets only in `.env`; no keys, tokens or personal data in Git.
- **Readable:** type hints on public functions, docstrings on modules, PEP 8 formatting.
- **Tested:** automated tests for core logic; they pass before every merge.
- **Documented:** README and docs updated whenever behaviour changes.

## Assumptions
- Python 3.10 or newer; internet access to install packages and fetch data.
- Free-tier / free-dataset resources are used wherever possible.

## Constraints
- Solo or small-team student project; target is a working demo, not production.
