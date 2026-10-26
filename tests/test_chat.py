import pytest
from src.chat import ChatSession, trim_history


def msgs(n, size=40):
    out = []
    for i in range(n):
        out.append({"role": "user" if i % 2 == 0 else "assistant", "content": "x" * size})
    return out


def test_trim_keeps_newest_and_starts_with_user():
    m = msgs(10)
    kept = trim_history(m, budget=35)  # ~10 tokens per message
    assert kept[-1] == m[-1]
    assert kept[0]["role"] == "user"
    assert len(kept) < len(m)


def test_trim_keeps_everything_when_budget_large():
    m = msgs(4)
    assert trim_history(m, budget=10_000) == m


def test_empty_input_rejected():
    with pytest.raises(ValueError):
        ChatSession().send("   ")


class FakeResponse:
    def __init__(self, text):
        self.text = text


class FakeModels:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.calls = []

    def generate_content(self, **kwargs):
        self.calls.append(kwargs)
        return next(self.responses)


class FakeClient:
    def __init__(self, responses):
        self.models = FakeModels(responses)


def test_send_uses_gemini_and_sends_prior_turns():
    client = FakeClient([FakeResponse("Hello!"), FakeResponse("It was blue.")])
    session = ChatSession(_client=client)

    assert session.send("Hi") == "Hello!"
    assert session.send("What color was it?") == "It was blue."

    first_call, second_call = client.models.calls
    assert first_call["model"] == "gemini-3.8-flash"
    assert first_call["config"]["system_instruction"] == session.system
    assert second_call["contents"] == [
        {"role": "user", "parts": [{"text": "Hi"}]},
        {"role": "model", "parts": [{"text": "Hello!"}]},
        {"role": "user", "parts": [{"text": "What color was it?"}]},
    ]
    assert session.messages[-1] == {
        "role": "assistant",
        "content": "It was blue.",
    }
