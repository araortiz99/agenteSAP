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
    monkeypatch.setattr(cli, "GitHubClient", lambda owner, repo, token=None: FakeClient())
    monkeypatch.setattr(
        cli,
        "run_agent",
        lambda client, request, ref, ticket_id=None, max_results=8: FakeResponse(
            request=request, result=FakeResult()
        ),
    )
    monkeypatch.setattr(
        "sys.argv",
        ["cli.py", "--ref", "feature/agent-mvp-search", "--json", "Consultá el ticket 31426"],
    )
    assert cli.main() == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["request"] == "Consultá el ticket 31426"
    assert payload["result"]["answer"] == "respuesta"


def test_cli_investigate_subcommand(monkeypatch, capsys):
    @dataclass
    class FakeInvestigation:
        case_id: str = "INV-20260928-ABCD"
        intent: str = "stock_discrepancy"

        def as_dict(self):
            return {"case_id": self.case_id, "intent": self.intent}

    monkeypatch.setattr(cli, "GitHubClient", lambda owner, repo, token=None: object())
    monkeypatch.setattr(cli, "investigate", lambda *args, **kwargs: FakeInvestigation())
    monkeypatch.setattr(
        "sys.argv",
        ["cli.py", "investigate", "¿Por qué el material 100123 difiere en centro 5023?", "--json"],
    )
    assert cli.main() == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["case_id"] == "INV-20260928-ABCD"


def test_cli_investigation_parser_rejects_zero_steps(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        ["cli.py", "investigate", "material 100123 centro 5023", "--max-steps", "0"],
    )
    try:
        cli.main()
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("zero max steps must be rejected")
