# SAP MM Investigation Foundation v1

## Current architecture assessment

The repository already contains the principal building blocks required for
the first investigation loop:

- deterministic Agent Router and intent routing;
- SAP Standard retrieval;
- internal knowledge retrieval;
- source selection;
- evidence evaluation and provenance;
- entity resolution;
- explicit relationship traversal;
- bounded Knowledge Intelligence / multi-hop context;
- LLM consultant and semantic/structural gates;
- QAS runtime controls and read-only tests;
- Workbench contracts.

Therefore this phase does not introduce duplicate evidence, relationship,
or QAS layers.

## Foundation flow

The target composition is:

USER QUERY
→ INTENT
→ ENTITY RESOLUTION
→ QUERY PLANNING
→ SOURCE SELECTION
→ SAP STANDARD / INTERNAL / QAS
→ RELATIONSHIPS
→ EVIDENCE
→ BOUNDED REASONING
→ LLM CONSULTANT
→ GATES
→ TRACEABLE ANSWER

## Query planner boundary

src/tools/query_planner.py is deterministic and bounded.

It creates retrieval hypotheses only. It does not:

- retrieve evidence;
- assert functional conclusions;
- mutate SAP;
- promote knowledge;
- bypass source policy.

## Knowledge Graph boundary

The current repository relationship model is the initial Knowledge Graph
foundation. Relationships are explicit Markdown records under
knowledge/relationships/, with typed source/target entities, relation type,
certainty, status and evidence provenance.

The graph must not infer relationships merely because two objects co-occur
in a document.

## Source separation

The investigation pipeline must preserve:

- SAP_STANDARD
- INTERNAL_KNOWLEDGE
- RUNTIME_EVIDENCE
- USER_CONTEXT

Customer Z objects, tickets and local process rules must not be silently
reclassified as SAP Standard.

## Read-only boundary

QAS remains:

- opt-in;
- allowlisted;
- auditable;
- fail-closed;
- read-only.

No write operation is introduced by this foundation.

## Definition of done

- architecture is mapped;
- query planner is bounded and tested;
- SAP Help source metadata is version-aware;
- Standard/Internal separation is tested;
- relationship traversal remains explicit;
- multi-hop limits remain enforced;
- benchmark contract exists;
- regression suite passes.
