# Workbench 2.0

## Propósito

El Workbench es la consola local de observabilidad, análisis y trazabilidad de agenteSAP. La UI consume contratos estructurados del backend y mantiene el payload legado en su forma original para compatibilidad. El nuevo contrato estructurado se expone bajo `workbench`.

## Arquitectura actual

\`\`\`
Usuario
  ↓
Workbench
  ↓
/api/consult
  ↓
Agent Router
  ↓
Retrieval / Evidence Assessment / Reasoning
  ↓
LLM Consultant
  ↓
Traceability
  ↓
WorkbenchAnalysisResponse
  ↓
UI
\`\`\`

## Fase 1 — Foundation

La primera entrega de Workbench 2.0 establece:

- \`request_id\` por solicitud.
- \`trace_id\` cuando existe trazabilidad.
- contrato \`WorkbenchAnalysisResponse\`.
- diagnóstico técnico estructurado.
- estado runtime explícito.
- evidencia, gaps y conflictos estructurados.
- compatibilidad con el payload \`result\` existente.

Los campos de latencia que el backend todavía no instrumenta por etapa se mantienen como \`null\`. No se simulan métricas.

## Regla de entrega incremental

No implementar todo Workbench 2.0 en un único cambio.

### Fase 1 — Foundation

- auditoría;
- response schema;
- diagnostics;
- request/trace IDs;
- backward compatibility.

### Fase 2 — Analysis UX

La UI consume el contrato `workbench` como fuente primaria para la lectura semántica del análisis. La respuesta Markdown continúa visible como representación completa y de compatibilidad.

- consulta;
- resumen estructurado;
- hechos confirmados;
- implementación documentada;
- elementos no confirmados;
- hipótesis, cuando el backend las provea;
- conflictos y gaps;
- evidencia y relaciones desde el contrato estructurado;
- estados vacíos explícitos cuando un bloque no tiene datos.

No se infiere certainty desde texto libre: los indicadores de evidencia utilizan la `certainty` entregada por el backend. La ausencia de hipótesis estructuradas se presenta como ausencia de datos, no como hipótesis inventada.

### Fase 3 — Evidence

La UI expone la evidencia ya producida por `EvidenceAssessment` y `TraceabilityReport`; no ejecuta un segundo retrieval.

- **Evidence Explorer:** filtra evidencia por texto, source layer y certainty.
- **Provenance Viewer:** muestra `evidence_id`, source layer, source ID, knowledge type/scope, certainty, weight, role, reason y provenance.
- **Retrieval Explorer:** muestra la query y los resultados realmente recuperados con score, matched terms, source layer, match type, source ID y certainty.
- estados vacíos explícitos;
- selección de evidencia para inspección de provenance.

El contrato `WorkbenchAnalysisResponse.retrieval` expone únicamente metadata de resultados recuperados; no contiene contenido adicional ni permite ejecutar retrieval desde el navegador.

### Fase 4 — Knowledge Intelligence

- relationships;
- graph;
- multi-hop explorer.

### Fase 5 — SAP Workspaces

- Ticket Workspace;
- SAP Object Workspace.

### Fase 6 — Operational UX

- runtime status;
- loading;
- errors;
- export.

Después de cada fase:

\`\`\`
implement
→ test
→ inspect diff
→ run E2E
→ verify CI
→ audit architecture
\`\`\`

No comenzar la siguiente fase si la anterior deja regresiones conocidas.

Si una capacidad no tiene soporte suficiente en backend, no se simula en frontend. Se extiende primero el contrato correspondiente o se registra como pendiente.

## Seguridad

- SAP writes permanecen deshabilitadas.
- PRD no se habilita.
- QAS runtime sigue siendo opt-in y read-only.
- El navegador no ejecuta herramientas SAP directamente.
- No se exponen secretos mediante endpoints.
- Runtime \`enabled_not_verified\` no significa conectado: requiere evidencia operacional adicional.
- SAP Standard, Internal, Runtime y External permanecen separados.

## Contrato estructurado

\`WorkbenchAnalysisResponse\` contiene:

- identidad de solicitud y trazabilidad;
- intención;
- resumen;
- hechos confirmados;
- implementación;
- información no confirmada;
- hipótesis;
- evidencia;
- relaciones;
- conflictos;
- gaps;
- contexto de ticket;
- diagnostics;
- runtime;
- respuesta Markdown para compatibilidad.

El Markdown es una representación legible; la UI debe preferir el contrato estructurado.

## Compatibilidad

El endpoint existente \`POST /api/consult\` continúa devolviendo \`result\`. La nueva estructura se expone en paralelo bajo `workbench`, sin cambiar la forma del payload legado. Esto permite migración incremental del frontend.

## Próximas fases

La siguiente fase puede reemplazar progresivamente la lectura de Markdown por paneles semánticos, sin modificar el Agent Router ni duplicar retrieval.
