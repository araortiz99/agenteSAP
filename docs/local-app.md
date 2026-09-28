# AgenteSAP local app

## Prerequisites

- Python 3.12 or 3.13
- Repository cloned locally
- GitHub access configured if repository evidence is private
- `OPENAI_API_KEY` when using the LLM-backed consultation flow

## Start

From the repository root:

```bash
python -m pip install -r requirements.txt
python -m src.app.server
```

Then open:

```
http://127.0.0.1:8765
```

The server binds to localhost only by default.

## Environment

Optional:

```text
GITHUB_OWNER=araortiz99
GITHUB_REPO=agenteSAP
GITHUB_REF=main
GITHUB_TOKEN=<token-if-required>
OPENAI_API_KEY=<key>
OPENAI_MODEL=gpt-5.6
AGENTESAP_APP_HOST=127.0.0.1
AGENTESAP_APP_PORT=8765
```

Do not commit secrets. Keep `.env` local.

## Health check

```bash
curl http://127.0.0.1:8765/health
```

Expected response:

```json
{"status":"ok","mode":"local-read-only"}
```

## Consultation API

```bash
curl -X POST http://127.0.0.1:8765/api/consult \
  -H "Content-Type: application/json" \
  -d '{"request":"Explicame qué es un goods movement en SAP MM"}'
```

The API delegates to the same `run_agent()` used by the CLI. It does not create a second reasoning implementation.

## Safety boundary

The local app is a presentation/API shell. It does not expose SAP write operations.

QAS runtime remains disabled by default and is only usable when the separate QAS read-only contract is explicitly configured and verified.

## Current scope

The first UI is intentionally small. Future UI layers can expose:

- evidence and citations;
- Standard vs Internal/Custom separation;
- ticket analysis;
- relationships;
- document generation;
- QAS read-only observations;
- conversation history.

These should remain presentation features over the existing agent capabilities rather than duplicated business logic.
