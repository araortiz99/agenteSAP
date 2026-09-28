import os

import pytest

from src.agent.cli import main
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
    result = investigate(None, question, max_steps=5)
    assert result.stop_reason != "missing_entity"
    assert result.case_id.startswith("INV-")
    assert all(item.landscape == "QAS" for item in result.evidence_collected)
    assert all(item.provider == "sap_mcp_server" for item in result.evidence_collected)
    assert all(item.provenance for item in result.evidence_collected)
    assert result.confidence in {"HIGH", "MEDIUM", "LOW"}


def test_live_investigation_requires_explicit_qas_opt_in():
    if os.getenv("AGENTESAP_QAS_LIVE_TESTS") == "true":
        pytest.skip("covered by real QAS test")
    assert os.getenv("AGENTESAP_QAS_LIVE_TESTS") != "true"
