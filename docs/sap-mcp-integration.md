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
- observation type;
- provenance/source identifier.

The observation type prevents provider category from being confused with the source semantics:

- `developer_context`: curated developer context such as `sap-devs`;
- `runtime_observation`: an observation obtained from an SAP runtime provider;
- `custom_runtime_observation`: an organization-specific ABAP MCP runtime observation;
- `external_source`: an MCP result whose source category has not been classified more specifically.

MCP output does not become SAP Standard Knowledge automatically. Runtime evidence remains tied to the SAP environment from which it was observed.

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

The CLI exposes a built-in MCP server with tools including `list_packs`, `get_context`, `search_resources`, `get_known_errors`, `get_samples`, `search_tutorials`, and `search_learning_journeys`.

The AgenteSAP adapter has been locally validated against `sap-devs 0.0.15` using the official Python MCP SDK. The validated path is:

```
AgenteSAP
    ↓
SapMcpClient
    ↓
MCP stdio
    ↓
sap-devs 0.0.15
```

Validated operations include:

- MCP handshake;
- server/tool discovery;
- `search_resources` schema discovery;
- read-only `search_resources` invocation;
- read-only `list_packs` invocation;
- normalization into `SapMcpEvidence`.

The local `list_packs` response currently exposes four packs: `base`, `cap`, `abap`, and `btp-core`.

This provider is appropriate for current SAP developer guidance and curated resources. It is not treated as a live SAP system and is not assumed to be a general functional MM knowledge source.

The default AgenteSAP allowlist remains intentionally conservative. In particular, `update_tutorial_progress` is not enabled by default.

### sap-mcp-server

The server is a binary distribution that connects MCP-compatible clients to SAP ABAP/BTP services through a compatible backend. Its documentation defines read-only, developer and full access scopes and landscape controls.

AgenteSAP should use the read-only boundary for runtime investigation.

The server's `connections.json` is local configuration and must never be committed.

The AgenteSAP adapter, QAS/read-only runtime contract, discovery-only flow, tool-descriptor validation, and execution boundary are implemented and tested. A live `sap-mcp-server` connection to an actual SAP QAS landscape has not yet been validated.

### abap-ai/mcp

The ABAP SDK allows an SAP system to expose custom MCP servers with tools/resources and DDIC-derived schemas.

This is useful when organization-specific ABAP capabilities need to be exposed through MCP. It is not required for the first SAP Standard Knowledge flow.

No live ABAP-hosted MCP connection has been implemented or validated.

## Implementation status

Current repository implementation provides:

- provider profiles;
- explicit tool allowlisting;
- read-only contract;
- normalized evidence provenance and observation classification;
- an official Python MCP SDK stdio client adapter;
- local `sap-devs` handshake and read-tool validation;
- unit tests for provider boundaries and read-tool normalization;
- Router/Consultant integration of MCP evidence;
- source-aware runtime selection and provenance preservation;
- QAS-only `mcp_readonly` runtime configuration;
- discovery-only `tools/list` flow;
- allowlist + advertised-tool + read-only/destructive-hint execution checks.

Not yet validated:

- a live `sap-mcp-server` connection to an actual SAP QAS landscape;
- the concrete QAS tool catalog and the first approved business read operation;
- organization-specific SAP landscape credentials;
- a live `abap-ai/mcp` endpoint.

These are intentionally separate from the repository-side contract and test suite.
