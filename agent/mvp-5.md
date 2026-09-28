# MVP 5 — Knowledge Intelligence Layer

## Estado

**MVP 5 EN IMPLEMENTACIÓN — 5.1–5.5 OPERACIONALES**

MVP 4.2 queda como contrato estable y no se redefine desde este MVP.

## 1. Objetivo

Convertir el pipeline de consulta validado en MVP 4.2 en un pipeline capaz de construir contexto funcional SAP estructurado a partir de entidades identificables, relaciones explícitamente documentadas, evidencia directa, evidencia relacionada, fuentes, tickets, conflictos y gaps de conocimiento.

El agente continúa siendo read-only respecto de SAP y del repositorio.

## 2. Flujo

USER QUERY → ENTITY RESOLUTION → DIRECT RETRIEVAL → RELATIONSHIP TRAVERSAL → RELATED RETRIEVAL → CONTEXT BUILDING → EVIDENCE / REASONING / TRACEABILITY → MVP 4.2 CONSULTANT → SEMANTIC VALIDATION

## 3. Componentes

### 5.1 Entity Resolution

Identifica únicamente entidades respaldadas por metadata o documentos del repositorio.

Tipos iniciales:

- SAP_OBJECT
- PROCESS
- BUSINESS_RULE
- TICKET
- SOURCE
- RELATIONSHIP

Una mención textual sin identificador respaldado no se convierte automáticamente en una entidad canónica.

### 5.2 Relationship Resolution

Utiliza exclusivamente relaciones documentadas en knowledge/relationships/.

Regla: coocurrencia != relación.

Cada relación recuperada conserva path, source_id, source_type, relation_type, target_id, target_type y hop.

### 5.3 Multi-hop Retrieval

El MVP soporta traversal acotado.

Valores por defecto:

- máximo 2 hops;
- máximo 8 entidades;
- máximo 16 relaciones;
- máximo 12 resultados de evidencia.

No se permite traversal ilimitado.

### 5.4 Context Builder

Construye un objeto KnowledgeContext que mantiene separados:

- entidades;
- relaciones;
- evidencia directa;
- evidencia relacionada;
- gaps;
- conflictos.

El contexto no reemplaza EvidenceAssessment ni TraceabilityReport.

### 5.5 Relevance

La evidencia directa tiene prioridad sobre la evidencia recuperada por relación.

Orden:

1. direct entity evidence;
2. direct query evidence;
3. first-hop related evidence;
4. second-hop related evidence.

El hop nunca cambia la procedencia original de una evidencia.

## 4. Reglas de integridad

1. No inventar entidades.
2. No inventar relaciones.
3. No convertir una mención en relación.
4. No elevar certainty.
5. No transformar Standard en Custom ni Custom en Standard.
6. No resolver conflictos automáticamente.
7. No utilizar ausencia de evidencia como prueba de inexistencia.
8. Mantener path y source_id cuando existan.
9. El contexto debe ser reproducible con el mismo repository ref.
10. El LLM recibe contexto, pero no controla provenance.

## 5. Integración con MVP 4.2

MVP 5 agrega contexto estructurado al prompt existente.

No modifica:

- contrato de respuesta;
- Structure Gate;
- Evidence Gate;
- Ticket Gate;
- Conflict Gate;
- identificadores EVD-*;
- identificadores TKT-*.

El LLM continúa siendo consumidor del contexto y no fuente de verdad.

## 6. Fuera de alcance

No implementar en MVP 5:

- vector database;
- embeddings;
- fine-tuning;
- ejecución SAP;
- escritura automática de Knowledge;
- aprendizaje automático de relaciones;
- resolución automática de conflictos;
- memoria conversacional persistente.

## 7. Benchmark

Casos mínimos:

1. resolución de entidad;
2. relación directa;
3. multi-hop;
4. preservación de conflicto;
5. separación Standard/Custom;
6. missing knowledge;
7. deduplicación de evidencia;
8. límite de traversal.

## 8. Gates

### Entity Gate

Las entidades recuperadas deben estar respaldadas por metadata/documentos.

### Relationship Gate

Toda relación debe existir explícitamente en knowledge/relationships/.

### Hop Gate

El traversal no puede superar el máximo configurado.

### Provenance Gate

Toda evidencia mantiene path, source layer, source_id y certainty.

### Context Gate

El contexto debe contener únicamente elementos derivados del retrieval y relaciones documentadas.

### Regression Gate

MVP 4.2 debe conservar su contrato y sus pruebas.

## 9. Criterio de cierre

MVP 5 podrá cerrarse cuando:

- los tests unitarios del Knowledge Intelligence Layer estén verdes;
- los casos negativos sean rechazados;
- el contexto sea reproducible;
- las relaciones falsas por coocurrencia sean rechazadas;
- los límites de hop funcionen;
- la integración con el consultant mantenga los gates de MVP 4.2;
- exista un benchmark ejecutable documentado.

## 10. Principio

RESOLVE → RETRIEVE → RELATE → TRAVERSE → BUILD CONTEXT → PRESERVE EVIDENCE → CONSULT

Nunca:

INFERIR RELACIONES → PERDER PROVENANCE → INVENTAR CONOCIMIENTO


MVP 5.4 — End-to-End Knowledge Consultant: CLOSED / APPROVED

Validado con el caso canónico 31426.

Flujo validado:
QUERY → ENTITY RESOLUTION → RELATIONSHIPS → MULTI-HOP → KNOWLEDGE CONTEXT → EVIDENCE → LLM → VALIDATED RESPONSE

Garantías verificadas:
- ticket context y TKT-*;
- resolución de ZMM_IMX_0004 por nombre técnico;
- relaciones explícitas;
- preservación de partial/candidate;
- conflicto K1/K4;
- separación Standard/Custom;
- evidencia EVD-*;
- estructura MVP 4.2;
- información pendiente sin elevar a confirmada;
- comportamiento read-only.

Hallazgo de implementación:
- los objetos SAP custom pueden tener un identificador interno (object_id) distinto del nombre técnico (object_name);
- las relaciones del grafo pueden utilizar el nombre técnico;
- entity resolution reconoce ambos sin tratar la relación como entidad.

Benchmark: benchmarks/mvp-5-4-end-to-end.md
Test: tests/test_mvp54_e2e.py
CI: Python Tests — 89 passed.


## MVP 5.5 — Operational Knowledge Consultant: CLOSED / APPROVED

MVP 5.5 convierte el Knowledge Consultant validado en MVP 5.4 en una interfaz CLI operativa.

Validado:
- consulta natural;
- ticket explícito con prioridad sobre extracción automática;
- repository ref configurable;
- max_results configurable;
- salida humana y JSON;
- plan de ejecución serializable;
- validación de parámetros;
- preservación de los gates de MVP 4.2 y 5.4;
- comportamiento read-only.

Benchmark: `benchmarks/mvp-5-5-operational-consultant.md`
Tests: `tests/test_mvp55_operational.py`
CI: Python Tests — 93 passed.


### MVP 5.5 — Performance Hardening

La validación E2E real del caso 31426 mostró una demora aproximada de varios minutos. El flujo funcional respondió correctamente, por lo que el siguiente foco de 5.5 es rendimiento operacional sin modificar la semántica de conocimiento.

Implementado:
- caché de árbol y archivos por ejecución/ref;
- lectura concurrente acotada de archivos;
- deduplicación de lecturas;
- sin memoria persistente;
- sin cambios de provenance, certainty, relaciones ni gates.

Estado: **CLOSED / APPROVED**.


### MVP 5.5 — Performance Hardening: CLOSED / APPROVED

La optimización operacional fue validada con el caso canónico 31426.

Resultado observado en ejecución local:
- baseline: ~5 minutos;
- después del hardening: ~20 segundos;
- reducción observada: ~93 %.

CI: Python Tests — 96 passed.

La medición de tiempo es una referencia de ejecución local y no un SLA productivo.
