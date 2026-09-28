# SAP MCP Integration

## Objective

Integrate three complementary SAP MCP ecosystems without coupling AgenteSAP to one provider:

- `SAP-samples/sap-devs-cli`: curated, current SAP developer knowledge and an MCP server exposed by `sap-devs mcp serve`.
- `sap-support/sap-mcp-server`: runtime access to SAP ABAP/BTP services through a compatible backend.
- `abap-ai/mcp`: ABAP-side MCP Server SDK for organization-specific tools and resources.

## Provider boundaries

| Provider | Primary role | Transport in AgenteSAP | Initial policy |
|---|---|---|---|
| sap-devs | SAP developer knowledge/resources | stdio | read-only, explicit tool allowlist |
| sap-mcp-server | SAP runtime | stdio | read-only, explicit tool allowlist |
| abap-ai | Custom ABAP MCP endpoint | streamable HTTP | read-only, explicit tool allowlist |

## Security boundary

AgenteSAP currently exposes MCP integration as read-only.

No credentials are stored in this repository. Provider-specific credentials must remain in the local MCP/client environment.

For `sap-mcp-server`, use the provider's read-only scope where available. Do not configure a full/write scope for AgenteSAP's read path.

For ABAP-hosted MCP servers, authorization remains an SAP concern. The repository records provenance and policy but does not grant SAP authorizations.

## Evidence model

Every MCP result that becomes evidence must retain:

- provider;
- operation/tool;
- source;
- system when known;
- landscape when known;
- SAP object when known;
- certainty;
- provenance/source identifier.

Runtime evidence must not silently become reusable SAP Standard Knowledge. It is evidence about a particular SAP environment.

## Knowledge flow

```
SAP source / MCP
      ↓
provider adapter
      ↓
normalized evidence
      ↓
classification + provenance
      ↓
candidate Knowledge
      ↓
human validation
      ↓
knowledge/sap-standard or knowledge/internal
```

## Provider notes

### sap-devs

The CLI can synchronize SAP developer content and exposes a built-in MCP server with tools such as `list_packs`, `get_context`, `search_resources`, `get_known_errors`, `get_samples`, `search_tutorials`, and `search_learning_journeys`.

This provider is appropriate for current SAP developer guidance and curated resources. It is not treated as a live SAP system.

### sap-mcp-server

The server is a binary distribution that connects MCP-compatible clients to SAP ABAP/BTP services through a compatible backend. Its documentation defines read-only, developer and full access scopes and landscape controls.

AgenteSAP should use the read-only boundary for runtime investigation.

The server's `connections.json` is local configuration and must never be committed.

### abap-ai/mcp

The ABAP SDK allows an SAP system to expose custom MCP servers with tools/resources and DDIC-derived schemas.

This is useful when organization-specific ABAP capabilities need to be exposed through MCP. It is not required for the first SAP Standard Knowledge flow.

## Implementation status

Current repository implementation provides:

- provider profiles;
- explicit tool allowlisting;
- read-only contract;
- normalized evidence provenance;
- tests for provider boundaries.

Not yet implemented:

- live MCP protocol client;
- local provider installation;
- SAP landscape credentials;
- SAP runtime connection;
- automatic promotion of MCP output to Knowledge.

Those are intentionally separate steps.
