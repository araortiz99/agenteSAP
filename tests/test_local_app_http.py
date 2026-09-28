from dataclasses import dataclass
import json
import threading
import urllib.request
import urllib.error

from src.app.server import AgentRequestHandler, ThreadingHTTPServer, _response_payload


@dataclass(frozen=True)
class FakeResponse:
    result: str


def test_local_app_http_health_and_consult(monkeypatch):
    import src.app.server as server

    monkeypatch.setattr(server, "run_agent", lambda *args, **kwargs: FakeResponse("ok"))

    httpd = ThreadingHTTPServer(("127.0.0.1", 0), AgentRequestHandler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        url = f"http://127.0.0.1:{httpd.server_port}"
        with urllib.request.urlopen(url + "/health", timeout=2) as response:
            assert json.loads(response.read()) == {
                "status": "ok",
                "mode": "local-read-only",
                "sap_writes_exposed": False,
            }

        with urllib.request.urlopen(url + "/api/status", timeout=2) as response:
            status = json.loads(response.read())
            assert status["agent"] == "ready"
            assert status["sap_writes_exposed"] is False
            assert status["qas_runtime_enabled"] is False
            assert "openai_api_key_configured" in status
            assert "github_token_configured" in status

        payload = json.dumps({"request": "test"}).encode()
        request = urllib.request.Request(
            url + "/api/consult",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=2) as response:
            payload = json.loads(response.read())
            assert payload["result"]["result"] == "ok"
            assert payload["request_id"].startswith("REQ-")
            assert payload["intent"] == "unknown"
            assert payload["diagnostics"]["trace_id"] is None
            assert payload["runtime"]["writes_exposed"] is False

        oversized_results = json.dumps({"request": "test", "max_results": 21}).encode()
        request = urllib.request.Request(
            url + "/api/consult",
            data=oversized_results,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            urllib.request.urlopen(request, timeout=2)
        except urllib.error.HTTPError as exc:
            assert exc.code == 400
            assert "max_results must be between 1 and 20" in exc.read().decode()
        else:
            raise AssertionError("max_results upper bound was not enforced")
    finally:
        httpd.shutdown()
        thread.join(timeout=2)
        httpd.server_close()
