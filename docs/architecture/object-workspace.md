# SAP Object Workspace

## Propósito

El SAP Object Workspace presenta un objeto SAP concreto como una unidad auditable de investigación. Consume las capacidades existentes de Knowledge Intelligence y no introduce un segundo motor de retrieval o traversal.

## Flujo

~~~
Query de objeto
  ↓
KnowledgeContext
  ↓
Entity Resolution
  ↓
Object Identity
  ↓
Relaciones explícitas
  ↓
Evidence
  ↓
Tickets / Dependencies
  ↓
Runtime status
  ↓
Gaps / Conflicts
~~~

## Identidad

Los estados posibles son:

- `resolved`: existe una única entidad soportada.
- `ambiguous`: existen múltiples candidatos soportados.
- `unresolved`: no existe una entidad soportada suficiente.

El Workspace no convierte nombres o convenciones SAP en hechos. Por ejemplo, un prefijo `ZMM` no basta para confirmar por sí mismo el módulo MM.

## Contrato

La implementación usa `src/tools/object_workspace.py` como contrato de dominio:

- `ObjectIdentity`
- `ObjectWorkspace`

El endpoint local es:

~~~
GET /api/object/{object_id}
~~~

La respuesta conserva:

- identidad;
- objeto resuelto;
- overview;
- relaciones;
- dependencias;
- evidencia;
- tickets;
- runtime;
- gaps;
- conflictos;
- diagnostics.

## Relaciones

Las relaciones se toman exclusivamente de `KnowledgeContext.relationships`. No se crean edges en el navegador y la ausencia de una relación no demuestra que no exista.

## Evidence

La evidencia conserva:

- path;
- score;
- matched terms;
- source layer;
- source ID;
- knowledge type/scope;
- certainty;
- hop;
- discovery;
- provenance.

## Runtime QAS

El Workspace no ejecuta una consulta QAS al abrir un objeto.

El estado:

- `not_observed` significa que no existe evidencia runtime en el contexto;
- `observed` solamente se informa cuando existe evidencia con `knowledge_scope=runtime` o `knowledge_type=runtime_observation`.

Runtime continúa separado de SAP Standard/Internal Knowledge y mantiene acceso `read-only`.

## Seguridad

- no SAP writes;
- no PRD;
- no browser → SAP;
- no browser → MCP;
- no wildcard allowlist;
- no promoción automática de MCP a Internal Knowledge;
- no certainty inflation;
- no relaciones inventadas.

## Limitaciones actuales

- el Workspace depende de que el objeto esté representado en el conocimiento indexado;
- no existe todavía un catálogo universal de todos los objetos SAP;
- no se genera una descripción funcional libre si el conocimiento no la respalda;
- la ejecución runtime queda fuera de la apertura del Workspace.

## Testing

Los tests cubren:

- resolución exacta;
- ambigüedad;
- entidades no soportadas;
- separación Knowledge/Runtime;
- contrato del builder;
- endpoint HTTP.

La validación E2E y CI deben realizarse sobre la rama de Fase 5 antes de considerar el cambio listo para revisión.
