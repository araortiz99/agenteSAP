import json
from dataclasses import dataclass

from src.agent import cli


def test_cli_json_output(monkeypatch, capsys):
    class FakeClient:
        pass

    @dataclass
    class FakeResult:
        answer: str = "respuesta"

    @dataclass
    class FakeResponse:
        request: str
        result: FakeResult

    monkeypatch.setenv("GITHUB_TOKEN", "test-token")
    monkeypatch.setattr(
        cli,
        "GitHubClient",
        lambda owner, repo, token=None: FakeClient(),
    )
    monkeypatch.setattr(
        cli,
        "run_agent",
        lambda client, request, ref: FakeResponse(request=request, result=FakeResult()),
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "cli.py",
            "--ref",
            "feature/agent-mvp-search",
            "--json",
            "Consultá el ticket 31426",
        ],
    )

    assert cli.main() == 0

    output = capsys.readouterr().out
    payload = json.loads(output)

    assert payload["request"] == "Consultá el ticket 31426"
    assert payload["result"]["answer"] == "respuesta"
