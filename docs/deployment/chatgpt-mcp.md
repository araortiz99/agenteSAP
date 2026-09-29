# AgenteSAP → ChatGPT MCP

## Scope

Remote Streamable HTTP MCP facade for the AgenteSAP consultant. This phase is
strictly read-only and keeps QAS runtime disabled.

## Exposed tools

- consult_sap
- investigate_sap
- agentesap_health

No SAP, GitHub, or Knowledge write tool is exposed.

## Deployment contract

Required environment:

    AGENTESAP_MCP_SERVER_TRANSPORT=streamable-http
    AGENTESAP_MCP_SERVER_HOST=0.0.0.0
    AGENTESAP_MCP_SERVER_PORT=8000
    AGENTESAP_MCP_SERVER_PATH=/mcp
    AGENTESAP_SAP_RUNTIME_ENABLED=false
    AGENTESAP_SAP_PUBLIC_MCP_ENABLED=true
    GITHUB_OWNER=araortiz99
    GITHUB_REPO=agenteSAP
    GITHUB_REF_NAME=main
    GITHUB_TOKEN=<secret>

The GitHub token must be stored as a deployment secret and must have only the
minimum repository access required to read the knowledge source.

## Security

The service must be exposed only over HTTPS. Do not place secrets in the MCP
URL or source control.

For private business knowledge, do not use an unauthenticated public endpoint
as the production boundary. Configure OAuth/OIDC at the MCP gateway before
loading sensitive company documents.

The OAuth provider should advertise and issue refresh tokens (for OIDC this
normally means offline_access) so ChatGPT can maintain authorization.

QAS remains disabled until a separate read-only runtime security review.

## ChatGPT registration

In ChatGPT web, authorized users can create a custom MCP app from Developer
Mode / Apps settings. Provide the HTTPS MCP endpoint and select the supported
authentication mechanism. If OAuth is selected, complete the authorization
flow and tool scan, then create the app.

The exact UI and availability depend on the ChatGPT plan and workspace policy.

## Acceptance

- HTTPS endpoint is reachable.
- MCP protocol initializes.
- tools/list exposes exactly the three read-only consultant tools.
- health reports QAS disabled.
- consult_sap works against public/approved knowledge.
- investigate_sap respects bounded limits.
- no write tool is exposed.
- authentication is required before private knowledge is enabled.
