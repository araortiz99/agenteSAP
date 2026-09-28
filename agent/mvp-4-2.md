# MVP 4.2 — SAP Consultant Experience

## Objetivo

Convertir el pipeline de consulta del MVP 4/4.1 en una experiencia de uso
orientada al Analista Funcional SAP.

MVP 4.2 no introduce:

- RAG semántico;
- memoria conversacional persistente;
- ejecución SAP;
- escritura automática en Knowledge Base.

## Flujo

```
USER
 ↓
CONSULTOR SAP
 ↓
Intent / Ticket detection
 ↓
Unified Retrieval
 ↓
Evidence + Reasoning
 ↓
Ticket Context
 ↓
LLM
 ↓
Structured Answer
 ├── Respuesta
 ├── Evidencias
 ├── Fuentes
 ├── Certeza
 ├── Información faltante
 └── Contexto del ticket
```

## Experiencia mínima

Una consulta debe poder responder con una estructura:

### Resumen

Respuesta funcional breve.

### Qué está confirmado

Solo hechos respaldados por evidencia confirmada.

### Qué corresponde a nuestra implementación

Separar conocimiento interno/custom de SAP Standard.

### Qué no está confirmado

Mostrar explícitamente gaps, evidencia parcial y contradicciones.

### Evidencias

Mostrar EVD-* con su fuente, path y certainty.

### Ticket

Cuando exista ticket_id, mostrar TKT-* y relaciones relevantes.

### Próximos pasos

Solo acciones funcionales sugeridas por la evidencia; no ejecutar SAP.

## Gate previo

MVP 4.2 se considera habilitado para implementación después de una prueba
con un proveedor LLM real que valide:

1. exactitud factual;
2. preservación de certainty;
3. citas EVD-* válidas;
4. tratamiento de contradicciones;
5. separación Standard/Custom;
6. identificación de información faltante.

## No objetivo

No implementar todavía:

- embeddings;
- vector database;
- RAG semántico;
- memoria de conversación;
- aprendizaje automático sobre tickets;
- ejecución de transacciones SAP;
- escritura automática de conocimiento.

## Resultado esperado

El agente debe sentirse como una capa de asistencia inteligente para el
Analista Funcional SAP, manteniendo la Knowledge Base como fuente de contexto
y la evidencia como mecanismo de control.
