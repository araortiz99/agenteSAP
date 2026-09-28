"""Provider-neutral LLM client with an OpenAI Responses API implementation."""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from typing import Protocol
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class LLMError(RuntimeError):
    """Base error for LLM integration failures."""


class LLMConfigurationError(LLMError):
    """Raised when required provider configuration is missing."""


class LLMResponseError(LLMError):
    """Raised when the provider response cannot be used safely."""


class LLMClient(Protocol):
    def generate(self, *, system_prompt: str, user_prompt: str) -> str:
        """Generate text from the supplied bounded context."""


@dataclass(frozen=True)
class OpenAIResponsesClient:
    """Minimal HTTP client for the OpenAI Responses API.

    Credentials are read at runtime and are never stored in the repository.
    """

    model: str = "gpt-5.6"
    api_key: str | None = None
    base_url: str = "https://api.openai.com/v1/responses"
    timeout_seconds: float = 60.0

    def generate(self, *, system_prompt: str, user_prompt: str) -> str:
        api_key = self.api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise LLMConfigurationError("OPENAI_API_KEY is not configured")
        if not system_prompt.strip() or not user_prompt.strip():
            raise ValueError("prompts must not be empty")

        payload = {
            "model": self.model,
            "input": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
        request = Request(
            self.base_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                raw = response.read().decode("utf-8")
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise LLMResponseError(
                f"LLM provider returned HTTP {exc.code}: {detail[:500]}"
            ) from exc
        except URLError as exc:
            raise LLMResponseError(f"LLM provider request failed: {exc.reason}") from exc

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise LLMResponseError("LLM provider returned invalid JSON") from exc

        text = data.get("output_text")
        if isinstance(text, str) and text.strip():
            return text.strip()

        output = data.get("output", [])
        parts: list[str] = []
        if isinstance(output, list):
            for item in output:
                if not isinstance(item, dict):
                    continue
                for content in item.get("content", []):
                    if isinstance(content, dict) and content.get("type") == "output_text":
                        value = content.get("text")
                        if isinstance(value, str):
                            parts.append(value)
        result = "\n".join(parts).strip()
        if not result:
            raise LLMResponseError("LLM response contained no usable text")
        return result
