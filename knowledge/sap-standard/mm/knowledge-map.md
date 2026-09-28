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

# SAP MM Knowledge Map

## Purpose

Define the controlled coverage map for SAP S/4HANA Materials Management knowledge in AgenteSAP.

This file is a navigation contract. It does not establish customer-specific configuration, Z developments, organizational rules, or runtime state.

## Domains

| Domain | Standard topics | Evidence boundary |
|---|---|---|
| Material/Product Master | product/material master, organizational views, units | SAP Standard only |
| Procurement | purchasing documents, source determination, purchasing processes | SAP Standard only |
| Inventory Management | stock, goods movements, physical inventory, transfer postings | SAP Standard only |
| Invoice Verification | logistics invoice verification, invoice documents, matching concepts | SAP Standard only |
| Valuation | valuation concepts, material valuation, account determination concepts | SAP Standard only |
| Physical Inventory | inventory procedures, count/recount concepts, differences | SAP Standard only |

## Retrieval rule

A query about a generic SAP MM concept should prefer this Standard layer.

A query about a customer-specific transaction, Z object, local business rule, ticket, configuration, or current SAP state must not be answered from this map alone.

## Evidence boundary

This map does not imply that:

- a transaction exists in a customer system;
- a movement type is configured or used by a customer;
- an organizational assignment exists;
- a Z object follows SAP Standard behavior;
- a runtime value is current;
- a documented Standard capability is enabled in a particular system.

Those claims require the corresponding Internal or Runtime evidence layer.
