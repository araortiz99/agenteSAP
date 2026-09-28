# SAP Help Knowledge Ingestion

## Objetivo

Incorporar documentación oficial SAP Help como evidencia `SAP_STANDARD` sin mezclarla con conocimiento interno ni con observaciones runtime.

## Auditoría inicial de fuentes

La organización oficial verificada de SAP en GitHub mantiene una organización dedicada a SAP Docs y declara proyectos de documentación bajo `SAP-docs`. Algunos repositorios de esa organización publican el Markdown fuente de guías que se reflejan en SAP Help Portal. La estructura no debe asumirse homogénea entre productos.

Para el MVP MM se adopta como autoridad primaria el SAP Help Portal y, cuando exista un repositorio SAP-docs correspondiente a la documentación objetivo, se utilizará el repositorio como fuente reproducible del contenido y el Help Portal como URL de referencia.

Ejemplo verificado: `SAP-docs/sap-hana-cloud-data-intelligence` contiene una carpeta `docs/`, archivos Markdown y licencia CC-BY-4.0, y explica que sus Markdown son revisados para incorporarse al SAP Help Portal. Esto demuestra el patrón de publicación, pero no demuestra que ese repositorio sea fuente de S/4HANA MM. Por ello no se debe reutilizar como fuente MM.

Para S/4HANA MM, la fuente funcional verificable actualmente es SAP Help Portal con versión explícita. Ejemplos auditados: Material Master para S/4HANA on-premise 2023 y Goods Movement para S/4HANA on-premise 2025 FPS01. La versión declarada por SAP debe conservarse en metadata.

## Criterios de selección

1. Fuente oficial SAP Help o repositorio SAP-docs verificable.
2. Producto y release identificables.
3. Idioma identificable.
4. URL oficial disponible cuando corresponda.
5. Licencia/provenance documentada antes de copiar contenido.
6. No ingerir contenido de terceros como SAP Standard.
7. No ingerir indiscriminadamente todo SAP Help.
8. Preferir documentos MM directamente relacionados con el caso de uso.

## Pipeline

`Discovery → Source validation → Fetch → Parse → Normalize → Metadata extraction → Structural chunking → Entity extraction → Relationship extraction → Deduplication → Index → Evidence registration → Validation`

Debe ser incremental, idempotente, reproducible, auditable, read-only y resumible.

## Estrategia de fetch

Orden de preferencia:

1. Repositorio SAP-docs oficial, cuando la relación con el Help Portal esté demostrada.
2. SAP Help Portal para auditoría y referencia oficial.
3. No realizar crawling indiscriminado.

El ingestion job debe registrar commit SHA cuando la fuente sea Git. Para una fuente web sin commit, debe registrar URL, versión declarada, fecha de recuperación y hash de contenido.

## Normalización

No alterar el significado. Se conserva:

- título;
- jerarquía de headings;
- párrafos;
- tablas;
- procedimientos;
- ejemplos;
- enlaces;
- identificadores SAP.

La normalización debe producir una representación estable para hashing y retrieval.

## Chunking

El chunking es estructural:

`Document → Chapter → Section → Subsection → Paragraph/Table/Procedure/Example`

Nunca separar una tabla, procedimiento o ejemplo de su contexto cuando ello pueda cambiar su significado.

## Deduplicación

La identidad de contenido se determina mediante `content_hash`. Un documento no debe volver a indexarse si su contenido normalizado no cambió.

La identidad completa debe considerar al menos:

`source + repository + commit/version + path + document_id + content_hash`

## Actualización

Una ejecución incremental debe:

1. detectar cambios de fuente;
2. recuperar sólo archivos nuevos/modificados;
3. recalcular hashes;
4. conservar versiones anteriores;
5. registrar `retrieved_at`;
6. actualizar el índice sólo para contenido cambiado;
7. producir un resumen auditable.

## Límites

El MVP se limita a MM y a un conjunto focalizado:

- Material Master;
- Inventory Management;
- Goods Movements;
- Movement Types;
- Purchasing;
- Purchase Orders;
- Goods Receipt;
- Invoice Verification;
- Material Documents;
- Stock Management.

No se descargará todo SAP Help por defecto.

## Copyright y licensing

El repositorio debe conservar la licencia declarada por la fuente y provenance completa. No se debe asumir que la disponibilidad pública implica permiso para redistribuir copias completas.

El índice puede almacenar metadata, hashes y fragmentos mínimos necesarios para retrieval, sujeto a la licencia aplicable. La URL oficial debe estar disponible para navegación y verificación.

## Estrategia de recuperación

SAP Standard debe permanecer en una capa independiente de INTERNAL y RUNTIME.

Prioridad conceptual:

1. exact identifier;
2. exact SAP object;
3. exact product/version;
4. exact relationship;
5. title/section;
6. semantic relevance;
7. lexical relevance.

La ausencia de SAP Help no prueba ausencia del comportamiento.

## Governance

SAP Help puede confirmar comportamiento estándar documentado, pero nunca confirma por sí sola:

- configuración de PY44;
- comportamiento de Z;
- causa raíz;
- ejecución real;
- resultado QA;
- equivalencia entre implementación interna y estándar.

Cualquier diferencia Standard/Internal se clasifica inicialmente como `standard_vs_internal_difference`, no como contradicción automática.

## Seguridad

La ingestión es read-only. No requiere conexión SAP ni expone operaciones mutantes.

## Estado

Esta documentación define la foundation de ingestión. La selección de un repositorio SAP-docs específico para S/4HANA MM queda pendiente hasta disponer de evidencia explícita de correspondencia con las páginas objetivo del Help Portal.
