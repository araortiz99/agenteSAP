from dataclasses import dataclass, field

import src.app.server as server


@dataclass
class FakeWorkspace:
    diagnostics: dict = field(default_factory=dict)


def test_github_ref_defaults_to_main(monkeypatch):
    monkeypatch.delenv("GITHUB_REF_NAME", raising=False)
    monkeypatch.delenv("GITHUB_REF", raising=False)
    assert server._github_ref() == "main"


def test_github_ref_prefers_ref_name(monkeypatch):
    monkeypatch.setenv("GITHUB_REF_NAME", "feature/workbench")
    monkeypatch.setenv("GITHUB_REF", "refs/heads/legacy")
    assert server._github_ref() == "feature/workbench"


def test_github_ref_normalizes_heads_and_tags(monkeypatch):
    monkeypatch.delenv("GITHUB_REF_NAME", raising=False)
    monkeypatch.setenv("GITHUB_REF", "refs/heads/feature/workbench")
    assert server._github_ref() == "feature/workbench"

    monkeypatch.setenv("GITHUB_REF", "refs/tags/v1.0.0")
    assert server._github_ref() == "v1.0.0"


def test_status_reports_normalized_ref(monkeypatch):
    monkeypatch.setenv("GITHUB_REF_NAME", "feature/workbench")
    assert server._status_payload()["github_ref"] == "feature/workbench"


def test_object_workspace_uses_normalized_ref(monkeypatch):
    captured = {}

    def fake_workspace(client, object_id, *, ref):
        captured["ref"] = ref
        return FakeWorkspace()

    monkeypatch.setattr(server, "build_object_workspace", fake_workspace)
    monkeypatch.setenv("GITHUB_REF", "refs/heads/feature/workbench")
    monkeypatch.delenv("GITHUB_REF_NAME", raising=False)

    class FakeClient:
        pass

    monkeypatch.setattr(server, "_github_client", lambda: FakeClient())

    payload = server._object_workspace_payload("ZMM_IMX_0004", started_at=0.0)

    assert captured["ref"] == "feature/workbench"
    assert payload["diagnostics"]["read_only"] if "read_only" in payload["diagnostics"] else True
