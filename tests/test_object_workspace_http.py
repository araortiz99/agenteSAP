import json
import threading
import urllib.request

from src.app.server import AgentRequestHandler, ThreadingHTTPServer


def test_object_workspace_http_endpoint(monkeypatch):
    import src.app.server as server

    monkeypatch.setattr(
        server,
        "_object_workspace_payload",
        lambda object_id, started_at: {
            "query": object_id,
            "identity": {
                "object_id": object_id,
                "status": "resolved",
                "certainty": "confirmed",
            },
            "object": {"id": object_id, "type": "SAP_OBJECT"},
            "relationships": (),
            "dependencies": (),
            "evidence": (),
            "tickets": (),
            "runtime": {
                "status": "not_observed",
                "landscape": "QAS",
                "access": "read-only",
            },
            "gaps": (),
            "conflicts": (),
            "diagnostics": {"read_only": True},
            "overview": (),
        },
    )

    httpd = ThreadingHTTPServer(("127.0.0.1", 0), AgentRequestHandler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        url = f"http://127.0.0.1:{httpd.server_port}/api/object/ZMM_IMX_0004"
        with urllib.request.urlopen(url, timeout=2) as response:
            payload = json.loads(response.read())
        assert payload["object"]["id"] == "ZMM_IMX_0004"
        assert payload["runtime"]["access"] == "read-only"
        assert payload["diagnostics"]["read_only"] is True
    finally:
        httpd.shutdown()
        thread.join(timeout=2)
        httpd.server_close()
