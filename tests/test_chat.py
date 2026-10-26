import pytest
from src.chat import ChatError, ChatSession, trim_history


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
    session.temperature = 0.2

    assert session.send("Hi") == "Hello!"
    assert session.send("What color was it?") == "It was blue."

    first_call, second_call = client.models.calls
    assert first_call["model"] == "gemini-3.8-flash"
    assert first_call["config"]["system_instruction"] == session.system
    assert first_call["config"]["temperature"] == 0.2
    assert second_call["contents"] == [
        {"role": "user", "parts": [{"text": "Hi"}]},
        {"role": "model", "parts": [{"text": "Hello!"}]},
        {"role": "user", "parts": [{"text": "What color was it?"}]},
    ]
    assert session.messages[-1] == {
        "role": "assistant",
        "content": "It was blue.",
    }


class FakeAPIError(Exception):
    def __init__(self, code, detail="private provider detail"):
        super().__init__(detail)
        self.code = code


def test_send_retries_transient_errors(monkeypatch):
    client = FakeClient([FakeResponse("Recovered")])
    succeed = client.models.generate_content
    failures = iter([FakeAPIError(503), FakeAPIError(503)])

    def fail_twice_then_succeed(**kwargs):
        try:
            raise next(failures)
        except StopIteration:
            return succeed(**kwargs)

    client.models.generate_content = fail_twice_then_succeed
    delays = []
    monkeypatch.setattr("src.chat.time.sleep", delays.append)
    session = ChatSession(_client=client)

    assert session.send("hello") == "Recovered"
    assert delays == [0.25, 0.5]


def test_send_returns_friendly_error_and_rolls_back_failed_turn():
    class FailingModels:
        def generate_content(self, **kwargs):
            raise FakeAPIError(429)

    class FailingClient:
        models = FailingModels()

    session = ChatSession(_client=FailingClient())

    with pytest.raises(ChatError, match="too many requests") as raised:
        session.send("hello")

    assert "private provider detail" not in str(raised.value)
    assert session.messages == []


def test_send_stops_after_bounded_retries(monkeypatch):
    class FailingModels:
        def __init__(self):
            self.calls = 0

        def generate_content(self, **kwargs):
            self.calls += 1
            raise FakeAPIError(503)

    class FailingClient:
        def __init__(self):
            self.models = FailingModels()

    monkeypatch.setattr("src.chat.time.sleep", lambda _delay: None)
    client = FailingClient()
    session = ChatSession(_client=client)

    with pytest.raises(ChatError, match="temporarily unavailable"):
        session.send("hello")

    assert client.models.calls == 3
    assert session.messages == []
