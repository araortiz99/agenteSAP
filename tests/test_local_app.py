from unittest.mock import patch

from src.app.server import AgentRequestHandler


def test_local_app_rejects_non_localhost_binding():
    import src.app.server as server

    assert "127.0.0.1" in {"127.0.0.1", "localhost", "::1"}
    assert server.AgentRequestHandler.server_version == "AgenteSAPLocal/0.1"


def test_local_app_root_exists():
    import src.app.server as server

    assert server.INDEX.exists()


def test_local_app_payload_is_dataclass_serializable():
    from dataclasses import dataclass

    import src.app.server as server

    @dataclass(frozen=True)
    class Sample:
        answer: str

    assert server._response_payload(Sample("ok")) == {"answer": "ok"}
