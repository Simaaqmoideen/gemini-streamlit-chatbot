"""Chat session logic, independent of any UI so it is easy to test."""
import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

DEFAULT_SYSTEM = (
    "You are a helpful, concise assistant. If you are not sure about something, "
    "say so instead of guessing."
)
MAX_API_ATTEMPTS = 3
RETRY_DELAYS_SECONDS = (0.25, 0.5)
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


class ChatError(Exception):
    """A user-safe error raised when a Gemini request cannot complete."""


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


def _status_code(error: Exception) -> int | None:
    """Read an HTTP status from the Gemini SDK error or its response."""
    for value in (
        getattr(error, "code", None),
        getattr(error, "status_code", None),
        getattr(getattr(error, "response", None), "status_code", None),
    ):
        try:
            return int(value)
        except (TypeError, ValueError):
            continue
    return None


def _is_transient(error: Exception, status_code: int | None) -> bool:
    """Return whether an API error is likely to succeed on a retry."""
    if status_code in RETRYABLE_STATUS_CODES:
        return True
    name = type(error).__name__.lower()
    return any(part in name for part in ("timeout", "connect", "network", "transport"))


def _friendly_error(error: Exception, status_code: int | None) -> ChatError:
    """Convert provider and network errors into safe, actionable messages."""
    if status_code == 429:
        return ChatError("Gemini is receiving too many requests. Wait a moment and try again.")
    if status_code in {401, 403}:
        return ChatError("Gemini rejected the request. Check your API key and model access.")
    if status_code is not None and status_code < 500:
        return ChatError("Gemini could not process that request. Check the model settings and try again.")
    if _is_transient(error, status_code):
        return ChatError("Gemini is temporarily unavailable. Please try again shortly.")
    return ChatError("Couldn't reach Gemini. Check your connection and API settings, then try again.")


@dataclass
class ChatSession:
    system: str = DEFAULT_SYSTEM
    model: str = field(default_factory=lambda: os.getenv("MODEL", "gemini-3.8-flash"))
    max_tokens: int = 1024
    temperature: float = 0.7
    history_budget: int = 6000
    messages: list = field(default_factory=list)
    _client: object = None

    def _get_client(self):
        if self._client is None:
            from google import genai

            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ChatError("Set GEMINI_API_KEY in your local .env file to use Gemini.")
            self._client = genai.Client(api_key=api_key)
        return self._client

    def send(self, user_text: str) -> str:
        if not isinstance(user_text, str):
            raise ValueError("Message must be text.")
        user_text = user_text.strip()
        if not user_text:
            raise ValueError("Message is empty.")
        previous_length = len(self.messages)
        self.messages.append({"role": "user", "content": user_text})
        window = trim_history(self.messages, self.history_budget)
        contents = [
            {
                "role": "model" if message["role"] == "assistant" else message["role"],
                "parts": [{"text": message["content"]}],
            }
            for message in window
        ]
        try:
            client = self._get_client()
            for attempt in range(MAX_API_ATTEMPTS):
                try:
                    response = client.models.generate_content(
                        model=self.model,
                        contents=contents,
                        config={
                            "system_instruction": self.system,
                            "max_output_tokens": self.max_tokens,
                            "temperature": self.temperature,
                        },
                    )
                    reply = response.text or ""
                    break
                except Exception as error:
                    status_code = _status_code(error)
                    if not _is_transient(error, status_code) or attempt + 1 == MAX_API_ATTEMPTS:
                        raise _friendly_error(error, status_code) from None
                    time.sleep(RETRY_DELAYS_SECONDS[attempt])
        except ChatError:
            del self.messages[previous_length:]
            raise
        except Exception as error:
            del self.messages[previous_length:]
            raise _friendly_error(error, _status_code(error)) from None
        self.messages.append({"role": "assistant", "content": reply})
        return reply

    def stream(self, user_text: str) -> Iterator[str]:
        """Yield reply text as Gemini generates it, then store the full turn."""
        if not isinstance(user_text, str):
            raise ValueError("Message must be text.")
        user_text = user_text.strip()
        if not user_text:
            raise ValueError("Message is empty.")

        previous_length = len(self.messages)
        self.messages.append({"role": "user", "content": user_text})
        window = trim_history(self.messages, self.history_budget)
        contents = [
            {
                "role": "model" if message["role"] == "assistant" else message["role"],
                "parts": [{"text": message["content"]}],
            }
            for message in window
        ]
        request = {
            "model": self.model,
            "contents": contents,
            "config": {
                "system_instruction": self.system,
                "max_output_tokens": self.max_tokens,
                "temperature": self.temperature,
            },
        }
        output_parts = []
        try:
            client = self._get_client()
            for attempt in range(MAX_API_ATTEMPTS):
                try:
                    for chunk in client.models.generate_content_stream(**request):
                        part = chunk.text or ""
                        if part:
                            output_parts.append(part)
                            yield part
                    break
                except Exception as error:
                    status_code = _status_code(error)
                    if (
                        output_parts
                        or not _is_transient(error, status_code)
                        or attempt + 1 == MAX_API_ATTEMPTS
                    ):
                        raise _friendly_error(error, status_code) from None
                    time.sleep(RETRY_DELAYS_SECONDS[attempt])
        except ChatError:
            del self.messages[previous_length:]
            raise
        except GeneratorExit:
            del self.messages[previous_length:]
            raise
        except Exception as error:
            del self.messages[previous_length:]
            raise _friendly_error(error, _status_code(error)) from None
        self.messages.append({"role": "assistant", "content": "".join(output_parts)})

    def save(self, path: str | Path) -> None:
        """Save conversation settings and messages as local JSON."""
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "version": 1,
            "system": self.system,
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "history_budget": self.history_budget,
            "messages": self.messages,
        }
        temporary_path = destination.with_suffix(destination.suffix + ".tmp")
        temporary_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        temporary_path.replace(destination)

    @classmethod
    def load(cls, path: str | Path) -> "ChatSession":
        """Load and validate a locally saved conversation."""
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        messages = payload.get("messages") if isinstance(payload, dict) else None
        if (
            not isinstance(payload, dict)
            or payload.get("version") != 1
            or not isinstance(messages, list)
        ):
            raise ValueError("Chat file has an unsupported format.")
        if any(
            not isinstance(message, dict)
            or message.get("role") not in {"user", "assistant"}
            or not isinstance(message.get("content"), str)
            for message in messages
        ):
            raise ValueError("Chat file contains invalid messages.")
        return cls(
            system=str(payload.get("system", DEFAULT_SYSTEM)),
            model=str(payload.get("model", "gemini-3.8-flash")),
            max_tokens=int(payload.get("max_tokens", 1024)),
            temperature=float(payload.get("temperature", 0.7)),
            history_budget=int(payload.get("history_budget", 6000)),
            messages=messages,
        )

    def clear(self) -> None:
        self.messages.clear()


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    s = ChatSession()
    print(s.send("In one sentence, what is a context window?"))
