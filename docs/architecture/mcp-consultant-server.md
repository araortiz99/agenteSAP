# AgenteSAP Consultant MCP Server

AgenteSAP can be exposed as a remote, read-only MCP server.

Tools: `consult_sap`, `investigate_sap`, and `agentesap_health`.

Use stdio locally or Streamable HTTP remotely. Production deployments require TLS and authentication. GitHub and SAP credentials remain server-side. The server exposes no SAP write operation.

The remote `/mcp` endpoint is the integration boundary for supported ChatGPT custom MCP apps and GitHub Copilot MCP configuration.


## Deployment checklist

Before exposing the HTTP endpoint:

1. Run the full test suite.
2. Build the Docker image.
3. Put the service behind HTTPS.
4. Enforce authentication at the gateway/reverse proxy.
5. Keep `GITHUB_TOKEN` and all SAP/QAS credentials in the deployment secret store.
6. Keep QAS runtime disabled until its explicit read-only allowlist has been validated.
7. Smoke-test `agentesap_health`, then `tools/list`, then one bounded `investigate_sap` call.
8. Do not expose any SAP write-capable MCP tool.

The application itself currently exposes only read-oriented MCP tools; the HTTP authentication layer should be supplied by the production gateway until the application-level auth guard is added.
