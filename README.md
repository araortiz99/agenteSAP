# agenteSAP

Agente consultivo para conocimiento y documentación funcional SAP.

## Estado

MVP funcional en construcción.

El MVP actual es **read-only** respecto de SAP y GitHub: recupera y analiza información del repositorio y genera documentos en memoria, sin ejecutar SAP ni escribir automáticamente en el repositorio.

## Arquitectura

```
Usuario
  ↓
Agente SAP
  ↓
Intent Router
  ├── SAP Standard Retrieval
  └── Internal Knowledge Retrieval
  ↓
Capabilities / Tools
  ↓
GitHub Knowledge Base
  ├── knowledge/sap-standard
  ├── knowledge
  ├── tickets
  ├── standards
  ├── templates
  └── agent
```

## Capabilities MVP

| Capability | Estado |
|---|---|
| `search_knowledge` | ✅ |
| `search_sap_standard` | ✅ |
| `search_unified` | ✅ |
| `get_ticket` | ✅ |
| `get_related_knowledge` | ✅ |
| `analyze` | ✅ |
| `generate_document` | ✅ |

### SAP Standard Knowledge

El repositorio ya contiene una primera capa de **SAP Standard Knowledge** basada exclusivamente en documentación oficial de SAP Help Portal.

MVP inicial:

- SAP S/4HANA
- Materials Management / Inventory Management
- release 2025 FPS01
- retrieval léxico determinístico
- fuentes trazables mediante URL y `source_id`

Los primeros documentos curados cubren:

- Goods Movement
- Material Master / Product Master
- Inventory Management: Basic Principles

La documentación oficial de SAP describe, por ejemplo, Goods Movement como el proceso para planificar, ingresar y documentar movimientos de stock; y describe el material/product master como fuente central de información específica de materiales. citeturn0search0turn0search14

### Orquestación del agente

El MVP incluye intent routing determinístico.

Ejemplos:

- `Analizá el ticket 31426` → `get_ticket → get_related_knowledge → analyze`
- `Buscá SAP Standard sobre material master` → `search_sap_standard`
- `Buscá conocimiento sobre SNC` → `search_knowledge`

### Generación documental

El MVP materializa de forma segura:

- Requerimiento
- Análisis
- Especificación Funcional
- Pruebas Funcionales
- Investigación

Los documentos se generan respetando el contrato de generación y dejando explícitamente como pendiente la información que no puede sustentarse.

**DEBUG queda fuera del alcance del MVP actual.**

## Retrieval

La búsqueda actual es determinística y léxica.

La búsqueda general prioriza:

1. identificadores de entidad;
2. títulos;
3. contenido.

La búsqueda SAP Standard está deliberadamente restringida a `knowledge/sap-standard/`.

Las relaciones se recuperan únicamente cuando están documentadas explícitamente en `knowledge/relationships/`. La coocurrencia de términos no crea relaciones.

## Knowledge model

El repositorio separa:

- `knowledge/sap-standard/` → conocimiento reutilizable de SAP Standard;
- `knowledge/` → conocimiento reutilizable de la organización;
- `tickets/` → contexto histórico;
- `templates/` → contratos de estructura documental;
- `standards/` → reglas normativas;
- `agent/` → comportamiento y contratos del agente.

SAP Standard Knowledge nunca debe utilizarse como evidencia de configuración o desarrollo específico del cliente.

## Seguridad

El MVP no ejecuta SAP ni modifica SAP.

No deben almacenarse en el repositorio:

- passwords;
- tokens;
- API keys;
- credenciales;
- claves privadas;
- otros secretos.

Las credenciales de GitHub, cuando sean necesarias, se suministran mediante variables de entorno o mecanismos externos de secretos.

## Pruebas

Las pruebas unitarias e integración se ejecutan mediante GitHub Actions.

El baseline actual debe mantenerse verde antes de incorporar nuevas capacidades.

## Alcance pendiente

Siguientes incrementos:

1. ingestionador controlado desde SAP Help Portal;
2. extracción/chunking de documentación;
3. deduplicación y actualización por release;
4. retrieval semántico/híbrido;
5. ~~promoción controlada de conocimiento~~ → implementada en MVP 2.2;
6. persistencia mediante Pull Requests;
7. integración con un LLM.



### SAP Help ingestion

The repository now includes a controlled SAP Help ingestion MVP:

- allowlisted source registry;
- official SAP Help HTTPS validation;
- HTML parsing;
- release/module/source metadata;
- SHA-256 content checksum;
- candidate staging;
- CLI invocation;
- tests for registry and URL safety.

Example:

```bash
python -m src.sap.cli --source-id SAP-HELP-S4-MM-2025-GOODS-MOVEMENT
```

Output is staged under `staging/sap-standard/` and remains `candidate / under_validation` until explicitly validated.



### Knowledge Promotion

MVP 2.2 adds an explicit promotion boundary from SAP candidate staging to reusable SAP Standard Knowledge.

The promotion engine validates source registration, metadata, release context, classification, source-text checksum and duplicate destinations. Successful promotion changes `candidate / under_validation` to `validated / confirmed`.

Promotion never overwrites existing Knowledge automatically.

Example:

```bash
python -m src.sap.promote_cli staging/sap-standard/<candidate>.md
```


### MVP 3 — Unified Retrieval

The agent now supports a unified retrieval layer that queries:

- SAP Standard Knowledge;
- internal/custom Knowledge.

The result preserves the source layer and available evidence metadata instead of merging both sources into an undifferentiated answer.

Example intent:

```
Compará SAP Standard y nuestra implementación sobre material master
```

This is retrieval only. The MVP does not infer that a customer implementation is equivalent to SAP Standard merely because both sources mention the same concept.


### MVP 3.1 — Evidence & Reasoning

The agent now separates:

```
Unified Retrieval
      ↓
Evidence Assessment
      ↓
Bounded Reasoning
      ↓
Conclusion Status
```

Conclusion states:

- `supported`
- `partial`
- `requires_analysis`
- `conflict`
- `insufficient`

The engine does not treat Standard vs Custom as a conflict. When both layers exist, it returns `requires_analysis` because functional comparison is required.

Evidence retains provenance, source ID, knowledge classification, scope and certainty.


### MVP 3.2 — Evidence Traceability

Evidence can now be represented as a deterministic audit trace.

Each evidence item receives a stable `EVD-...` identifier derived from provenance rather than retrieval order.

A trace report preserves:

- evidence identity;
- source layer and source ID;
- path;
- knowledge classification;
- certainty;
- evidence role;
- supporting and unresolved evidence IDs;
- gaps and conflicts.

The trace can be rendered as a human-readable audit artifact and is designed to become structured context for a future LLM without losing provenance.


### MVP 4 — LLM Consultant

The agent now supports an explicit consultative LLM layer on top of the existing
deterministic retrieval, evidence assessment, bounded reasoning and evidence
traceability.

Flow:

```
Request
  ↓
Unified Retrieval
  ↓
Evidence Assessment
  ↓
Bounded Reasoning
  ↓
Evidence Traceability
  ↓
Bounded LLM Context
  ↓
Consultative Answer
```

The LLM does not retrieve arbitrary repository content and is not the source of
truth. It receives evidence records with provenance, certainty and stable
`EVD-*` identifiers.

The provider boundary is implemented in `src/llm/client.py`. The current
implementation uses the OpenAI Responses API through standard-library HTTP.
Credentials are runtime-only:

```bash
export OPENAI_API_KEY="..."
```

No API key is stored in the repository.

Explicit requests such as:

```
Consultá sobre material master
Explicame qué está confirmado sobre SNC
```

are routed through the LLM consultant. Existing deterministic intents remain
available.

The consultant is read-only and must not claim SAP execution, configuration
changes, code changes or GitHub modifications.

### MVP 5 — Knowledge Intelligence Layer

MVP 5 agrega una capa determinística para construir contexto funcional SAP a partir de entidades, relaciones explícitas y evidencia recuperada.

Componentes principales:

- Entity Resolution;
- Relationship Resolution;
- bounded multi-hop retrieval;
- KnowledgeContext;
- provenance preservation;
- conflict preservation.

El traversal está limitado por defecto a 2 hops, 8 entidades, 16 relaciones y 12 evidencias.

La regla fundamental se mantiene:

```
coocurrencia != relación
mención != entidad canónica
hop != certainty
retrieval != conclusión
```

El contexto de MVP 5 se incorpora al consultor de MVP 4.2 sin alterar su contrato de respuesta ni sus semantic gates.



### MVP 6 — Knowledge Governance

MVP 6 agrega una frontera explícita entre el consultor read-only y la persistencia controlada de Knowledge.

Flujo:

```
CONSULT → PROPOSE → VALIDATE → BRANCH → COMMIT → PULL REQUEST → HUMAN REVIEW → MERGE
```

La publicación está limitada inicialmente a `knowledge/`.

Gates:
- scope;
- metadata;
- security;
- version;
- branch;
- duplicate;
- Pull Request;
- human review.

El agente no modifica SAP, no escribe directamente en `main`, no hace merge y no se autoaprueba.

La CLI de publicación funciona en dry-run por defecto. La escritura real requiere `--publish` y un token de GitHub con permisos de escritura adecuados.