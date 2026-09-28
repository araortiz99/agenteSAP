# MVP 5 — Knowledge Intelligence Benchmark

## Purpose

Validate deterministic entity resolution, explicit relationship traversal, bounded multi-hop retrieval and provenance preservation.

## Canonical cases

| ID | Case | Expected |
|---|---|---|
| KI-01 | Entity resolution | Canonical SAP object resolved from metadata |
| KI-02 | Direct relationship | Explicit relationship is returned |
| KI-03 | Multi-hop | Related evidence is discovered within configured hop limit |
| KI-04 | No false relationship | Co-occurrence alone creates no relationship |
| KI-05 | Provenance | path/source_layer/source_id/certainty survive traversal |
| KI-06 | Hop limit | Traversal stops at configured maximum |
| KI-07 | Deduplication | Same evidence path appears once |
| KI-08 | Context rendering | Structured context exposes entities, relationships and evidence |

## Negative cases

### KI-N01 — Textual co-occurrence

Input contains two SAP identifiers in one document without a relationship document.

Expected: no relationship is created.

### KI-N02 — Certainty escalation

A related document has certainty: partial.

Expected: context preserves partial.

### KI-N03 — Hop overflow

A third-hop relationship exists.

Expected: with max_hops=2, third-hop data is not traversed.

### KI-N04 — Unknown entity

Query does not map to metadata-backed entity.

Expected: no fabricated entity is returned.

## Closure criteria

All canonical and negative cases must pass. MVP 4.2 regression tests must remain green.


## Ejecutabilidad

Los casos KI-N01 a KI-N04 se materializan en `tests/test_knowledge_intelligence.py`.
El benchmark de MVP 5 debe considerarse válido únicamente si la suite local y el CI coinciden.
