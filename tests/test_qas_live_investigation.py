import os

import pytest

from src.github.client import GitHubClient
from src.investigation.engine import investigate


@pytest.mark.skipif(
    os.getenv("AGENTESAP_QAS_LIVE_TESTS") != "true",
    reason="real QAS tests require explicit opt-in",
)
def test_real_qas_consultative_investigation():
    question = os.getenv(
        "AGENTESAP_QAS_LIVE_INVESTIGATION_QUERY",
        "¿Por qué el material 100123 tiene stock diferente al esperado en el centro 5023?",
    )
    token = os.getenv("GITHUB_TOKEN")
    assert token, "GITHUB_TOKEN is required for Knowledge retrieval"
    client = GitHubClient(os.getenv("GITHUB_OWNER", "araortiz99"), os.getenv("GITHUB_REPO", "agenteSAP"), token=token)
    result = investigate(client, question, max_steps=5)
    assert result.stop_reason != "missing_entity"
    assert result.case_id.startswith("INV-")
    runtime = [item for item in result.evidence_collected if item.landscape == "QAS"]
    assert runtime, "real QAS investigation must collect runtime evidence"
    assert all(item.provider == "sap_mcp_server" for item in runtime)
    assert all(item.provenance for item in runtime)
    assert result.confidence in {"HIGH", "MEDIUM", "LOW"}


def test_live_investigation_requires_explicit_qas_opt_in():
    if os.getenv("AGENTESAP_QAS_LIVE_TESTS") == "true":
        pytest.skip("covered by real QAS test")
    assert os.getenv("AGENTESAP_QAS_LIVE_TESTS") != "true"
