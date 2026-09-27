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
Capabilities
  ↓
Tools
  ↓
GitHub Knowledge Base
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
| `get_ticket` | ✅ |
| `get_related_knowledge` | ✅ |
| `analyze` | ✅ |
| `generate_document` | ✅ |

### Orquestación del agente

El MVP incluye una capa determinística de intent routing. Una solicitud como `Analizá el ticket 31426` se transforma automáticamente en el plan `get_ticket → get_related_knowledge → analyze`, sin que el usuario tenga que invocar las capabilities individualmente.

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

La relevancia prioriza:

1. identificadores de entidad;
2. títulos;
3. contenido.

Las relaciones se recuperan únicamente cuando están documentadas explícitamente en `knowledge/relationships/`. La coocurrencia de términos no crea relaciones.

## Knowledge model

El repositorio separa:

- `knowledge/` → conocimiento reutilizable;
- `tickets/` → contexto histórico;
- `templates/` → contratos de estructura documental;
- `standards/` → reglas normativas;
- `agent/` → comportamiento y contratos del agente.

La clasificación utiliza `knowledge_type`, `knowledge_scope`, certeza y clasificación Standard/Custom según la evidencia disponible.

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

El siguiente nivel posterior al MVP puede incorporar:

- retrieval semántico;
- mejor resolución de documentos existentes y versionado;
- promoción controlada de Knowledge;
- persistencia mediante Pull Requests;
- integración con un LLM.

Estas capacidades no forman parte del MVP actual.
