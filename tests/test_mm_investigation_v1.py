import re

import pytest

from src.agent.consultant import consult
from src.agent.investigation import investigate


class InvestigationFixtureClient:
    def __init__(self):
        self.files = {
            "knowledge/sap-standard/mm/investigation.md": """---
source_id: SAP-MM-INVESTIGATION-TEST
knowledge_type: standard
knowledge_scope: global
certainty: confirmed
---
# SAP MM Standard Investigation
Movimiento 551 y movimiento 552 son movimientos de inventario.
El purchase order, goods receipt, material document y accounting document
forman conceptos relacionados pero distintos.
MIRO pertenece a Logistics Invoice Verification.
GR/IR y account determination son conceptos estándar de integración contable.
Material document es documento logístico; accounting document es documento contable.
""",
            "knowledge/sap-objects/zmm-im-0002.md": """---
object_id: ZMM_IM_0002
knowledge_type: custom
knowledge_scope: organization
certainty: confirmed
---
# ZMM_IM_0002
Custom implementation for inventory adjustment. It is not SAP Standard.
""",
            "knowledge/processes/inventory-custom.md": """---
process_id: PROC-MM-INV
knowledge_type: custom
knowledge_scope: process
certainty: partial
---
# Custom inventory process
The customer implementation uses ZMM_IM_0002 for a local inventory process.
""",
            "knowledge/entities/purchase-order.md": """---
process_id: PURCHASE_ORDER
knowledge_type: standard
knowledge_scope: global
certainty: confirmed
---
# Purchase Order
Standard purchase order entity.
""",
            "knowledge/entities/goods-receipt.md": """---
process_id: GOODS_RECEIPT
knowledge_type: standard
knowledge_scope: global
certainty: confirmed
---
# Goods Receipt
Standard goods receipt entity.
""",
            "knowledge/entities/material-document.md": """---
object_id: MATERIAL_DOCUMENT
knowledge_type: standard
knowledge_scope: global
certainty: confirmed
---
# Material Document
Standard material document entity.
""",
            "knowledge/entities/accounting-document.md": """---
object_id: ACCOUNTING_DOCUMENT
knowledge_type: standard
knowledge_scope: global
certainty: confirmed
---
# Accounting Document
Standard accounting document entity.
""",
            "knowledge/relationships/po-gr.md": """---
relationship_id: REL-MM-001
source_id: PURCHASE_ORDER
source_type: PROCESS
relation_type: precede
target_id: GOODS_RECEIPT
target_type: PROCESS
knowledge_type: standard
knowledge_scope: global
certainty: confirmed
status: confirmed
evidence_source_id: SAP-MM-INVESTIGATION-TEST
---
# Relationship
Purchase order precedes goods receipt in the documented flow.
""",
            "knowledge/relationships/gr-material.md": """---
relationship_id: REL-MM-002
source_id: GOODS_RECEIPT
source_type: PROCESS
relation_type: genera
target_id: MATERIAL_DOCUMENT
target_type: SAP_OBJECT
knowledge_type: standard
knowledge_scope: global
certainty: confirmed
status: confirmed
evidence_source_id: SAP-MM-INVESTIGATION-TEST
---
# Relationship
Goods receipt generates a material document.
""",
            "knowledge/relationships/material-accounting.md": """---
relationship_id: REL-MM-003
source_id: MATERIAL_DOCUMENT
source_type: SAP_OBJECT
relation_type: genera
target_id: ACCOUNTING_DOCUMENT
target_type: SAP_OBJECT
knowledge_type: standard
knowledge_scope: global
certainty: partial
status: candidate
evidence_source_id: SAP-MM-INVESTIGATION-TEST
---
# Relationship
The documented scenario links material and accounting documents.
""",
        }

    def get_tree(self, ref="main"):
        return [{"path": path, "type": "blob"} for path in self.files]

    def get_file(self, path, ref="main"):
        return self.files[path]


class ContractLLM:
    model = "benchmark-test-model"

    def generate(self, *, system_prompt, user_prompt):
        ids = re.findall(r"EVD-[A-Z0-9]+", user_prompt)
        citation = f"[{ids[0]}]" if ids else "No evidence ID available."
        return (
            "## Resumen\n"
            f"Resultado acotado al contexto recuperado {citation}.\n\n"
            "## Qué está confirmado\n"
            f"Solo lo respaldado por la evidencia recuperada {citation}.\n\n"
            "## Qué corresponde a nuestra implementación\n"
            f"Solo elementos identificados como custom/internal {citation}.\n\n"
            "## Qué no está confirmado\n"
            "No se asumen configuración ni estado runtime sin evidencia.\n\n"
            "## Evidencias\n"
            f"{citation}\n\n"
            "## Ticket\n"
            "No aplica.\n\n"
            "## Próximos pasos\n"
            "Validar los gaps indicados por el pipeline."
        )


CASES = (
    ("MM-001", "¿Qué significa el movimiento 551?", "factual"),
    ("MM-002", "¿Cuál es la diferencia entre movimiento 551 y 552?", "comparison"),
    ("MM-003", "¿Qué es un goods receipt contra un purchase order?", "factual"),
    ("MM-004", "¿Cuál es la diferencia entre material document y accounting document?", "comparison"),
    ("MM-005", "¿Qué es MIRO e Invoice Verification?", "factual"),
    ("MM-006", "¿Qué es GR/IR en SAP MM?", "factual"),
    ("MM-007", "¿Cómo funciona account determination en MM?", "configuration"),
    ("MM-008", "Compará SAP Standard con la implementación ZMM_IM_0002.", "standard_vs_custom"),
    ("MM-009", "¿Cómo se relacionan purchase order, goods receipt, material document y accounting document?", "multi_hop"),
    ("MM-010", "¿Por qué falla actualmente en QAS el proceso de inventario?", "troubleshooting"),
)


@pytest.mark.parametrize("case_id,query,expected_intent", CASES, ids=[x[0] for x in CASES])
def test_mm_investigation_cases_are_executable(case_id, query, expected_intent):
    client = InvestigationFixtureClient()
    result = investigate(
        client,
        query,
        max_steps=4,
        max_results=8,
        max_hops=2,
    )

    assert result.plan.intent == expected_intent
    assert result.plan.subqueries
    assert len(result.plan.subqueries) <= 4
    assert result.retrieval.query == query
    assert result.evidence.query == query
    assert result.reasoning.query == query
    assert result.knowledge_context.query == query

    if case_id == "MM-010":
        assert any("runtime" in gap.lower() for gap in result.evidence.gaps)

    if case_id == "MM-008":
        assert any(item.source_layer == "sap_standard" for item in result.retrieval.results)
        assert any(item.source_layer == "internal" for item in result.retrieval.results)

    if case_id == "MM-009":
        assert result.knowledge_context.relationships
        assert all(item.hop <= 2 for item in result.knowledge_context.relationships)


@pytest.mark.parametrize("case_id,query,_expected_intent", CASES, ids=[x[0] for x in CASES])
def test_mm_investigation_cases_reach_consultant_contract(case_id, query, _expected_intent):
    client = InvestigationFixtureClient()
    result = consult(client, query, ContractLLM(), max_results=8)

    assert result.investigation is not None
    assert result.investigation.plan.subqueries
    assert result.knowledge_context is not None
    assert result.answer.startswith("## Resumen")
    assert result.answer.count("## ") == 7
    assert result.traceability.trace_id.startswith("TRACE-")

    if result.traceability.supporting_evidence_ids:
        assert result.citations
