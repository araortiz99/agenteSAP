Este archivo será el ÍNDICE MAESTRO DE TICKETS del repositorio `agenteSAP`.

==================================================
1. CONTEXTO
==================================================

El repositorio `agenteSAP` constituye una base de conocimiento para un futuro agente de IA especializado en consultoría funcional SAP.

La arquitectura utiliza:

STANDARDS
    ↓
TEMPLATES
    ↓
KNOWLEDGE
    ↓
TICKETS
    ↓
AGENT

Los tickets representan CASOS REALES.

El Knowledge Base representa CONOCIMIENTO REUTILIZABLE.

Por lo tanto:

TICKET
=
contexto específico + trazabilidad + documentación + evidencia

KNOWLEDGE
=
conocimiento permanente y reutilizable

El archivo:

tickets/ticket.md

define la estructura maestra de un ticket individual.

Este archivo:

tickets/index.md

debe funcionar como índice central para localizar y consultar rápidamente los tickets existentes.

==================================================
2. OBJETIVO
==================================================

El índice debe permitir al usuario y al futuro agente:

- localizar tickets;
- identificar tickets por `ticket_id`;
- conocer el tipo de ticket;
- conocer el módulo SAP;
- conocer el estado;
- conocer la prioridad;
- identificar fechas relevantes;
- acceder al documento maestro del ticket;
- identificar documentación asociada;
- identificar conocimiento relacionado;
- facilitar búsquedas y recuperación de contexto;
- evitar recorrer manualmente todo el repositorio.

El índice NO debe reemplazar el contenido de:

tickets/<ticket_id>/ticket.md

ni de los documentos especializados asociados.

Debe funcionar como una capa de navegación y descubrimiento.

==================================================
3. PRINCIPIO FUNDAMENTAL
==================================================

El índice debe responder rápidamente:

"¿Qué tickets existen y dónde está su información?"

No debe intentar responder:

"¿Cuál es el contenido completo del ticket?"

Por lo tanto:

INDEX
→ identifica y referencia.

TICKET
→ describe el caso.

DOCUMENTACIÓN
→ desarrolla el análisis o solución.

KNOWLEDGE
→ conserva conocimiento reutilizable.

==================================================
4. ESTRUCTURA DE TICKETS
==================================================

El índice debe asumir como estructura futura:

tickets/
├── index.md
├── ticket.md
│
├── <ticket_id>/
│   ├── ticket.md
│   ├── requirement.md
│   ├── analysis.md
│   ├── debug.md
│   ├── investigation.md
│   ├── functional-specification.md
│   └── functional-tests.md
│
├── <ticket_id>/
│   └── ...
│
└── ...

No asumir que todos los tickets tendrán todos los documentos.

Un ticket puede contener solamente:

ticket.md

o cualquier combinación de documentos oficiales y actividades de consultoría que corresponda.

==================================================
5. METADATA DEL ÍNDICE
==================================================

El archivo debe comenzar con:

---
document_type: "ticket-index"
version: "1.0"
status: "active"
date: ""
author: ""
---

No utilizar `ticket_id` en el front matter porque este archivo representa múltiples tickets.

El índice debe tener una sección visible de metadata.

==================================================
6. TÍTULO
==================================================

Utilizar:

# Índice de Tickets

Debajo del título incluir una breve descripción del propósito del índice.

==================================================
7. RESUMEN DEL ÍNDICE
==================================================

Incluir una sección:

## 1. Resumen

Debe explicar:

- qué representa este índice;
- qué información contiene;
- cómo se relaciona con `tickets/ticket.md`;
- cómo debe utilizarlo el agente.

No incluir información ficticia.

==================================================
8. CATÁLOGO PRINCIPAL
==================================================

Incluir:

## 2. Catálogo de Tickets

Utilizar una tabla estructurada:

| Ticket ID | Título | Tipo | Módulo | Prioridad | Estado | Fecha apertura | Fecha actualización | Ticket |
|---|---|---|---|---|---|---|---|---|

La columna `Ticket` debe contener un enlace relativo al documento maestro:

`[Ver ticket](./<ticket_id>/ticket.md)`

No inventar tickets.

Si todavía no existen tickets reales, dejar la tabla preparada sin datos ficticios e indicar:

"No existen tickets registrados actualmente."

==================================================
9. CAMPOS DEL CATÁLOGO
==================================================

El índice debe utilizar únicamente información disponible en el `ticket.md` correspondiente.

### Ticket ID

Debe coincidir exactamente con:

ticket_id

No modificar formato.

### Título

Debe representar el título real del ticket.

No generar títulos alternativos.

### Tipo

Utilizar el `ticket_type` registrado en el ticket.

Tipos permitidos por `tickets/ticket.md`:

- INCIDENT
- REQUIREMENT
- IMPROVEMENT
- CONSULTATION
- PROBLEM
- CHANGE
- INVESTIGATION
- OTHER

### Módulo

Utilizar el módulo SAP documentado.

Ejemplos conceptuales:

- MM
- FI
- SD
- EWM

No inferir el módulo si no está documentado.

### Prioridad

Utilizar la prioridad registrada.

No recalcularla ni modificarla.

### Estado

Utilizar el estado operativo real del ticket.

No confundir:

STATUS DEL TICKET

con:

STATUS DEL DOCUMENTO

### Fecha apertura

Utilizar:

date_opened

### Fecha actualización

Utilizar:

date_updated

==================================================
10. CLASIFICACIÓN POR TIPO
==================================================

Incluir:

## 3. Tickets por Tipo

Organizar referencias por:

### INCIDENT

### REQUIREMENT

### IMPROVEMENT

### CONSULTATION

### PROBLEM

### CHANGE

### INVESTIGATION

### OTHER

Cada categoría debe contener únicamente referencias a tickets existentes.

Ejemplo conceptual:

### INCIDENT

- [33007 — Error en generación de XML SNC K1](./33007/ticket.md)
- [31426 — Error en mosaico SNC](./31426/ticket.md)

No inventar información.

Si una categoría no contiene tickets:

"N/A"

==================================================
11. CLASIFICACIÓN POR MÓDULO
==================================================

Incluir:

## 4. Tickets por Módulo

Organizar los tickets por módulo SAP cuando el módulo esté documentado.

Ejemplo conceptual:

### MM

- [33007](./33007/ticket.md)

### FI

- [XXXXX](./XXXXX/ticket.md)

### SD

- [XXXXX](./XXXXX/ticket.md)

No crear categorías para módulos no documentados.

Si un ticket afecta múltiples módulos:

registrarlo en cada módulo correspondiente solamente si esa relación está explícitamente documentada.

==================================================
12. TICKETS ABIERTOS Y CERRADOS
==================================================

Incluir:

## 5. Estado de Tickets

Separar como mínimo:

### Abiertos

### Cerrados

### En análisis

### Pendientes de validación

### Otros estados

Utilizar el estado real registrado en cada ticket.

No interpretar automáticamente un estado.

Si el estado no permite una clasificación clara:

registrarlo en:

### Otros estados

==================================================
13. DOCUMENTACIÓN ASOCIADA
==================================================

Incluir:

## 6. Documentación Asociada

Esta sección debe explicar cómo localizar documentos relacionados con cada ticket.

La información detallada permanece dentro del directorio del ticket.

Ejemplo conceptual:

```text
tickets/
└── 33007/
    ├── ticket.md
    ├── analysis.md
    ├── debug.md
    ├── investigation.md
    ├── functional-specification.md
    └── functional-tests.md

El índice no debe duplicar el contenido de estos documentos.

Cuando sea útil, puede incluir una tabla:

Ticket ID	Requirement	Analysis	Debug	Investigation	Functional Specification	Functional Tests

Utilizar enlaces relativos únicamente cuando los archivos existan.

No crear enlaces hacia documentos inexistentes.

==================================================
14. KNOWLEDGE RELACIONADO

Incluir:

7. Knowledge Relacionado

El índice puede indicar qué tickets tienen relación con:

SAP Objects;
Processes;
Business Rules;
Relationships.

No duplicar el contenido del Knowledge Base.

Utilizar los identificadores reales:

object_id
process_id
rule_id
relationship_id

Ejemplo conceptual:

Ticket ID	SAP Objects	Processes	Business Rules	Relationships

Los valores deben ser referencias a entidades existentes.

No crear identificadores ficticios.

==================================================
15. BÚSQUEDA POR IDENTIFICADOR

Incluir:

8. Convenciones de Búsqueda

Definir que ticket_id es el identificador transversal principal.

El agente debe poder utilizarlo para localizar:

ticket;
requirement;
functional specification;
functional tests;
analysis;
debug;
investigation;
objetos SAP relacionados;
procesos relacionados;
reglas relacionadas;
relaciones;
evidencias.

Ejemplo conceptual:

ticket_id
   ↓
tickets/<ticket_id>/
   ↓
documentación
   ↓
knowledge relacionado
==================================================
16. REGLAS PARA EL AGENTE

Incluir:

9. Reglas para el Agente

El agente debe:

Utilizar ticket_id como identificador principal para localizar tickets.
Buscar primero en tickets/index.md cuando necesite descubrir tickets.
Abrir tickets/<ticket_id>/ticket.md para obtener el contexto completo.
Consultar documentos especializados solamente cuando sean necesarios.
No interpretar el índice como fuente de conocimiento funcional detallado.
No inventar tickets.
No inventar estados.
No inventar prioridades.
No inventar relaciones.
No asumir que un ticket tiene documentación que no existe.
Mantener los enlaces relativos actualizados.
Utilizar el Knowledge Base para conocimiento reutilizable.
Utilizar el ticket como evidencia y contexto de un caso específico.
Respetar las versiones y estados documentales.
Mantener trazabilidad entre ticket y documentación relacionada.
==================================================
17. REGLAS DE ACTUALIZACIÓN

Incluir:

10. Actualización del Índice

Definir que el índice debe actualizarse cuando:

se crea un nuevo ticket;
cambia información relevante del ticket;
se agrega documentación significativa;
cambia el estado operativo;
se identifican nuevas relaciones con Knowledge;
se elimina o archiva un ticket.

El índice no debe contener información que contradiga el ticket.md.

Cuando exista una diferencia:

verificar el ticket.md;
verificar la versión;
verificar la fecha;
actualizar el índice;
conservar la trazabilidad mediante Git.
==================================================
18. CONTROL DE DUPLICADOS

Incluir:

11. Control de Duplicados

No debe existir más de una entrada principal para el mismo:

ticket_id

Si un ticket tiene múltiples documentos:

todos deben permanecer bajo el mismo ticket.

No crear tickets duplicados para representar:

análisis;
debug;
investigación;
pruebas;
especificaciones.

Esos documentos pertenecen al mismo ticket cuando comparten el mismo ticket_id.

==================================================
19. TICKETS SIN TICKET_ID

No crear entradas para documentos que no tengan:

ticket_id

Si un documento no está asociado a un ticket:

ticket_id: "N/A"

debe permanecer fuera del catálogo de tickets.

Puede pertenecer a Knowledge o documentación independiente.

==================================================
20. SEGURIDAD

El índice debe cumplir:

standards/security-standard.md

No almacenar:

contraseñas;
tokens;
API keys;
credenciales;
claves privadas;
secretos;
datos personales innecesarios;
información productiva sensible.

El índice debe contener únicamente metadata y referencias necesarias para localizar conocimiento.

==================================================
21. VERSIONADO

El índice debe utilizar:

version: "1.0"

Aplicar las reglas de:

standards/versioning-standard.md

Cambios editoriales:

PATCH

Cambios que agreguen información sin alterar la estructura:

MINOR

Cambios estructurales relevantes:

MAJOR

Git constituye el historial técnico de modificaciones.

==================================================
22. PREPARACIÓN PARA IA

El índice debe estar diseñado para facilitar consultas como:

¿Qué tickets existen sobre MM?
¿Qué tickets están abiertos?
¿Qué tickets están relacionados con SNC?
¿Qué tickets tienen debugging?
¿Qué tickets tienen especificación funcional?
¿Qué tickets están relacionados con determinado objeto SAP?
¿Qué tickets afectan determinado proceso?
¿Qué tickets documentaron una determinada regla?
¿Qué tickets están relacionados entre sí?

El índice debe actuar como punto inicial de recuperación.

El agente debe poder seguir:

INDEX
↓
TICKET
↓
DOCUMENTACIÓN
↓
KNOWLEDGE
↓
EVIDENCIA

==================================================
23. RELACIÓN CON KNOWLEDGE BASE

El índice de tickets NO debe convertirse en un segundo Knowledge Base.

Debe mantener la separación:

TICKETS
→ casos históricos y operativos.

KNOWLEDGE
→ conocimiento reusable.

Un ticket puede descubrir o validar conocimiento.

Pero el conocimiento debe permanecer en:

knowledge/

cuando corresponda.

==================================================
24. CALIDAD DEL ÍNDICE

Antes de considerar actualizado tickets/index.md, verificar:

 todos los ticket_id son válidos;
 no existen duplicados;
 los enlaces apuntan a archivos existentes;
 el título coincide con el ticket;
 el tipo coincide con el ticket;
 el módulo coincide con el ticket;
 el estado coincide con el ticket;
 las fechas coinciden con el ticket;
 no existen referencias ficticias;
 no se duplicó contenido funcional;
 no se inventaron relaciones;
 se respetan los standards;
 la información sensible fue excluida.
==================================================
25. FORMATO FINAL

El archivo final debe ser un documento Markdown limpio, profesional y preparado para humanos y agentes de IA.

Debe contener:

YAML front matter.
Título # Índice de Tickets.
Metadata.
Resumen.
Catálogo principal.
Clasificación por tipo.
Clasificación por módulo.
Estado de tickets.
Documentación asociada.
Knowledge relacionado.
Convenciones de búsqueda.
Reglas para el agente.
Reglas de actualización.
Control de duplicados.
Tratamiento de tickets sin ticket_id.
Seguridad.
Versionado.
Preparación para IA.
Relación con Knowledge Base.
Checklist de calidad.

No crear tickets ficticios.

No crear ejemplos de tickets reales.

No inventar IDs.

No inventar enlaces.

No modificar tickets/ticket.md.

No modificar otros archivos.
