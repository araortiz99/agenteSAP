Actúa como arquitecto de repositorios de conocimiento y especialista en gestión documental para agentes de IA orientados a SAP.

Necesito generar el archivo:

standards/output-structure-standard.md

Este documento debe definir de manera normativa cómo se almacenan, identifican, nombran, versionan y relacionan los documentos generados por el agente SAP.

IMPORTANTE:

- No generar documentos funcionales concretos.
- No generar tickets reales.
- No inventar información SAP.
- No modificar la arquitectura conceptual existente.
- No reemplazar documentation-standard.md.
- No reemplazar versioning-standard.md.
- No reemplazar los templates.
- Este archivo debe definir únicamente la estructura física y las convenciones de salida.

==================================================
ARQUITECTURA ACTUAL
==================================================

El repositorio contiene:

tickets/
├── index.md
└── ticket.md

templates/
├── analysis.md
├── functional-specification.md
├── functional-tests.md
├── investigation.md
└── requirement.md

knowledge/
├── business-rules/
├── processes/
├── relationships/
├── sap-objects/
└── sources/

standards/
├── documentation-standard.md
├── knowledge-classification-standard.md
├── security-standard.md
└── versioning-standard.md

agent/
├── agent.md
└── generation.md

El ticket_id será el identificador transversal para los casos asociados a tickets.

==================================================
OBJETIVO
==================================================

Definir exactamente cómo debe estructurarse:

tickets/<ticket_id>/

y cómo se almacenan dentro los documentos generados.

==================================================
ESTRUCTURA BASE
==================================================

La estructura propuesta debe ser:

tickets/
├── index.md
├── ticket.md
├── <ticket_id>/
│   ├── ticket.md
│   ├── requirement.md
│   ├── analysis.md
│   ├── investigation.md
│   ├── debug.md
│   ├── functional-specification.md
│   └── functional-tests.md

Sin embargo, analizar esta estructura y determinar si:

- ticket.md debe existir siempre;
- los documentos deben tener nombres fijos;
- los documentos deben ser opcionales;
- un ticket puede contener varios documentos del mismo tipo;
- debe existir un identificador documental adicional;
- cómo manejar múltiples versiones;
- cómo manejar documentos históricos.

No asumir automáticamente que la estructura propuesta es definitiva.

==================================================
DOCUMENT TYPES
==================================================

Los tipos documentales actuales son:

- requirement
- analysis
- debug
- investigation
- functional-specification
- functional-tests

Definir:

1. nombre canónico;
2. nombre del archivo;
3. ubicación;
4. relación con ticket_id;
5. posibilidad de múltiples documentos del mismo tipo.

Utilizar nombres de archivo consistentes y en lowercase-kebab-case o lowercase con guiones, seleccionando una única convención y justificándola.

==================================================
TICKET
==================================================

Definir la estructura:

tickets/<ticket_id>/ticket.md

El ticket debe funcionar como contexto principal del caso.

Definir qué información debe vivir en ticket.md y qué información debe permanecer exclusivamente en documentos especializados.

Evitar duplicación.

==================================================
DOCUMENT ID
==================================================

Analizar si los documentos deben tener:

document_id

además de:

ticket_id

Evaluar la necesidad de document_id considerando:

- trazabilidad;
- relaciones;
- referencias cruzadas;
- versionado;
- documentos históricos;
- reutilización futura;
- Knowledge Graph.

Si se recomienda document_id, definir:

- formato;
- reglas;
- unicidad;
- relación con ticket_id;
- ejemplos conceptuales.

No crear IDs reales.

==================================================
VERSIONADO
==================================================

Definir cómo se representa la versión.

Distinguir:

1. archivo actual;
2. versión documental;
3. historial Git;
4. documentos obsoletos.

Analizar si las versiones deben almacenarse:

A)
en el mismo archivo mediante metadata e historial,

o

B)
como archivos separados,

o

C)
mediante Git exclusivamente.

Seleccionar una estrategia coherente con versioning-standard.md.

Evitar duplicación innecesaria de archivos.

==================================================
NOMENCLATURA
==================================================

Definir reglas para:

- ticket_id;
- document_id;
- nombres de archivo;
- directorios;
- extensiones;
- metadata;
- referencias internas.

La nomenclatura debe ser:

- determinística;
- legible;
- estable;
- compatible con Git;
- fácil de recuperar por un agente de IA.

==================================================
DOCUMENTOS MÚLTIPLES
==================================================

Analizar casos como:

- dos análisis diferentes;
- varias investigaciones;
- varias pruebas funcionales;
- una especificación funcional revisada;
- documentos complementarios.

Definir cuándo:

- actualizar el documento existente;
- versionar;
- crear un documento nuevo;
- utilizar un documento relacionado.

No permitir duplicación arbitraria.

==================================================
DOCUMENTOS SIN TICKET
==================================================

Definir qué ocurre cuando un documento no tiene ticket_id.

Ejemplos:

- investigación general;
- documentación de proceso;
- documentación de objeto SAP;
- análisis transversal;
- conocimiento general.

Determinar si:

- deben existir fuera de tickets;
- deben vivir directamente en knowledge/;
- deben tener otra estructura.

La solución debe mantener clara la separación entre:

DOCUMENTATION
y
REUSABLE KNOWLEDGE.

==================================================
RELACIÓN CON KNOWLEDGE
==================================================

Definir cómo un documento almacenado en:

tickets/<ticket_id>/

puede referenciar:

knowledge/sap-objects/
knowledge/processes/
knowledge/business-rules/
knowledge/relationships/
knowledge/sources/

La referencia debe ser estable.

No duplicar Knowledge dentro del ticket.

==================================================
RELACIÓN CON SOURCES
==================================================

Definir cómo los documentos generados referencian las Sources utilizadas.

Debe ser posible responder:

- qué fuente fue utilizada;
- qué evidencia aportó;
- cuándo fue consultada;
- qué parte del documento respalda.

==================================================
INDEXACIÓN
==================================================

Definir el papel de:

tickets/index.md

Debe actuar como índice y no como copia de los contenidos de los tickets.

Determinar qué columnas/campos debe contener.

Como mínimo evaluar:

- ticket_id;
- title;
- ticket_type;
- module;
- priority;
- status;
- knowledge_type;
- knowledge_scope;
- date_opened;
- date_updated;
- date_closed;
- path.

==================================================
ESTRUCTURA DE DIRECTORIOS
==================================================

Definir formalmente:

tickets/
tickets/<ticket_id>/

y, si corresponde:

knowledge/
knowledge/<knowledge_type>/

No crear niveles de carpetas innecesarios.

La estructura debe facilitar:

- navegación humana;
- recuperación semántica;
- recuperación determinística;
- Git;
- automatización futura;
- relaciones entre entidades.

==================================================
REGLAS DE CREACIÓN
==================================================

Definir cuándo el agente:

- crea un ticket;
- crea un documento;
- actualiza un documento;
- crea una nueva versión;
- crea un documento adicional;
- actualiza tickets/index.md.

El agente no debe crear archivos duplicados por cada interacción.

==================================================
REGLAS DE ACTUALIZACIÓN
==================================================

Definir el flujo:

DOCUMENTO EXISTENTE
→ IDENTIFICAR
→ COMPARAR
→ DETERMINAR CAMBIO
→ ACTUALIZAR
→ VERSIONAR
→ REGISTRAR TRAZABILIDAD

==================================================
REGLAS DE ELIMINACIÓN
==================================================

Definir si los documentos:

- pueden eliminarse;
- deben marcarse obsolete;
- deben conservarse por trazabilidad.

Priorizar preservación histórica.

==================================================
REFERENCIAS INTERNAS
==================================================

Definir cómo referenciar:

- ticket;
- documento;
- SAP Object;
- Process;
- Business Rule;
- Relationship;
- Source.

Las referencias deben ser estables y no depender de texto libre cuando exista un identificador formal.

==================================================
ESTRUCTURA DEL DOCUMENTO GENERADO
==================================================

Definir metadata mínima que debe aparecer al inicio de cada documento.

Como mínimo evaluar:

```yaml
document_id: ""
document_type: ""
ticket_id: ""
title: ""
version: "1.0"
status: ""
knowledge_type: ""
knowledge_scope: ""
date: ""
author: ""
