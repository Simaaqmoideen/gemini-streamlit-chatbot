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


def test_stream_yields_chunks_and_saves_complete_reply():
    class StreamingModels:
        def __init__(self):
            self.calls = []

        def generate_content_stream(self, **kwargs):
            self.calls.append(kwargs)
            yield FakeResponse("Hello")
            yield FakeResponse(" there")

    class StreamingClient:
        def __init__(self):
            self.models = StreamingModels()

    client = StreamingClient()
    session = ChatSession(_client=client)

    assert list(session.stream("Hi")) == ["Hello", " there"]
    assert client.models.calls[0]["contents"] == [
        {"role": "user", "parts": [{"text": "Hi"}]}
    ]
    assert session.messages[-1] == {"role": "assistant", "content": "Hello there"}


def test_chat_session_saves_and_loads_local_json(tmp_path):
    source = ChatSession(
        system="Be concise",
        model="gemini-test-model",
        max_tokens=300,
        temperature=0.4,
        history_budget=1200,
        messages=[{"role": "user", "content": "Hi"}],
        _client=object(),
    )
    path = tmp_path / "saved" / "chat.json"

    source.save(path)
    loaded = ChatSession.load(path)

    assert loaded.system == source.system
    assert loaded.model == source.model
    assert loaded.max_tokens == source.max_tokens
    assert loaded.temperature == source.temperature
    assert loaded.history_budget == source.history_budget
    assert loaded.messages == source.messages
    assert loaded._client is None


def test_chat_session_rejects_invalid_saved_json(tmp_path):
    path = tmp_path / "invalid.json"
    path.write_text('{"version": 1, "messages": [{"role": "tool"}]}', encoding="utf-8")

    with pytest.raises(ValueError, match="invalid messages"):
        ChatSession.load(path)


def test_client_reads_gemini_api_key_from_environment(monkeypatch):
    from google import genai

    expected_key = "test-key-from-environment"
    monkeypatch.setenv("GEMINI_API_KEY", expected_key)
    client = FakeClient([])
    received = {}

    def make_client(api_key):
        received["api_key"] = api_key
        return client

    monkeypatch.setattr(genai, "Client", make_client)

    assert ChatSession()._get_client() is client
    assert received["api_key"] == expected_key


def test_clear_starts_a_new_conversation():
    session = ChatSession(messages=[{"role": "user", "content": "old turn"}])

    session.clear()

    assert session.messages == []
