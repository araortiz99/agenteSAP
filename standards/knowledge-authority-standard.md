# Knowledge Authority Standard

## Purpose

Define when AgenteSAP may treat persisted knowledge as a source of truth.

Retrieval and authority are separate concerns:

```
SOURCE → INGEST → PROVENANCE → CLASSIFY → REVIEW → AUTHORIZE → RETRIEVE
```

Finding a document does not make it authoritative.

## Authority states

| State | Meaning | May support factual answer | Source of truth |
|---|---|---:|---:|
| candidate | Ingested but not reviewed | Yes, explicitly qualified | No |
| reference | Reviewed contextual material | Yes | No |
| authoritative | Explicitly approved current knowledge | Yes | Yes |
| superseded | Replaced by a newer authority | Historical only | No |

## Mandatory provenance

Every business knowledge source must retain:

- stable source/document ID;
- SHA-256 content hash;
- logical version;
- origin;
- scope;
- source path;
- document title;
- evidence/chunk references;
- approval identity when authoritative.

## Promotion gate

Knowledge may become authoritative only when:

1. provenance is complete;
2. security review has passed;
3. a human approval identity is recorded;
4. the content has a valid version;
5. the source is not generated knowledge;
6. the change passed the Knowledge Lifecycle PR process.

The agent cannot self-approve or silently promote knowledge.

## Conflict rule

If two authoritative sources conflict, the agent must not select one silently.

It must expose:

- both sources;
- their versions;
- their scopes;
- their authority state;
- the conflict;
- the information required to resolve it.

A superseded source must never override a current authoritative source unless the user explicitly asks for historical behavior.

## Answer semantics

When an answer uses knowledge:

- authoritative → state as documented organizational fact;
- reference → identify it as reference/context;
- candidate → identify it as unvalidated;
- superseded → identify it as historical;
- inference → label as inference;
- missing evidence → state what is unknown.

## Non-negotiable rule

```
INGESTED ≠ VALIDATED
VALIDATED ≠ AUTHORITATIVE
AUTHORITATIVE ≠ UNIVERSAL
```

Authority is scoped by source, version and applicability.
