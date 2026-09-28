# SAP Standard Knowledge Standard

## Purpose

Define how official SAP documentation is incorporated into agenteSAP as reusable Standard Knowledge.

## Scope

This standard applies to content whose source is official SAP documentation.

The repository must keep SAP Standard Knowledge separate from organization-specific knowledge.

## Required metadata

Each SAP Standard Knowledge item should identify:

- `knowledge_type`: `standard`
- `knowledge_scope`
- `source_id`
- `source_type`: `sap_documentation`
- `product`
- `module`, when applicable
- `release`, when applicable
- `language`
- `source_url`
- `retrieved_at`
- `certainty`

## Evidence rule

Official SAP documentation supports statements about SAP-provided functionality. It does not by itself prove that a customer system is configured or implemented that way.

Therefore:

SAP documentation -> SAP Standard Knowledge

SAP documentation + customer evidence -> potentially Mixed Knowledge

Customer observation alone -> not SAP Standard Knowledge.

## Release control

Release/version is part of the identity of the source context. Content must not be presented as release-independent when the source is release-specific.

## Ingestion rules

1. Prefer official SAP domains.
2. Preserve the canonical source URL.
3. Record retrieval date.
4. Avoid duplicating identical source content.
5. Preserve product, module and release context.
6. Do not convert every documentation statement into a business rule.
7. Do not infer customer configuration from SAP documentation.
8. Mark gaps and unsupported claims explicitly.

## Security

Do not ingest credentials, private customer information, tokens or secrets from any source.

## Status

This standard defines the MVP contract for SAP Standard Knowledge ingestion.
