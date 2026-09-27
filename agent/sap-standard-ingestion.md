# SAP Standard Knowledge Ingestion Contract

## Objective

Define the controlled pipeline for bringing official SAP documentation into agenteSAP.

## Pipeline

```
Official SAP documentation
        ↓
Source registration
        ↓
Retrieval
        ↓
Parsing
        ↓
Metadata
        ↓
Deduplication
        ↓
Knowledge extraction
        ↓
Validation
        ↓
knowledge/sap-standard/
        ↓
Agent retrieval
```

## MVP boundary

The MVP does not crawl SAP indiscriminately and does not treat search results as confirmed knowledge automatically.

The first implementation should support a controlled source catalog and deterministic retrieval.

## Source validation

A source must be:

- official SAP documentation;
- associated with a product/release when the source provides that context;
- traceable through a canonical URL;
- recorded with retrieval metadata.

## Promotion rule

Raw source material and reusable knowledge are conceptually different.

The ingestion process may identify candidate knowledge, but promotion to reusable knowledge requires validation against the source and the SAP Standard Knowledge Standard.

## Customer-context rule

SAP Standard Knowledge must never be used as proof of customer-specific configuration, custom development or local process behavior.

## Future stages

1. controlled manual source registration;
2. automated retrieval;
3. parsing/chunking;
4. metadata extraction;
5. deduplication;
6. semantic indexing;
7. scheduled refresh;
8. change detection.


## Candidate lifecycle

A retrieved page is initially staged as:

`status: candidate`
`certainty: under_validation`

Only after human or automated validation against the source may it be promoted to reusable Standard Knowledge with:

`status: validated`
`certainty: confirmed`

The ingestor records a SHA-256 checksum so repeated retrievals can be compared without relying on URL identity alone.

## Network safety

The collector currently permits only HTTPS URLs hosted on `help.sap.com`, applies a bounded response size, uses no credentials, and does not execute downloaded content.


## Source registry

The source registry is the allowlist for ingestion. A CLI run requires an existing `source_id`.

The registry records:

- canonical URL;
- product;
- module;
- release;
- language;
- status.

A CLI URL override is rejected when it differs from the registered URL. This prevents ingestion from silently switching to an unregistered source.

## CLI

Controlled ingestion can be invoked with:

```bash
python -m src.sap.cli --source-id SAP-HELP-S4-MM-2025-GOODS-MOVEMENT
```

The default output is `staging/sap-standard/`.

The staging output is a candidate and must not be treated as validated Knowledge automatically.
