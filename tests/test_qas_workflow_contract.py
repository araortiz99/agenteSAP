from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
QAS_WORKFLOW = REPO_ROOT / '.github' / 'workflows' / 'qas-live.yml'


def test_qas_workflow_has_no_guessed_runtime_tool_fallbacks():
    workflow = QAS_WORKFLOW.read_text(encoding='utf-8')
    assert 'sap_list_destinations' not in workflow
    assert 'SID_QAS' not in workflow
    assert 'vars.AGENTESAP_SAP_RUNTIME_READ_TOOLS ||' not in workflow
    assert 'vars.AGENTESAP_SAP_RUNTIME_QUERY_TOOL ||' not in workflow


def test_qas_workflow_requires_environment_supplied_runtime_configuration():
    workflow = QAS_WORKFLOW.read_text(encoding='utf-8')
    assert 'environment: qas' in workflow
    assert 'AGENTESAP_SAP_RUNTIME_SYSTEM: ' + '${{' + ' vars.AGENTESAP_SAP_RUNTIME_SYSTEM }}' in workflow
    assert 'AGENTESAP_SAP_RUNTIME_READ_TOOLS: ' + '${{' + ' vars.AGENTESAP_SAP_RUNTIME_READ_TOOLS }}' in workflow
    assert 'AGENTESAP_SAP_RUNTIME_QUERY_TOOL: ' + '${{' + ' vars.AGENTESAP_SAP_RUNTIME_QUERY_TOOL }}' in workflow
    assert 'AGENTESAP_SAP_RUNTIME_QUERY_ARGUMENT: ' + '${{' + ' vars.AGENTESAP_SAP_RUNTIME_QUERY_ARGUMENT }}' in workflow


def test_qas_workflow_keeps_catalog_verification_before_live_query():
    workflow = QAS_WORKFLOW.read_text(encoding='utf-8')
    discovery = workflow.index('name: Verify configured QAS MCP catalog')
    smoke = workflow.index('name: Run real QAS read-only smoke test')
    assert discovery < smoke
