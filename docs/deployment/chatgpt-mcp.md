# AgenteSAP → ChatGPT MCP

## Production security contract

This deployment is **read-only and fail-closed**.

- QAS runtime is disabled.
- No SAP write tool exists.
- No GitHub write tool exists.
- The Streamable HTTP MCP endpoint requires a Bearer token when
  `AGENTESAP_MCP_AUTH_REQUIRED=true`.
- The token is checked by the HTTP layer and is never exposed as a tool input.
- The process refuses to start if authentication is required but the token is
  missing.
- `GITHUB_TOKEN` is a deployment secret and is never committed.
- Private business knowledge must not be enabled behind an unauthenticated
  endpoint.

The Bearer token is a bootstrap protection. For a multi-user production
ChatGPT integration, replace it with an OAuth/OIDC gateway and keep the MCP
server behind that gateway.

## Render deployment

The repository contains `deploy/render.yaml` for a Docker web service.
Render supports Docker-based web services and lets secrets be configured as
environment variables instead of committing them to source control.

Required production secrets:

- `GITHUB_TOKEN`: minimum read access required for the knowledge repository.
- `AGENTESAP_MCP_BEARER_TOKEN`: random high-entropy secret used to protect
  MCP requests during the bootstrap phase.

Required runtime flags:

```
AGENTESAP_MCP_SERVER_TRANSPORT=streamable-http
AGENTESAP_MCP_SERVER_HOST=0.0.0.0
AGENTESAP_MCP_SERVER_PORT=8000
AGENTESAP_MCP_SERVER_PATH=/mcp
AGENTESAP_MCP_AUTH_REQUIRED=true
AGENTESAP_MCP_ALLOWED_HOSTS=agentesap-consultant-mcp.onrender.com:*
AGENTESAP_SAP_RUNTIME_ENABLED=false
AGENTESAP_SAP_PUBLIC_MCP_ENABLED=true
GITHUB_OWNER=araortiz99
GITHUB_REPO=agenteSAP
GITHUB_REF_NAME=main
```

### First deployment

1. Create the Render Web Service from `araortiz99/agenteSAP`.
2. Select Docker and branch `main`.
3. Configure the two secrets above.
4. Deploy.
5. Verify `GET /healthz` returns a non-secret healthy status.
6. Verify an unauthenticated `/mcp` request receives HTTP 401.
7. Verify an authenticated MCP client can initialize and list exactly:
   - `consult_sap`
   - `investigate_sap`
   - `agentesap_health`
8. Keep QAS disabled.

Render assigns a public `onrender.com` URL to a web service. Do not place
secrets in the URL.

## ChatGPT integration

ChatGPT custom MCP apps are configured from Developer Mode / Apps on supported
workspace plans. The endpoint and authentication mechanism are selected
during app creation. If OAuth is used, the identity provider must support
refresh tokens; OpenAI specifically documents the `offline_access` scope and
discovery metadata requirements.

For a durable enterprise deployment, use:

```
ChatGPT
   ↓
OAuth/OIDC
   ↓
Authenticated MCP gateway
   ↓
AgenteSAP MCP
   ↓
GitHub knowledge
   ↓
Optional public SAP Developer Center MCP

QAS = OFF
Writes = OFF
```

Do not expose private business documents through a public unauthenticated
endpoint.

## Acceptance criteria

- [ ] Render service created and deployed.
- [ ] HTTPS endpoint reachable.
- [ ] Authentication required at HTTP boundary.
- [ ] No secrets in source control.
- [ ] `tools/list` contains only the three consultant tools.
- [ ] `consult_sap` is read-only and traceable.
- [ ] `investigate_sap` remains bounded.
- [ ] health reports QAS disabled.
- [ ] No SAP write path exists.
- [ ] OAuth/OIDC gateway is configured before private business knowledge is
      considered production-ready.
