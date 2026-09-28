# Generation Contract

## 1. Purpose

Define the normative and operational mechanism used by agenteSAP to generate functional documentation from a user request and repository evidence.

Generation is consultative and read-only. It produces a proposed document in memory; it does not execute SAP changes or write to the repository.

## 2. Scope

The MVP covers requirement, analysis, functional-specification, functional-test and investigation. DEBUG is intentionally outside the current MVP scope.

The contract applies to documents associated with a ticket and to documents that legitimately have no ticket. It does not authorize SAP execution, repository writes, automatic Knowledge promotion, or automatic approval.

## 3. Generation Lifecycle

REQUEST → DOCUMENT TYPE IDENTIFICATION → TEMPLATE SELECTION → TICKET RESOLUTION → CONTEXT RETRIEVAL → KNOWLEDGE RETRIEVAL → SOURCE RETRIEVAL → EVIDENCE ANALYSIS → DOCUMENT GENERATION → VALIDATION → VERSIONING → TRACEABILITY → OUTPUT → KNOWLEDGE PROMOTION EVALUATION

Each stage is mandatory unless the request is explicitly out of scope.

- REQUEST: capture the user's objective and supplied context.
- DOCUMENT TYPE IDENTIFICATION: determine one supported document type; ask when ambiguous.
- TEMPLATE SELECTION: load the official template before generating.
- TICKET RESOLUTION: resolve an existing ticket when applicable; never invent one.
- CONTEXT RETRIEVAL: retrieve ticket documents and available chronology, decisions, validations and pending items.
- KNOWLEDGE RETRIEVAL: retrieve explicit reusable knowledge and relationships.
- SOURCE RETRIEVAL: identify sources supporting relevant statements.
- EVIDENCE ANALYSIS: separate facts, evidence, hypotheses, inference and gaps.
- DOCUMENT GENERATION: populate the template without inventing unavailable information.
- VALIDATION: validate structure, content, evidence, classification, security and version.
- VERSIONING: determine the appropriate document version from the existing state and change.
- TRACEABILITY: preserve ticket, source, Knowledge and related-document references.
- OUTPUT: return the complete proposed document and its validation state.
- KNOWLEDGE PROMOTION EVALUATION: identify candidate reusable Knowledge separately; never promote automatically.

## 4. Document Type Identification

| User intent | document_type |
|---|---|
| Need, problem, business need, acceptance criteria | requirement |
| Functional assessment, evidence-based diagnosis, analysis | analysis |
| Functional test plan/results | functional-test |
| Research/question investigation | investigation |
| Functional solution definition | functional-specification |

DEBUG is not supported by the current MVP. If requested, the agent must state that the current generation capability does not materialize DEBUG documents rather than silently choosing another type.

If the intention is ambiguous, the agent asks for clarification instead of selecting arbitrarily.

## 5. Template Selection

| document_type | Template |
|---|---|
| requirement | templates/requirement.md |
| analysis | templates/analysis.md |
| functional-specification | templates/functional-specification.md |
| functional-test | templates/functional-tests.md |
| investigation | templates/investigation.md |

The template is the structural contract. Generated documents are instances of the template and must not be confused with the template itself.

## 6. Standard Selection

Before generation, consult standards/documentation-standard.md, standards/knowledge-classification-standard.md, standards/versioning-standard.md and standards/security-standard.md.

When the document uses sources, relationships, SAP objects, processes or business rules, the corresponding Knowledge specifications are also applicable.

## 7. Ticket Resolution

Resolve ticket_id in this order: explicitly provided by the user; identified in supplied context; identified through existing repository documentation with sufficient evidence; absent when the document type legitimately permits a document without a ticket.

Never invent a ticket identifier. When an existing ticket directory is available, get_ticket is the authoritative retrieval capability for its document set.

## 8. Context Retrieval

For a ticket, retrieve ticket documentation, available analysis/specification/test documents, documented chronology, decisions, validations, pending information and explicitly related documents.

Ticket context is historical context. It is not automatically reusable Knowledge or universal SAP behavior.

## 9. Knowledge Retrieval

Search reusable Knowledge before generating new statements. Relevant entities include SAP Objects, Processes, Business Rules, Relationships and Sources.

Classify retrieved information as directly applicable, related, potentially applicable or contradictory.

Only explicit relationships are traversed. Co-occurrence does not establish a relationship.

## 10. Source Retrieval

Sources are classified by origin, source_type, reliability and certainty.

Evidence priority is: direct evidence > official SAP documentation > confirmed configuration > confirmed code > functional test > internal documentation > analysis > inference.

A lower-priority source may provide context but must not be presented as stronger evidence than its classification supports.

## 11. Evidence Handling

The agent distinguishes direct evidence, documentary evidence, technical evidence, test evidence, debug evidence when referenced by existing documentation, partial evidence and absence of evidence.

When evidence is insufficient, the document explicitly records the gap.

## 12. Information Gaps

The agent must identify missing information, distinguish unknown from not applicable, mark pending validation, request indispensable information, continue generation where safe and never fill critical fields by assumption.

Allowed certainty states: confirmed, partial, under_validation, inferred, not_confirmed.

## 13. Document Generation

Generation follows this sequence: load the official template; load applicable standards; resolve ticket/context; retrieve Knowledge and relationships; retrieve sources; classify evidence; populate metadata; populate every required template section; explicitly mark unavailable information; validate the generated document.

The generator may construct a complete document in memory. Repository persistence is outside the MVP.

For functional tests, expected and obtained results are never invented. For requirements and specifications, technical objects are never invented. For investigations, conclusions remain bounded by the evidence.

## 14. Fact and Inference Separation

Every substantive statement must be attributable to user-provided information, repository fact, source/evidence, functional analysis, hypothesis, inference or pending validation.

Facts and evidence may be stated as such. Hypotheses and inferences must be labeled. Pending information must remain pending.

## 15. Validation

### Structural validation
- official template loaded;
- required headings present;
- metadata present;
- document type consistent.

### Content validation
- no invented facts;
- required sections populated or explicitly marked pending;
- facts, analysis and pending information remain distinguishable.

### Evidence validation
- relevant source paths retained;
- explicit relationships preserved;
- uncertainty retained;
- no relationship created by co-occurrence.

### Classification validation
- knowledge_type;
- knowledge_scope;
- certainty where applicable;
- SAP object origin and implementation_type;
- source origin, source_type and reliability where applicable.

### Security validation
- no passwords;
- no tokens;
- no API keys;
- no private keys;
- no credentials;
- no unnecessary sensitive production information.

### Version validation
- current version identified when available;
- change type recorded;
- history not silently overwritten.

## 16. Versioning

Versioning follows standards/versioning-standard.md. A version increment must be justified by the nature of the change. Git commit history is separate from the document version.

The agent must not rewrite historical approved/validated content silently. A correction creates a new logical version when the standard requires it.

## 17. Traceability

A generated document must expose, when applicable: originating ticket_id; source paths; retrieved Knowledge; explicit relationships; related documents; pending information; generation version/status.

Traceability must permit reconstruction of why a statement was included.

## 18. Existing Document Handling

Before creating a new document for a ticket: search for an existing document of the same type; determine whether the request is a new document or an update; compare the requested change with the existing version; preserve the prior logical version; increment the version when required; update related references when necessary; avoid duplicate documents.

The current MVP can generate proposed documents but does not perform repository writes or automatic merges.

## 19. Knowledge Promotion

Knowledge promotion is a separate lifecycle: DOCUMENTATION → DISCOVERY → CANDIDATE KNOWLEDGE → VALIDATION → REUSABLE KNOWLEDGE.

A generated document does not automatically become reusable Knowledge.

Promotion requires sufficient evidence, correct classification, source traceability and explicit validation.

## 20. Conflict Handling

When information conflicts, preserve the conflicting sources, identify dates and contexts, classify certainty, do not silently choose one as universal truth, and distinguish historical behavior from current behavior.

## 21. Output Contract

A generated output contains, when applicable: metadata; document_type; ticket_id; version; status; date; author; knowledge_type; knowledge_scope; complete template content; source/evidence traceability; related Knowledge; pending information.

The output is a proposed artifact unless a human process explicitly changes its status.

## 22. Human Review

Supported lifecycle statuses are draft, in_review, approved, validated, implemented and obsolete.

The agent may propose a status based on the request but must not claim human approval or validation unless explicitly documented.

## 23. Agent Rules

- Do not invent.
- Do not duplicate.
- Do not generalize from a single ticket without evidence.
- Do not confuse Standard with Custom.
- Do not confuse configuration with development.
- Do not create relationships without evidence.
- Do not convert inference into fact.
- Preserve uncertainty.
- Preserve traceability.
- Use the official template.
- Apply the applicable standards.
- Version changes consistently.
- Preserve history.
- Ask for clarification when indispensable.
- Do not execute or modify SAP.

## 24. Generation Checklist

- [ ] Correct document_type.
- [ ] Official template loaded.
- [ ] Required sections present.
- [ ] ticket_id resolved or intentionally absent.
- [ ] Metadata complete with known values only.
- [ ] knowledge_type and knowledge_scope classified.
- [ ] Facts separated from analysis and inference.
- [ ] Missing information explicitly marked.
- [ ] Sources/evidence traceable.
- [ ] Relationships are explicit, not inferred from co-occurrence.
- [ ] Standard/Custom classification supported by evidence.
- [ ] No technical object invented.
- [ ] Security validation passed.
- [ ] Version/status are consistent.
- [ ] Existing document checked when applicable.
- [ ] Human approval not assumed.
- [ ] Knowledge promotion not performed automatically.