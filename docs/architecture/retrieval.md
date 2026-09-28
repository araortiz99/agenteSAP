# Retrieval Architecture

## Orden de prioridad

1. exact identifier;
2. exact SAP object;
3. exact product/version;
4. exact entity relationship;
5. title/section;
6. semantic relevance;
7. lexical relevance.

Los términos genéricos no deben dominar el ranking.

## Source-aware retrieval

Filtros previstos:

- source = SAP_STANDARD;
- source = INTERNAL;
- source = QAS_RUNTIME;
- source = ALL;
- product;
- version;
- module;
- entity;
- document;
- language.

La selección de fuente es una necesidad de evidencia, no evidencia.

## SAP Standard

`search_sap_standard` debe permanecer separado de `search_knowledge`. `search_unified` puede combinar resultados para comparación, pero conserva `source_layer` y provenance.

## Version filtering

Un documento de S/4HANA 2025 no debe presentarse como evidencia universal de 2023, ECC o Cloud Public Edition.

## Conflictos

- Standard vs Internal difference → `standard_vs_internal_difference`
- dos documentos SAP incompatibles → `standard_documentation_conflict`
- Runtime vs SAP Help → `runtime_vs_documentation_difference`

Ninguno debe resolverse automáticamente por el LLM.

## Public SAP Developer Center MCP

AgenteSAP can optionally use the official SAP Developer Center hosted MCP as **external evidence**. The public search mount is read-only and uses Streamable HTTP.

Enable it locally with:

- `AGENTESAP_SAP_PUBLIC_MCP_ENABLED=true`
- `AGENTESAP_SAP_PUBLIC_MCP_URL=https://developers.sap.com/mcp/search` (default)
- `AGENTESAP_SAP_PUBLIC_MCP_READ_TOOLS=search_tutorials,get_tutorial,list_missions,get_mission`

For a live connectivity check, set `AGENTESAP_SAP_PUBLIC_MCP_LIVE_TESTS=true` and run:

`python -m pytest -q tests/test_public_sap_mcp_live.py`

The live smoke test performs only `tools/list` and one allowlisted `search_tutorials` call. It does not modify SAP or SAP Developer Center state.
