from src.tools.source_selection import select_evidence_sources


def test_generic_query_requests_standard_and_internal():
    selection = select_evidence_sources("¿Cómo funciona el inventario de materiales?")
    assert selection.requested == ("sap_standard", "internal")


def test_runtime_query_requires_runtime():
    selection = select_evidence_sources("¿Qué está configurado actualmente en QAS para MM?")
    assert "runtime" in selection.requested


def test_standard_internal_comparison_selects_both():
    selection = select_evidence_sources("Compará SAP Standard con nuestra implementación")
    assert selection.requested == ("sap_standard", "internal")


def test_empty_query_rejected():
    try:
        select_evidence_sources("")
    except ValueError:
        pass
    else:
        raise AssertionError("empty query must be rejected")


def test_generic_sap_phrase_does_not_require_runtime():
    selection = select_evidence_sources("¿Cómo funciona el stock en SAP?")
    assert "runtime" not in selection.requested


def test_current_configuration_still_requires_runtime():
    selection = select_evidence_sources("¿Qué configuración tiene SAP actualmente en QAS?")
    assert selection.requested == ("runtime",)
