# Agent Capabilities

## 1. Purpose

Define the executable capabilities exposed by the SAP agent.

This file describes the contract of each capability. It does not implement the capability.

Implementation belongs under `src/`.

The initial agent operates in read-only mode against the knowledge repository. It does not execute SAP transactions and does not modify SAP.

## 2. Capability Model

Each capability defines:

- purpose;
- when it should be invoked;
- inputs;
- outputs;
- allowed sources;
- validation rules;
- access level;
- failure behavior.

The agent must use the minimum capability set required to fulfill a request.

## 3. Initial Capabilities

| Capability | Purpose | Access |
|---|---|---|
| `search_knowledge` | Search repository knowledge and documentation | read |
| `get_ticket` | Retrieve a complete ticket context | read |
| `get_related_knowledge` | Retrieve documented relationships and related entities | read |
| `analyze` | Build an evidence-based functional analysis | read |
| `generate_document` | Generate a document according to a template and standards | read + generated output |

## 4. search_knowledge

### Purpose

Find relevant repository files based on a user query.

### Invocation

Use when the agent needs to discover information before answering or analyzing.

### Inputs

```yaml
query: string
paths: optional list[string]
max_results: optional integer
```

### Outputs

```yaml
query: string
results:
  - path: string
    score: number
    matched_terms: list[string]
    content: string
```

### Rules

- Search only repository content.
- Prefer `knowledge/`, `tickets/`, `standards/`, `templates/`, and `agent/`.
- Do not claim that a result exists unless it was retrieved.
- Preserve the source path.
- Do not expose secrets.
- Search is read-only.

## 5. get_ticket

### Purpose

Retrieve the context of a specific ticket.

### Inputs

```yaml
ticket_id: string
```

### Outputs

The ticket document and its available related documentation.

### Rules

- Never invent a ticket.
- Resolve only an existing `tickets/<ticket_id>/` directory.
- Preserve the ticket_id.
- Treat ticket information as historical context, not automatically as reusable knowledge.

## 6. get_related_knowledge

### Purpose

Retrieve documented knowledge related to an entity.

### Inputs

```yaml
entity_type: string
entity_id: string
```

### Outputs

Related:

- SAP Objects;
- Processes;
- Business Rules;
- Relationships;
- Sources;
- Documents;
- Tickets.

### Rules

- Follow documented relationships only.
- Do not create relationships from co-occurrence.
- Preserve certainty and source information.
- Distinguish direct relationships from broader search matches.

### MVP behavior

The implementation reads only Markdown relationship records under
`knowledge/relationships/`. An entity matches when it is the documented
source or target of a relationship. Co-occurrence in tickets, documents, or
other files is not treated as a relationship.

A result may be empty when no explicit relationship has been documented.

## 7. analyze

### Purpose

Produce an evidence-based functional analysis using repository context.

### Inputs

```yaml
request: string
ticket_id: optional string
context: optional object
```

### Outputs

An analysis following `templates/analysis.md` and the applicable standards.

### Rules

- Retrieve evidence before reasoning.
- Separate facts, hypotheses, inferences, and missing information.
- Distinguish standard, configuration, custom, and integration.
- Never invent SAP objects, technical implementations, or business rules.
- Keep ticket context separate from reusable knowledge.

### MVP behavior

The implementation retrieves the ticket first and then retrieves explicit
relationships for that ticket. It extracts only explicitly formatted ticket
bullet items as MVP facts. It does not infer root causes, solutions, or
business rules.

Missing relationships or insufficient evidence are returned explicitly.
Hypotheses remain empty unless a later implementation adds an evidence-backed
hypothesis mechanism.

## 8. generate_document

### Purpose

Generate a concrete document instance using the repository's template and standards.

### Inputs

```yaml
document_type: string
ticket_id: optional string
request: string
```

### Outputs

A validated document instance.

### Rules

- Load the corresponding template.
- Load applicable standards.
- Retrieve context and evidence.
- Complete metadata from known information only.
- Mark missing information explicitly.
- Validate before delivery.
- Do not automatically promote generated content to reusable Knowledge.

### MVP behavior

The implementation loads the requested official template before generating.
For `analysis`, it retrieves the ticket and documented relationships through
the analysis capability and materializes a draft with explicit evidence and
pending information.

Other document types currently produce a structural draft with explicit
pending content rather than inventing facts. Repository writes are not
performed by this capability.

## 9. Access Levels

### read

The capability may retrieve and interpret repository information but may not modify repository content.

### generated output

The capability may construct a document in memory or as a proposed artifact. Repository write access is not implied.

### future write

Repository modification, branch creation, commits, pull requests, or deletion are separate capabilities and must not be assumed by the initial agent.

## 10. Common Failure States

The implementation should distinguish at least:

- `not_found`
- `invalid_input`
- `repository_unavailable`
- `authentication_failed`
- `permission_denied`
- `parse_error`
- `ambiguous_request`

A failure must never be converted into invented content.

## 11. Security

Capabilities must never return:

- passwords;
- tokens;
- API keys;
- private keys;
- credentials;
- other secrets.

Secrets must be supplied through the runtime environment or secret manager, never repository files.

## 12. Extension Rule

New capabilities must be documented here before being treated as part of the agent contract.

Each new capability must define its purpose, inputs, outputs, access level, source restrictions, validation rules, and failure behavior.


## 12. Orchestration and Intent Routing

The MVP exposes an orchestration layer that receives a natural-language request and selects the minimum capability chain required to fulfill it.

The orchestration flow is:

```
USER REQUEST
    ↓
INTENT ROUTING
    ↓
AGENT PLAN
    ↓
CAPABILITY EXECUTION
    ↓
RESULT
```

The router must:

- identify the primary intent;
- resolve an explicit ticket identifier when present;
- select only supported capabilities;
- reject ambiguous requests when a required identifier or document type is missing;
- execute capabilities in the required order;
- return the result together with the selected plan.

For example, a request such as "Analizá el ticket 31426" is routed to:

```
get_ticket
    ↓
get_related_knowledge
    ↓
analyze
```

The user does not need to invoke these capabilities individually.

The orchestration layer is deterministic in the MVP. It does not use an LLM to select tools and does not execute SAP actions.

### Orchestration access

The orchestration layer remains read-only. It can retrieve repository content and construct an in-memory result, but it does not modify SAP or persist repository changes.
