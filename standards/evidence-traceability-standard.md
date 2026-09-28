# Evidence Traceability Standard

## Purpose

Define how agenteSAP preserves the provenance of evidence used during retrieval and reasoning.

## Evidence identity

Each evidence item must have a deterministic identifier:

`EVD-<12 uppercase hexadecimal characters>`

The identifier is derived from provenance attributes and must not depend on retrieval order.

## Required trace attributes

An evidence trace should preserve:

- evidence_id;
- path;
- source_layer;
- source_id;
- knowledge_type;
- knowledge_scope;
- certainty;
- weight;
- role;
- reason.

## Roles

- `supporting`: confirmed evidence that supports the bounded assessment;
- `unresolved`: partial or under-validation evidence;
- `non_supporting`: inferred, not confirmed or unknown evidence.

## Trace report

A trace report identifies:

- trace_id;
- query;
- conclusion_status;
- conclusion;
- evidence items;
- supporting evidence IDs;
- unresolved evidence IDs;
- gaps;
- conflicts.

## Rules

1. Evidence IDs must be stable for the same provenance.
2. Retrieval order must not affect Evidence IDs.
3. Every relevant conclusion must be traceable to evidence.
4. A source ID is not a substitute for the document path.
5. SAP Standard and internal evidence must retain separate source layers.
6. Missing evidence must be reported rather than invented.
7. Traceability does not convert inference into confirmed knowledge.
8. A trace report is an audit artifact; it does not itself prove functional correctness.

## LLM boundary

A future LLM may receive a trace report as structured context. The LLM must not remove provenance, change certainty, or promote unsupported evidence without an explicit validation step.
