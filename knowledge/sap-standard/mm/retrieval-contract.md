---
knowledge_type: standard
knowledge_scope: global
origin: sap
product: SAP S/4HANA
module: MM
release: "2025 FPS01"
language: en
certainty: confirmed
status: validated
---

# SAP MM Retrieval Contract

## Objective

Define how AgenteSAP should use SAP MM Standard Knowledge without turning generic documentation into customer-specific conclusions.

## Query classification

### Standard concept

Examples:

- what is Material/Product Master;
- what is a goods movement;
- what is Inventory Management;
- what is purchasing in SAP MM.

Expected evidence: knowledge/sap-standard/.

### Customer implementation

Examples:

- how ZMM_IM_0002 works;
- what a local movement Z88 does;
- how the SNC K1 process is implemented.

Expected evidence: Internal/Custom knowledge.

### Current state

Examples:

- what is configured in QAS;
- what values exist in a table;
- whether a runtime object currently exists.

Expected evidence: Runtime, when an approved QAS read tool is available.

### Comparison

Examples:

- compare SAP Standard with ZMM_IMX_0004;
- identify where the customer implementation differs from Standard.

Expected evidence: Standard + Internal/Custom. Runtime may be added when current state is explicitly requested.

## Gap rule

If the requested evidence layer is unavailable, report the gap.

Do not replace missing Runtime evidence with Standard documentation and do not replace missing Internal evidence with a generic SAP explanation.

## Certainty rule

Retrieval relevance does not increase factual certainty.

A highly relevant Standard document can establish a Standard concept, but it cannot establish customer configuration or runtime state.
