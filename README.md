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
