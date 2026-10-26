# Project Brief: AI Chatbot using Generative AI

## One-line summary
A simple chat app that answers user questions with a large language model.

## Problem statement
People want quick, conversational answers. This project builds a small chat application on top of an LLM API, with conversation memory and a configurable persona.

## Learning goals
How tools like ChatGPT work at a basic level: prompts, context windows, tokens, system prompts, streaming and conversation memory.

## Target users
- Students who want a study helper
- Anyone who wants a simple, private chat UI you control

## In scope
- Chat UI with message history
- Calls an LLM API with the full conversation context
- Configurable system prompt (persona / rules)
- API key read from environment, never hard-coded
- Graceful error handling (rate limit, network, empty input)

## Out of scope (for v1)
- Production-scale infrastructure, authentication and payments
- Anything under "Could have" in `02_REQUIREMENTS.md` unless time remains

## Success criteria
- Answers a 10-question test set sensibly (manual review)
- Remembers context across at least 5 turns
- Handles API failure without crashing
- Response starts in under ~3 s (streaming)

## Owner / timeline
- Owner: _your name_
- Start date: ____  Target finish: ____ (see `05_ROADMAP.md`)
