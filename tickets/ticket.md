Quiero que crees el archivo:

tickets/ticket.md

Este archivo será la plantilla maestra para documentar y centralizar TICKETS dentro del repositorio agenteSAP.

==================================================
CONTEXTO
==================================================

El repositorio agenteSAP está construyendo una base de conocimiento estructurada para un futuro agente de IA especializado en consultoría funcional SAP.

Las fases anteriores establecieron:

FASE 1 — STANDARDS

- standards/documentation-standard.md
- standards/versioning-standard.md
- standards/security-standard.md

FASE 2 — TEMPLATES

- templates/requirement.md
- templates/functional-specification.md
- templates/functional-tests.md
- templates/analysis.md
- templates/debug.md
- templates/investigation.md

FASE 3 — KNOWLEDGE

- knowledge/sap-objects/object.md
- knowledge/processes/process.md
- knowledge/business-rules/business-rule.md
- knowledge/relationships/relationships.md

FASE 4 — TICKETS

Este archivo será el registro maestro de cada ticket.

==================================================
OBJETIVO
==================================================

ticket.md debe funcionar como el índice y contexto central de un caso real.

Debe responder:

- ¿Qué ticket es?
- ¿Qué tipo de caso representa?
- ¿Cuál es el problema o necesidad?
- ¿Cuál es su alcance?
- ¿Cuál es el estado actual?
- ¿Qué documentación se generó?
- ¿Qué objetos SAP están involucrados?
- ¿Qué procesos están involucrados?
- ¿Qué reglas de negocio están involucradas?
- ¿Qué relaciones fueron identificadas?
- ¿Qué evidencias existen?
- ¿Qué conclusión se obtuvo?
- ¿Qué información sigue pendiente?
- ¿Cuál es el resultado final?

ticket.md NO debe reemplazar:

- requirement.md
- functional-specification.md
- functional-tests.md
- analysis.md
- debug.md
- investigation.md

Esos documentos contienen el detalle especializado.

ticket.md debe centralizar y enlazar dicho conocimiento.

==================================================
PRINCIPIO FUNDAMENTAL
==================================================

Un ticket representa un CASO REAL.

El Knowledge Base representa CONOCIMIENTO REUTILIZABLE.

Por lo tanto:

TICKET
=
contexto específico + trazabilidad + documentación + referencias

KNOWLEDGE
=
conocimiento permanente y reutilizable

No copiar dentro del ticket toda la documentación de objetos, procesos o reglas.

El ticket debe referenciarlos mediante sus identificadores.

==================================================
ESTRUCTURA CONCEPTUAL
==================================================

El ticket debe funcionar como punto de conexión:

TICKET
   │
   ├── Requirement
   ├── Analysis
   ├── Debug
   ├── Investigation
   ├── Functional Specification
   ├── Functional Tests
   │
   ├── SAP Objects
   ├── Processes
   ├── Business Rules
   ├── Relationships
   │
   └── Evidence

El ticket puede descubrir, confirmar, cuestionar o modificar conocimiento existente.

==================================================
METADATA
==================================================

El archivo debe comenzar obligatoriamente con YAML front matter:

---
ticket_id: ""
ticket_type: ""
title: ""
module: ""
priority: ""
status: ""
version: "1.0"
date_opened: ""
date_updated: ""
date_closed: ""
author: ""
---

Luego:

# Ticket

## Metadata

Utilizar una tabla:

| Campo | Valor |
|---|---|
| Ticket ID | |
| Tipo | |
| Título | |
| Módulo | |
| Prioridad | |
| Estado | |
| Versión | |
| Fecha de apertura | |
| Última actualización | |
| Fecha de cierre | |
| Autor | |

No inventar valores.

==================================================
TICKET_ID
==================================================

ticket_id es el identificador transversal del caso.

Debe mantenerse estable durante todo el ciclo de vida del ticket.

Puede representar:

- incidente;
- requerimiento;
- mejora;
- consulta;
- investigación;
- problema;
- cambio;
- otro caso de soporte.

El ticket_id NO identifica:

- un objeto SAP;
- un proceso;
- una regla;
- una relación.

Esos elementos poseen sus propios identificadores.

==================================================
TICKET_TYPE
==================================================

Registrar el tipo de ticket.

Utilizar categorías controladas:

- INCIDENT
- REQUIREMENT
- IMPROVEMENT
- CONSULTATION
- PROBLEM
- CHANGE
- INVESTIGATION
- OTHER

Si la clasificación no está confirmada:

"UNKNOWN"

No crear categorías innecesarias.


==================================================
ESTADOS
==================================================

Utilizar estados consistentes con:

standards/documentation-standard.md

Para el documento:

- draft
- in_review
- approved
- implemented
- validated
- obsolete

Cuando se necesite representar el estado operativo del ticket, utilizar una clasificación separada y explícita.

Por ejemplo:

- OPEN
- IN_ANALYSIS
- WAITING_INFORMATION
- IN_DEVELOPMENT
- IN_TEST
- RESOLVED
- CLOSED
- CANCELLED

No mezclar:

ESTADO DEL DOCUMENTO

con:

ESTADO DEL TICKET


==================================================
1. IDENTIFICACIÓN DEL CASO
==================================================

## 1. Identificación del caso

Documentar:

- ticket_id;
- título;
- tipo;
- módulo;
- prioridad;
- solicitante, si corresponde;
- área;
- fecha de apertura;
- estado actual.

No almacenar información personal innecesaria.

==================================================
2. RESUMEN
==================================================

## 2. Resumen

Describir brevemente:

- qué ocurrió;
- qué se necesita;
- cuál es el impacto;
- cuál es el estado actual.

Debe permitir comprender el ticket sin leer todos los documentos relacionados.

No reemplazar el análisis detallado.

==================================================
3. ANTECEDENTE
==================================================

## 3. Antecedente

Documentar el contexto que originó el ticket.

Puede incluir:

- proceso involucrado;
- situación previa;
- cambio reciente;
- incidente previo;
- requerimiento del negocio;
- implementación relacionada;
- ticket anterior.

Distinguir hechos de interpretaciones.


==================================================
4. PROBLEMA / NECESIDAD
==================================================

## 4. Problema / Necesidad

Documentar claramente qué originó el caso.

Cuando sea un incidente:

- síntoma reportado;
- comportamiento esperado;
- comportamiento observado.

Cuando sea un requerimiento:

- necesidad;
- objetivo;
- resultado esperado.

Cuando sea una consulta:

- pregunta que debe responderse.


==================================================
5. ALCANCE
==================================================

## 5. Alcance

Definir qué está incluido en el ticket.

Puede incluir:

- procesos;
- sociedades;
- centros;
- almacenes;
- materiales;
- documentos;
- módulos;
- sistemas;
- objetos SAP.

También indicar explícitamente el fuera de alcance cuando esté definido.

No asumir alcance.


==================================================
6. IMPACTO
==================================================

## 6. Impacto

Documentar el impacto conocido.

Puede ser:

- funcional;
- operativo;
- contable;
- inventario;
- integración;
- fiscal;
- financiero;
- datos;
- usuarios.

Distinguir:

IMPACTO REPORTADO

de:

IMPACTO CONFIRMADO

cuando corresponda.


==================================================
7. DOCUMENTACIÓN DEL TICKET
==================================================

## 7. Documentación del ticket

Registrar los documentos generados durante el ciclo de vida del ticket.

Utilizar una tabla:

| Tipo | Documento | Ruta / Referencia | Versión | Estado |
|---|---|---|---|---|

Tipos permitidos:

- REQUIREMENT
- FUNCTIONAL_SPECIFICATION
- FUNCTIONAL_TEST
- ANALYSIS
- DEBUG
- INVESTIGATION
- OTHER

Los documentos deben utilizar los templates definidos en:

templates/

No duplicar su contenido en ticket.md.


==================================================
8. KNOWLEDGE RELACIONADO
==================================================

## 8. Knowledge relacionado

Esta sección conecta el ticket con la Fase 3.

### SAP Objects

| Object ID | Objeto | Relación con el ticket |
|---|---|---|

### Processes

| Process ID | Proceso | Relación con el ticket |
|---|---|---|

### Business Rules

| Rule ID | Regla | Relación con el ticket |
|---|---|---|

### Relationships

| Relationship ID | Relación | Rol en el ticket |
|---|---|---|

No copiar la documentación completa.

Utilizar los identificadores existentes.

==================================================
9. OBJETOS DESCUBIERTOS
==================================================

## 9. Objetos descubiertos

Registrar objetos SAP identificados durante el ticket que todavía no estén documentados en:

knowledge/sap-objects/

Utilizar:

DISC-OBJ-01
DISC-OBJ-02

Para cada uno:

| ID | Tipo | Nombre técnico | Estado | Acción |
|---|---|---|---|---|

Estados:

- IDENTIFICADO
- CONFIRMADO
- PENDIENTE
- NO CONFIRMADO

Si un objeto pasa a formar parte del Knowledge Base, debe crearse su documentación correspondiente.

No inventar object_id.


==================================================
10. PROCESOS DESCUBIERTOS
==================================================

## 10. Procesos descubiertos

Registrar procesos identificados durante el ticket que todavía no estén documentados.

Utilizar:

DISC-PROC-01
DISC-PROC-02

No duplicar procesos existentes.

Si el proceso ya existe:

referenciar su process_id.


==================================================
11. REGLAS DESCUBIERTAS
==================================================

## 11. Reglas descubiertas

Registrar reglas de negocio identificadas durante el ticket.

Utilizar:

DISC-BR-01
DISC-BR-02

Distinguir:

- regla existente confirmada;
- nueva regla identificada;
- regla cuestionada;
- regla pendiente de validación.

No crear reglas automáticamente sin evidencia.


==================================================
12. RELACIONES DESCUBIERTAS
==================================================

## 12. Relaciones descubiertas

Registrar nuevas relaciones identificadas durante el ticket.

Utilizar:

DISC-REL-01
DISC-REL-02

Una vez confirmada una relación, debe documentarse en:

knowledge/relationships/

No considerar una relación confirmada solamente porque dos objetos aparezcan en el mismo ticket.


==================================================
13. EVIDENCIAS
==================================================

## 13. Evidencias

Registrar evidencias relevantes del ticket.

Utilizar:

EVID-TKT-01
EVID-TKT-02

Pueden incluir:

- capturas;
- logs;
- documentos;
- resultados de consultas;
- resultados de pruebas;
- debug;
- documentación SAP;
- mensajes del sistema;
- configuraciones;
- archivos.

Utilizar:

| ID | Tipo | Referencia | Qué demuestra |
|---|---|---|---|

No almacenar secretos.

No incluir datos sensibles innecesarios.

==================================================
14. CRONOLOGÍA
==================================================

## 14. Cronología

Registrar los eventos relevantes del ticket.

Utilizar:

| Fecha | Evento | Responsable / área | Resultado |
|---|---|---|---|

Registrar únicamente eventos relevantes.

La cronología debe permitir reconstruir la evolución del caso.

==================================================
15. DECISIONES
==================================================

## 15. Decisiones

Registrar decisiones relevantes tomadas durante el ticket.

Utilizar:

DEC-TKT-01
DEC-TKT-02

Para cada decisión:

- decisión;
- motivo;
- evidencia;
- impacto;
- fecha.

No registrar opiniones como decisiones.


==================================================
16. CONCLUSIÓN
==================================================

## 16. Conclusión

Documentar el resultado general del ticket.

La conclusión debe distinguir:

- causa confirmada;
- solución aplicada;
- resultado;
- limitaciones;
- información pendiente.

No forzar una conclusión si el caso no fue resuelto.

Utilizar estados cuando corresponda:

- RESUELTO
- RESUELTO_PARCIALMENTE
- SIN_REPRODUCCION
- SIN_CAUSA_CONFIRMADA
- PENDIENTE
- CANCELADO


==================================================
17. SOLUCIÓN / ACCIÓN REALIZADA
==================================================

## 17. Solución / Acción realizada

Documentar brevemente qué se hizo para resolver o atender el caso.

Puede incluir:

- configuración;
- desarrollo;
- corrección;
- parametrización;
- cambio de proceso;
- reproceso;
- ajuste;
- documentación;
- capacitación;
- ninguna acción.

No convertir esta sección en especificación técnica.

Cuando exista una especificación funcional o documentación técnica, referenciarla.


==================================================
18. RESULTADO DE VALIDACIÓN
==================================================

## 18. Resultado de validación

Registrar si el resultado fue validado.

Utilizar:

- VALIDADO
- VALIDADO_PARCIALMENTE
- NO_VALIDADO
- BLOQUEADO
- NO_APLICA

Relacionar con:

templates/functional-tests.md

cuando existan pruebas formales.

No afirmar "VALIDADO" sin evidencia.


==================================================
19. INFORMACIÓN PENDIENTE
==================================================

## 19. Información pendiente

Registrar información que todavía necesita resolución.

Utilizar:

PEND-TKT-01
PEND-TKT-02

Tabla:

| ID | Información pendiente | Motivo | Acción requerida | Estado |
|---|---|---|---|---|

Si no existe:

"N/A"


==================================================
20. DOCUMENTACIÓN RELACIONADA
==================================================

## 20. Documentación relacionada

Relacionar el ticket con:

- otros tickets;
- requirements;
- specifications;
- tests;
- analyses;
- debug;
- investigations;
- SAP objects;
- processes;
- business rules;
- relationships.

Utilizar referencias reales.

==================================================
TRAZABILIDAD
==================================================

El ticket debe permitir reconstruir la cadena:

TICKET
  ↓
DOCUMENTACIÓN
  ↓
EVIDENCIA
  ↓
KNOWLEDGE
  ↓
CONCLUSIÓN

Y también:

KNOWLEDGE
  ↓
TICKETS
  ↓
CASOS REALES

Esto permitirá al futuro agente consultar tanto:

"¿Qué sabemos sobre este objeto?"

como:

"¿En qué tickets fue utilizado o investigado este objeto?"


==================================================
TICKET COMO FUENTE DE CONOCIMIENTO
==================================================

Un ticket puede generar nuevo conocimiento.

Por ejemplo:

TICKET
  ↓
DEBUG
  ↓
descubre comportamiento
  ↓
SAP OBJECT actualizado

O:

TICKET
  ↓
INVESTIGATION
  ↓
descubre regla
  ↓
BUSINESS RULE creada

O:

TICKET
  ↓
ANALYSIS
  ↓
descubre relación
  ↓
RELATIONSHIP creada

Por lo tanto, cerrar un ticket no significa que su conocimiento desaparezca.

El conocimiento relevante debe promoverse a FASE 3.


==================================================
TICKET COMO EVIDENCIA
==================================================

Un ticket puede utilizarse como evidencia de:

- comportamiento observado;
- configuración;
- relación;
- regla;
- proceso;
- problema;
- solución.

Pero un ticket no convierte automáticamente una afirmación en verdad general.

Ejemplo conceptual:

"En el ticket 33007 ocurrió X"

NO significa automáticamente:

"SAP siempre funciona de esta manera."

La generalización requiere evidencia adicional.


==================================================
DIFERENCIA ENTRE CASO Y CONOCIMIENTO
==================================================

CASO:

"En este ticket ocurrió X."

CONOCIMIENTO:

"El proceso se comporta de esta manera."

REGLA:

"Cuando se cumple esta condición, debe ocurrir X."

RELACIÓN:

"Objeto A está relacionado con objeto B de esta manera."

Mantener estas diferencias.


==================================================
HECHOS, HIPÓTESIS Y CONCLUSIONES
==================================================

Aplicar:

standards/documentation-standard.md

Distinguir claramente:

HECHO

Lo observado o confirmado.

HIPÓTESIS

Explicación propuesta todavía no confirmada.

INFORMACIÓN FALTANTE

Dato necesario que no está disponible.

CONCLUSIÓN

Resultado sustentado por la evidencia disponible.

No convertir hipótesis en hechos.


==================================================
SEGURIDAD
==================================================

Cumplir:

standards/security-standard.md

No almacenar:

- contraseñas;
- tokens;
- API keys;
- credenciales;
- claves privadas;
- secretos.

Minimizar:

- datos personales;
- datos financieros;
- datos productivos;
- información de proveedores o clientes.

Conservar solamente la información necesaria para comprender y resolver el caso.

Las capturas y evidencias deben ser sanitizadas.


==================================================
VERSIONADO
==================================================

Utilizar:

version: "1.0"

Aplicar:

PATCH:
Correcciones editoriales.

MINOR:
Información adicional que no modifica significativamente el caso.

MAJOR:
Cambio significativo en el contexto, conclusión, solución o interpretación del ticket.

No sobrescribir silenciosamente conclusiones anteriores.

Los cambios deben quedar trazables mediante Git.


==================================================
RELACIÓN CON LOS DOCUMENTOS DE FASE 2
==================================================

ticket.md debe actuar como índice, no como sustituto.

La relación conceptual es:

TICKET
│
├── REQUIREMENT
│
├── FUNCTIONAL SPECIFICATION
│
├── FUNCTIONAL TEST
│
├── ANALYSIS
│
├── DEBUG
│
└── INVESTIGATION

Cada documento mantiene su propia estructura y propósito.

ticket.md solamente debe:

- referenciarlo;
- indicar su estado;
- indicar su versión;
- resumir su función dentro del caso.


==================================================
PREPARACIÓN PARA IA
==================================================

La estructura debe permitir que el futuro agente responda preguntas como:

- ¿Qué ocurrió en este ticket?
- ¿Cuál fue el problema?
- ¿Cuál fue la causa?
- ¿Qué se investigó?
- ¿Qué se encontró?
- ¿Qué objetos SAP participaron?
- ¿Qué proceso estaba involucrado?
- ¿Qué reglas aplicaban?
- ¿Qué documentos fueron generados?
- ¿Qué pruebas se realizaron?
- ¿Cuál fue el resultado?
- ¿Qué información sigue pendiente?
- ¿Qué conocimiento nuevo produjo este ticket?
- ¿Qué otros tickets están relacionados?
- ¿Qué tickets anteriores trataron el mismo objeto?
- ¿Qué evidencia respalda la conclusión?

El agente debe poder navegar:

TICKET
→ DOCUMENTS
→ KNOWLEDGE
→ EVIDENCE
→ OTHER TICKETS


==================================================
REGLAS PARA EL AGENTE
==================================================

El agente que complete esta plantilla debe:

1. Buscar primero si el ticket ya existe.
2. No crear tickets duplicados.
3. Mantener ticket_id estable.
4. No utilizar ticket_id como identificador de objetos, procesos o reglas.
5. No duplicar documentos especializados.
6. Referenciar documentos mediante ruta y/o identificador.
7. Referenciar Knowledge mediante object_id, process_id, rule_id y relationship_id.
8. No crear relaciones por simple co-ocurrencia.
9. No convertir hipótesis en hechos.
10. No inventar evidencias.
11. No inventar conclusiones.
12. Registrar información pendiente.
13. Mantener cronología relevante.
14. Registrar decisiones importantes.
15. Promover conocimiento reutilizable hacia FASE 3.
16. Mantener historial mediante Git.
17. No eliminar silenciosamente información confirmada.
18. Mantener trazabilidad entre ticket, documentación y conocimiento.


==================================================
CRITERIO DE PROMOCIÓN A KNOWLEDGE
==================================================

No todo lo aprendido en un ticket debe convertirse automáticamente en conocimiento permanente.

Promover información a FASE 3 cuando:

- sea reutilizable;
- esté suficientemente confirmada;
- represente comportamiento general;
- represente una regla de negocio;
- represente un proceso;
- represente un objeto SAP;
- represente una relación válida.

No promover como conocimiento general:

- síntomas aislados;
- hipótesis;
- datos específicos sin valor reutilizable;
- información no confirmada;
- errores que solamente aplican a un caso particular.

Cuando exista duda, mantener la información dentro del ticket hasta obtener validación.


==================================================
FORMATO FINAL
==================================================

El archivo final debe ser una plantilla Markdown limpia, profesional y reutilizable.

Debe contener:

1. YAML front matter.
2. Título "# Ticket".
3. Metadata.
4. Las 20 secciones definidas.
5. Identificadores consistentes.
6. Tablas donde aporten estructura.
7. Comentarios HTML breves para orientar al usuario.
8. Ningún dato ficticio.
9. Ningún ticket real de ejemplo.
10. Ninguna conclusión inventada.
11. Ninguna evidencia inventada.
12. Compatibilidad con todos los standards existentes.
13. Compatibilidad con todos los templates de Fase 2.
14. Compatibilidad con todo el Knowledge Base de Fase 3.

No agregues secciones adicionales fuera de las definidas.

No generes ejemplos reales de tickets SAP.

No inventes información.

No expliques el proceso de creación.
