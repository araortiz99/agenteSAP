# SAP MM Investigation v1 Benchmark

## Purpose

First reproducible benchmark for the SAP MM Investigation Foundation.

The benchmark evaluates the investigation contract, not only whether the
agent can produce a fluent answer.

## Evidence layers

Every case must distinguish:

- SAP_STANDARD
- INTERNAL_KNOWLEDGE
- RUNTIME_EVIDENCE
- USER_CONTEXT

A generated query plan is a retrieval hypothesis, never evidence.

## Cases

| ID | Investigation | Intent | Primary entities | Required distinction |
|---|---|---|---|---|
| MM-001 | Movimiento 551 | factual | MOVEMENT_TYPE | Standard semantics vs customer usage |
| MM-002 | 551 vs 552 | comparison | MOVEMENT_TYPE | Standard difference; no inferred customer config |
| MM-003 | Goods Receipt contra Purchase Order | factual | PURCHASE_ORDER, GOODS_RECEIPT, MATERIAL_DOCUMENT | Standard document flow |
| MM-004 | Material Document vs Accounting Document | comparison | MATERIAL_DOCUMENT, ACCOUNTING_DOCUMENT | Distinguish logistics vs accounting evidence |
| MM-005 | MIRO / Invoice Verification | factual | TRANSACTION, INVOICE, ACCOUNTING_DOCUMENT | Standard MM-IV scope |
| MM-006 | GR/IR | conceptual | CONFIGURATION_CONCEPT, ACCOUNTING_DOCUMENT | Standard accounting concept |
| MM-007 | Account Determination | configuration | CONFIGURATION_CONCEPT | Explain concept; runtime config requires QAS |
| MM-008 | SAP Standard vs Z implementation | standard_vs_custom | SAP_OBJECT, PROCESS | Never classify Z behavior as standard |
| MM-009 | PO → GR → material document → accounting document | multi_hop | PURCHASE_ORDER, GOODS_RECEIPT, MATERIAL_DOCUMENT, ACCOUNTING_DOCUMENT | Bounded relationship traversal |
| MM-010 | Incident with missing runtime evidence | troubleshooting | PROCESS, SAP_OBJECT, RUNTIME_EVIDENCE | Separate facts, hypotheses and missing information |

## Case contract

Each implementation should record:

- question
- intent
- entities
- expected_sources
- expected_relationships
- expected_evidence
- acceptable_answer
- forbidden_claims

## Acceptance principles

1. A Standard answer must cite or preserve SAP Standard provenance.
2. A Z/custom object must remain in the internal layer unless official SAP
   evidence explicitly establishes otherwise.
3. Runtime claims require runtime evidence.
4. Missing evidence must be reported rather than fabricated.
5. Multi-hop traversal must remain bounded.
6. Query-plan subqueries must never be promoted to evidence.

## Current phase

This file defines the benchmark contract. Passing all ten cases end-to-end
is a later milestone after the investigation pipeline is fully integrated.
