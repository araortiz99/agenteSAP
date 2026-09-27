Actúa como arquitecto de conocimiento, consultor funcional SAP senior y especialista en documentación técnica/funcional.

Debes crear el archivo:

standards/documentation-standard.md

para el repositorio `agenteSAP`.

## CONTEXTO DEL PROYECTO

`agenteSAP` será una base de conocimiento para un agente de IA que actuará como asistente de consultoría funcional SAP.

El agente no debe ejecutar ni modificar SAP inicialmente.

Su función principal será:

- leer documentación;
- analizar información;
- relacionar conocimiento;
- identificar antecedentes;
- analizar incidentes y mejoras;
- apoyar actividades de consultoría;
- analizar debugging;
- generar documentación funcional;
- generar pruebas funcionales;
- identificar información faltante;
- mantener trazabilidad;
- reutilizar conocimiento existente.

La calidad del agente dependerá directamente de la calidad y estructura de la documentación almacenada en el repositorio.

Por este motivo, este documento debe funcionar como el ESTÁNDAR DOCUMENTAL CENTRAL del proyecto.

---

# PRINCIPIO FUNDAMENTAL

La documentación debe permitir que una persona o un agente que no participó originalmente del análisis pueda comprender:

1. qué ocurrió;
2. qué se necesitaba;
3. qué se analizó;
4. qué evidencia se obtuvo;
5. qué se determinó;
6. qué solución se definió;
7. cómo se validó;
8. qué conocimiento puede reutilizarse posteriormente.

La documentación no debe depender exclusivamente del conocimiento tácito del analista que realizó el trabajo.

Priorizar:

1. precisión;
2. trazabilidad;
3. claridad;
4. contexto;
5. reutilización.

No agregar información únicamente para aumentar el volumen documental.

---

# 1. IDENTIFICADOR TRANSVERSAL

El elemento principal de trazabilidad es:

`ticket_id`

El `ticket_id` será el índice transversal de la documentación operativa.

Debe permitir relacionar:

- requerimientos;
- especificaciones funcionales;
- pruebas funcionales;
- análisis;
- debugging;
- investigaciones;
- objetos SAP;
- procesos;
- reglas de negocio;
- tickets relacionados;
- actividades de consultoría.

Un ticket puede representar:

- incidente;
- mejora;
- requerimiento;
- actividad de consultoría;
- análisis;
- investigación;
- debugging;
- validación.

IMPORTANTE:

El `ticket_id` es un índice de trazabilidad.

No debe considerarse necesariamente la única entidad de conocimiento.

Un mismo objeto SAP, proceso o regla de negocio puede estar relacionado con múltiples tickets.

---

# 2. MODELO DOCUMENTAL

La documentación debe dividirse en dos categorías.

## DOCUMENTACIÓN OFICIAL

Para incidentes y mejoras existen tres documentos base:

```text
DOCUMENTACIÓN OFICIAL

├── REQUERIMIENTO
├── ESPECIFICACIÓN FUNCIONAL
└── PRUEBAS FUNCIONALES
