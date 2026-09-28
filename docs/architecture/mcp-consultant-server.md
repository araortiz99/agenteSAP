# AgenteSAP Consultant MCP Server

AgenteSAP can be exposed as a remote, read-only MCP server.

Tools: `consult_sap`, `investigate_sap`, and `agentesap_health`.

Use stdio locally or Streamable HTTP remotely. Production deployments require TLS and authentication. GitHub and SAP credentials remain server-side. The server exposes no SAP write operation.

The remote `/mcp` endpoint is the integration boundary for supported ChatGPT custom MCP apps and GitHub Copilot MCP configuration.
