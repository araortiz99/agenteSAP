# Knowledge Context Standard

## Propósito

Definir el contrato del contexto estructurado utilizado por el agente para conectar retrieval, relaciones, evidencia y el consultor LLM.

## 1. Entity

Una entidad es una referencia canónica respaldada por metadata del repositorio.

Campos:

- entity_id
- entity_type
- path
- match_type
- score
- certainty

Tipos soportados:

- SAP_OBJECT
- PROCESS
- BUSINESS_RULE
- TICKET
- SOURCE
- RELATIONSHIP

## 2. Relationship

Una relación es válida solamente si existe un documento explícito bajo knowledge/relationships/.

Campos:

- path
- source_id
- source_type
- relation_type
- target_id
- target_type
- hop

## 3. Evidence

Una evidencia debe provenir del retrieval existente.

Debe conservar:

- path
- source_layer
- source_id
- knowledge_type
- knowledge_scope
- certainty
- score
- hop

El campo hop indica cómo fue descubierta la evidencia; no modifica su certainty ni su provenance.

## 4. Context

KnowledgeContext contiene:

- query;
- entities;
- relationships;
- evidence;
- gaps;
- conflicts.

El contexto debe ser determinista para un mismo query + repository ref + límites de retrieval.

## 5. Relevancia

Prioridad:

1. evidencia directa de entidad;
2. evidencia directa de consulta;
3. evidencia de primer hop;
4. evidencia de segundo hop.

Ante empate:

1. mayor score;
2. SAP Standard antes que Internal solamente cuando el score sea equivalente;
3. path lexicográfico.

## 6. Seguridad

El contexto nunca debe incluir secretos.

No almacenar passwords, tokens, API keys, credenciales ni claves privadas.

## 7. Regla crítica

coocurrencia != relación

mención != entidad canónica

hop != certainty

retrieval != conclusión


## 8. Relationship certainty

La relación conserva su propia metadata:

- certainty;
- status;
- evidence_source_id.

Una relación partial/candidate no debe convertirse en confirmed por traversal.
