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
