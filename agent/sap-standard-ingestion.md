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
