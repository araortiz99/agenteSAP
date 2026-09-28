import json

import pytest

from src.llm.client import LLMConfigurationError, OpenAIResponsesClient


class FakeResponse:
    def __init__(self, payload):
        self.payload = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return self.payload


def test_openai_client_requires_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    client = OpenAIResponsesClient(model="test-model")

    with pytest.raises(LLMConfigurationError):
        client.generate(system_prompt="system", user_prompt="user")


def test_openai_client_from_env_requires_api_key_only(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_MODEL", raising=False)

    with pytest.raises(LLMConfigurationError, match="OPENAI_API_KEY"):
        OpenAIResponsesClient.from_env()


def test_openai_client_from_env_uses_default_model(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-only-key")
    monkeypatch.delenv("OPENAI_MODEL", raising=False)

    client = OpenAIResponsesClient.from_env()

    assert client.model == "gpt-5.6"
    assert client.api_key == "test-only-key"


def test_openai_client_from_env_reads_custom_model(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-only-key")
    monkeypatch.setenv("OPENAI_MODEL", "test-model")

    client = OpenAIResponsesClient.from_env()

    assert client.model == "test-model"
    assert client.api_key == "test-only-key"


def test_openai_client_parses_output_text(monkeypatch):
    captured = {}

    def fake_urlopen(request, timeout):
        captured["body"] = json.loads(request.data.decode("utf-8"))
        captured["authorization"] = request.headers["Authorization"]
        captured["timeout"] = timeout
        return FakeResponse({"output_text": "respuesta"})

    monkeypatch.setenv("OPENAI_API_KEY", "test-only-key")
    monkeypatch.setattr("src.llm.client.urlopen", fake_urlopen)

    client = OpenAIResponsesClient(model="test-model", timeout_seconds=12)
    result = client.generate(system_prompt="system", user_prompt="user")

    assert result == "respuesta"
    assert captured["authorization"] == "Bearer test-only-key"
    assert captured["body"]["model"] == "test-model"
    assert captured["body"]["input"][0]["role"] == "system"
    assert captured["body"]["input"][1]["role"] == "user"
    assert captured["timeout"] == 12
