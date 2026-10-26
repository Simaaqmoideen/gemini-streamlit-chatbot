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
