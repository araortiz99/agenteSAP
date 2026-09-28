# MVP 4 — LLM Consultant Contract

## Purpose

MVP 4 adds an LLM synthesis layer on top of deterministic retrieval, evidence,
reasoning and traceability.

The LLM is not the source of truth. It receives bounded repository evidence and
produces a consultative response subject to certainty and provenance rules.

## Flow

```
USER REQUEST
    ↓
UNIFIED RETRIEVAL
    ↓
EVIDENCE ASSESSMENT
    ↓
BOUNDED REASONING
    ↓
EVIDENCE TRACEABILITY
    ↓
LLM CONTEXT PACK
    ↓
LLM SYNTHESIS
    ↓
CONSULTATIVE ANSWER
```

## Provider boundary

`src/llm/client.py` defines the provider boundary. The MVP includes a minimal
OpenAI Responses API implementation using standard-library HTTP. No provider SDK
or credential is stored in the repository.

Runtime configuration:

- `OPENAI_API_KEY` — required at runtime for the OpenAI client.
- model selection is supplied when constructing the client.

The API key must never be committed to the repository, documentation, fixtures or logs.

## Evidence contract

The LLM receives, for each retrieved result:

- `EVD-*` evidence ID;
- path;
- source layer;
- source ID;
- knowledge type;
- knowledge scope;
- certainty;
- evidence role;
- bounded content snippet.

It also receives the deterministic conclusion status, gaps and conflicts.

## Response rules

The LLM must:

- answer in Spanish by default;
- preserve certainty;
- distinguish SAP Standard from internal/custom evidence;
- distinguish facts from functional interpretation;
- state evidence gaps;
- cite evidence IDs inline;
- never claim SAP execution or repository modification;
- never invent technical objects, configuration, causes or solutions.

## Security boundary

The MVP sends only retrieved Knowledge context to the provider. It does not send
GitHub credentials, SAP credentials, environment secrets or the local GitHub token.

The provider client is optional; deterministic retrieval and reasoning continue to
work without an API key.

## Failure behavior

If the provider is not configured or fails, the deterministic evidence and reasoning
results remain available. The application must surface the provider error rather than
fabricate an answer.
