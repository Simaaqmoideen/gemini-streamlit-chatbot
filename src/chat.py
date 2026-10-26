"""Chat session logic, independent of any UI so it is easy to test."""
import os
from dataclasses import dataclass, field

DEFAULT_SYSTEM = (
    "You are a helpful, concise assistant. If you are not sure about something, "
    "say so instead of guessing."
)


def estimate_tokens(text: str) -> int:
    """Rough estimate: ~4 characters per token. Good enough for trimming."""
    return max(1, len(text) // 4)


def trim_history(messages: list[dict], budget: int) -> list[dict]:
    """Keep the newest messages whose estimated tokens fit in `budget`.

    Always keeps at least the latest message.
    """
    kept, used = [], 0
    for msg in reversed(messages):
        cost = estimate_tokens(msg["content"])
        if kept and used + cost > budget:
            break
        kept.append(msg)
        used += cost
    kept.reverse()
    # The API expects the first message to come from the user.
    while len(kept) > 1 and kept[0]["role"] != "user":
        kept.pop(0)
    return kept


@dataclass
class ChatSession:
    system: str = DEFAULT_SYSTEM
    model: str = field(default_factory=lambda: os.getenv("MODEL", "claude-sonnet-5-5"))
    max_tokens: int = 1024
    history_budget: int = 6000
    messages: list = field(default_factory=list)
    _client: object = None

    def _get_client(self):
        if self._client is None:
            import anthropic  # imported lazily so tests do not need the SDK

            self._client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
        return self._client

    def send(self, user_text: str) -> str:
        user_text = (user_text or "").strip()
        if not user_text:
            raise ValueError("Message is empty.")
        self.messages.append({"role": "user", "content": user_text})
        window = trim_history(self.messages, self.history_budget)
        resp = self._get_client().messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=self.system,
            messages=window,
        )
        reply = "".join(b.text for b in resp.content if getattr(b, "text", None))
        self.messages.append({"role": "assistant", "content": reply})
        return reply

    def clear(self):
        self.messages.clear()


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    s = ChatSession()
    print(s.send("In one sentence, what is a context window?"))
