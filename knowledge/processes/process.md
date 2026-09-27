Este archivo será la plantilla maestra para documentar PROCESOS SAP dentro del repositorio agenteSAP.

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

Ahora se debe crear la plantilla:

knowledge/processes/process.md

Esta plantilla permitirá documentar procesos funcionales y operativos de SAP como conocimiento permanente y reutilizable.

==================================================
OBJETIVO
==================================================

La plantilla debe permitir documentar un proceso SAP de manera estructurada, independiente de un ticket específico.

Debe responder principalmente:

- ¿Qué proceso es?
- ¿Cuál es su objetivo?
- ¿Cuándo comienza?
- ¿Cuándo termina?
- ¿Qué actores intervienen?
- ¿Qué precondiciones existen?
- ¿Cuáles son las etapas del proceso?
- ¿Qué documentos SAP intervienen?
- ¿Qué objetos SAP participan?
- ¿Qué reglas de negocio aplican?
- ¿Qué validaciones existen?
- ¿Qué integraciones intervienen?
- ¿Qué excepciones pueden ocurrir?
- ¿Qué evidencias sustentan el conocimiento?

La documentación debe representar conocimiento reutilizable.

No debe convertirse en:

- un ticket;
- una especificación funcional;
- un análisis de incidente;
- un debug;
- una guía de configuración;
- documentación técnica de código.

==================================================
PRINCIPIO FUNDAMENTAL
==================================================

Un proceso representa una secuencia funcional de actividades que transforma un estado inicial en un estado final.

Conceptualmente:

ESTADO INICIAL
      ↓
ACTIVIDAD
      ↓
DECISIÓN / VALIDACIÓN
      ↓
ACTIVIDAD
      ↓
DOCUMENTO / RESULTADO
      ↓
ESTADO FINAL

El proceso debe documentarse desde el punto de vista funcional.

Los detalles técnicos deben incorporarse solamente cuando sean necesarios para comprender el proceso y estén confirmados.

==================================================
METADATA
==================================================

El archivo debe comenzar obligatoriamente con YAML front matter:

---
process_id: ""
process_name: ""
process_type: ""
module: ""
version: "1.0"
status: "draft"
date: ""
author: ""
---

Luego:

# Proceso SAP

## Metadata

Utilizar una tabla:

| Campo | Valor |
|---|---|
| Process ID | |
| Nombre del proceso | |
| Tipo de proceso | |
| Módulo | |
| Versión | |
| Estado | |
| Fecha | |
| Autor | |

No inventar valores.

==================================================
PROCESS_ID
==================================================

Cada proceso debe tener un identificador estable.

Utilizar:

PROC-0001
PROC-0002
PROC-0003

El process_id identifica al proceso como conocimiento.

No utilizar ticket_id como identificador del proceso.

Un proceso puede estar relacionado con múltiples tickets.

==================================================
PROCESS_TYPE
==================================================

Registrar el tipo de proceso cuando corresponda.

Ejemplos:

- END_TO_END
- SUBPROCESS
- BUSINESS_PROCESS
- SAP_PROCESS
- INTEGRATION_PROCESS
- CONTROL_PROCESS
- REPORTING_PROCESS
- OTHER

No forzar una clasificación cuando no sea posible determinarla.

Si no está confirmado:

"UNKNOWN"

==================================================
1. IDENTIFICACIÓN
==================================================

## 1. Identificación

Documentar:

- nombre del proceso;
- process_id;
- tipo;
- módulo principal;
- módulos relacionados;
- proceso padre, si existe;
- subprocesos, si existen.

Indicar si se trata de:

- proceso estándar SAP;
- proceso configurado;
- proceso personalizado;
- proceso mixto;
- proceso interno de negocio integrado con SAP.

No asumir que un proceso es estándar SAP únicamente porque utilice funcionalidades estándar.


==================================================
2. OBJETIVO
==================================================

## 2. Objetivo

Explicar qué resultado busca alcanzar el proceso.

Debe responder:

¿Qué necesidad funcional resuelve?

El objetivo debe describir el resultado del proceso, no una implementación técnica.


==================================================
3. ALCANCE
==================================================

## 3. Alcance

Definir:

- qué incluye el proceso;
- qué áreas participan;
- qué sociedades, centros, almacenes u organizaciones pueden estar involucrados cuando corresponda;
- qué parte del ciclo funcional está cubierta.

También indicar explícitamente qué queda fuera del proceso.

Si no existe información suficiente:

"Alcance pendiente de validar."


==================================================
4. INICIO Y FIN DEL PROCESO
==================================================

## 4. Inicio y fin del proceso

Documentar:

### Evento de inicio

¿Qué condición, evento o acción inicia el proceso?

### Evento de finalización

¿Qué condición indica que el proceso terminó correctamente?

### Resultado final

¿Qué estado, documento o resultado queda generado?

Debe distinguirse:

- evento de inicio;
- primera actividad;
- resultado final;
- evento de cierre.

No asumir que la ejecución de una transacción equivale al inicio o fin del proceso.


==================================================
5. ACTORES
==================================================

## 5. Actores

Documentar los participantes del proceso.

Pueden incluir:

- usuario de negocio;
- comprador;
- encargado de tienda;
- depósito;
- administración;
- finanzas;
- proveedor;
- sistema SAP;
- sistema externo;
- proceso automático;
- job.

Utilizar una tabla:

| ID | Actor | Rol en el proceso | Participación |
|---|---|---|---|

Utilizar:

ACT-01
ACT-02
ACT-03

No inventar roles.


==================================================
6. PRECONDICIONES
==================================================

## 6. Precondiciones

Documentar las condiciones necesarias antes de iniciar el proceso.

Pueden incluir:

- datos maestros;
- documentos previos;
- configuración;
- stock;
- autorizaciones;
- estados;
- parámetros;
- interfaces;
- información externa.

Utilizar identificadores:

PRE-01
PRE-02

Cada precondición debe poder validarse.


==================================================
7. FLUJO DEL PROCESO
==================================================

## 7. Flujo del proceso

Esta es una de las secciones principales.

Documentar el proceso como una secuencia de pasos.

Utilizar identificadores:

STEP-01
STEP-02
STEP-03

Utilizar una tabla:

| Paso | Actividad | Responsable | Entrada | Resultado | Objeto SAP relacionado |
|---|---|---|---|---|---|

Cada paso debe describir:

- qué ocurre;
- quién lo realiza;
- qué información utiliza;
- qué resultado produce;
- qué objeto SAP interviene, si está confirmado.

No convertir cada paso en instrucciones técnicas detalladas.

El flujo debe representar comportamiento funcional.


==================================================
8. DECISIONES Y VALIDACIONES
==================================================

## 8. Decisiones y validaciones

Documentar los puntos del proceso donde existe una decisión o validación.

Utilizar:

DEC-01
DEC-02

Estructura:

| ID | Punto del proceso | Condición | Si cumple | Si no cumple |
|---|---|---|---|---|

Las condiciones deben corresponder a reglas o validaciones conocidas.

No inventar criterios.


==================================================
9. DOCUMENTOS SAP
==================================================

## 9. Documentos SAP

Documentar los documentos SAP generados, utilizados o modificados durante el proceso.

Pueden incluir:

- pedido;
- entrega;
- documento de material;
- documento contable;
- factura;
- nota de crédito;
- documento de inventario;
- documento de compra;
- documento de venta;
- otros.

Utilizar:

| ID | Documento | Momento del proceso | Generado / utilizado / modificado | Observación |
|---|---|---|---|---|

No inventar documentos.


==================================================
10. OBJETOS SAP RELACIONADOS
==================================================

## 10. Objetos SAP relacionados

Relacionar el proceso con objetos documentados en:

knowledge/sap-objects/

Pueden incluir:

- transacciones;
- tablas;
- programas;
- clases;
- funciones;
- BAPIs;
- BADIs;
- movimientos;
- Fiori Apps;
- roles;
- catálogos;
- servicios;
- integraciones.

Utilizar una tabla:

| Object ID | Nombre técnico | Tipo | Uso dentro del proceso |
|---|---|---|---|

Cuando el objeto todavía no tenga documentación propia:

"Objeto identificado — documentación pendiente."

No inventar object_id.


==================================================
11. REGLAS DE NEGOCIO
==================================================

## 11. Reglas de negocio

Relacionar el proceso con reglas documentadas en:

knowledge/business-rules/

Utilizar:

| Rule ID | Regla | Momento de aplicación | Impacto |
|---|---|---|---|

No duplicar innecesariamente el contenido completo de la regla.

La fuente principal debe ser el business-rule correspondiente cuando exista.

Si una regla todavía no está formalizada:

"Regla identificada — documentación pendiente."


==================================================
12. DATOS Y OBJETOS DE INFORMACIÓN
==================================================

## 12. Datos y objetos de información

Documentar la información relevante para el proceso.

Puede incluir:

- material;
- proveedor;
- cliente;
- centro;
- almacén;
- sociedad;
- organización de compras;
- pedido;
- lote;
- cantidad;
- importe;
- fecha;
- documento;
- estado.

Utilizar una tabla:

| Dato | Descripción | Origen | Utilización | Resultado |
|---|---|---|---|---|

No documentar datos sensibles innecesarios.


==================================================
13. INTEGRACIONES
==================================================

## 13. Integraciones

Documentar sistemas externos o internos que participan en el proceso.

Utilizar:

| ID | Sistema | Dirección | Momento | Propósito | Evidencia |
|---|---|---|---|---|---|

Dirección puede indicar, cuando esté confirmado:

- SAP → Sistema externo
- Sistema externo → SAP
- Bidireccional

No inventar interfaces.

==================================================
14. ESTADOS DEL PROCESO
==================================================

## 14. Estados del proceso

Cuando corresponda, documentar los estados relevantes.

Ejemplo conceptual de estructura:

| Estado | Descripción | Entrada | Salida / transición |
|---|---|---|---|

Utilizar identificadores:

STATE-01
STATE-02

No asumir que todos los procesos tienen estados explícitos.


==================================================
15. EXCEPCIONES
==================================================

## 15. Excepciones

Documentar situaciones en las que el proceso no sigue el flujo normal.

Utilizar:

EXC-01
EXC-02

Para cada excepción:

- condición;
- paso afectado;
- comportamiento observado;
- resultado;
- tratamiento conocido.

No inventar tratamientos.

Si la resolución no está documentada:

"Tratamiento pendiente de validar."


==================================================
16. CONTROLES
==================================================

## 16. Controles

Documentar controles funcionales relevantes.

Pueden incluir:

- validaciones;
- autorizaciones;
- controles de cantidades;
- controles de estados;
- controles contables;
- controles de duplicidad;
- controles de integración;
- controles de consistencia.

Utilizar:

CTRL-01
CTRL-02

Relacionar el control con una regla o validación cuando exista.


==================================================
17. RESULTADOS
==================================================

## 17. Resultados

Documentar los resultados esperados del proceso.

Pueden incluir:

- documentos generados;
- actualizaciones;
- movimientos;
- contabilizaciones;
- estados finales;
- información enviada a otros sistemas;
- reportes;
- registros de control.

Distinguir entre:

RESULTADO ESPERADO

y:

RESULTADO OBSERVADO

cuando el conocimiento provenga de una investigación o caso real.


==================================================
18. EVIDENCIAS
==================================================

## 18. Evidencias

Registrar las fuentes que sustentan la descripción del proceso.

Utilizar:

EVID-PROC-01
EVID-PROC-02

Las evidencias pueden provenir de:

- documentación oficial SAP;
- configuración;
- documentos del sistema;
- análisis;
- debug;
- investigación;
- pruebas funcionales;
- especificaciones;
- tickets;
- documentación interna.

Utilizar:

| ID | Fuente | Tipo | Qué demuestra |
|---|---|---|---|

No inventar evidencias.


==================================================
19. RELACIONES
==================================================

## 19. Relaciones

Relacionar el proceso con otros elementos del knowledge base.

Las relaciones formales deben documentarse también en:

knowledge/relationships/

Esta sección puede utilizarse para referenciar relaciones relevantes.

Ejemplos:

PROCESO
→ utiliza → OBJETO SAP

PROCESO
→ aplica → REGLA

PROCESO
→ contiene → SUBPROCESO

PROCESO
→ integra con → SISTEMA

No duplicar innecesariamente la definición de las relaciones.


==================================================
20. INFORMACIÓN PENDIENTE
==================================================

## 20. Información pendiente

Registrar aspectos del proceso que todavía necesitan validación.

Utilizar:

PEND-PROC-01
PEND-PROC-02

Tabla:

| ID | Información pendiente | Motivo | Acción requerida |
|---|---|---|---|

Si no existe información pendiente:

"N/A"


==================================================
21. DOCUMENTACIÓN RELACIONADA
==================================================

## 21. Documentación relacionada

Relacionar el proceso con:

- requirements;
- functional specifications;
- functional tests;
- analysis;
- debug;
- investigations;
- business rules;
- SAP objects;
- relationships;
- tickets.

Utilizar referencias reales.

No inventar documentos.


==================================================
ESTÁNDAR VS PERSONALIZACIÓN
==================================================

La documentación debe distinguir claramente:

SAP STANDARD

Proceso entregado por SAP.

CONFIGURED

Proceso estándar adaptado mediante configuración.

CUSTOM

Proceso implementado mediante desarrollo o personalización.

MIXED

Proceso que combina estándar, configuración, desarrollos propios o integraciones.

UNKNOWN

Origen no confirmado.

No clasificar un proceso como estándar simplemente porque utilice transacciones estándar.


==================================================
HECHOS VS INTERPRETACIÓN
==================================================

La documentación debe seguir:

standards/documentation-standard.md

Distinguir:

HECHO

Información confirmada mediante evidencia.

HIPÓTESIS

Interpretación todavía no confirmada.

INFORMACIÓN FALTANTE

Dato necesario que todavía no está disponible.

CONCLUSIÓN

Resultado obtenido a partir de la información disponible.

No presentar hipótesis como comportamiento confirmado del proceso.


==================================================
NIVEL DE CONOCIMIENTO
==================================================

El proceso debe indicar el estado de conocimiento:

- CONFIRMADO
- PARCIAL
- EN VALIDACIÓN
- NO CONFIRMADO

Cuando diferentes partes del proceso tengan distintos niveles de certeza, indicarlo específicamente.


==================================================
RELACIÓN CON TICKETS
==================================================

Un proceso es conocimiento permanente.

Un ticket representa un caso particular.

Por lo tanto:

process_id = identidad del proceso

ticket_id = caso donde el proceso fue utilizado, analizado, modificado o investigado.

No utilizar ticket_id como sustituto de process_id.

Un mismo proceso puede estar relacionado con múltiples tickets.


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
- secretos;
- información personal innecesaria.

Los datos productivos deben minimizarse.

Los identificadores técnicos SAP pueden conservarse cuando sean necesarios para comprender el proceso.


==================================================
VERSIONADO
==================================================

Utilizar:

version: "1.0"

Aplicar:

PATCH:
Correcciones editoriales.

MINOR:
Información adicional que no cambia sustancialmente el modelo del proceso.

MAJOR:
Cambio significativo en el flujo, alcance, reglas o comportamiento del proceso.

No eliminar silenciosamente conocimiento confirmado.


==================================================
PREPARACIÓN PARA IA
==================================================

La estructura debe permitir que un futuro agente responda preguntas como:

- ¿Cómo funciona este proceso?
- ¿Cuál es el objetivo?
- ¿Cómo comienza?
- ¿Cómo termina?
- ¿Qué pasos tiene?
- ¿Qué transacciones intervienen?
- ¿Qué tablas están relacionadas?
- ¿Qué documentos SAP genera?
- ¿Qué reglas de negocio aplican?
- ¿Qué validaciones existen?
- ¿Qué excepciones pueden ocurrir?
- ¿Qué sistemas externos intervienen?
- ¿Qué procesos anteriores o posteriores están relacionados?
- ¿Qué tickets documentan problemas de este proceso?
- ¿Qué información está confirmada?
- ¿Qué información todavía debe validarse?

Por esta razón:

- utilizar identificadores estables;
- mantener relaciones explícitas;
- utilizar nombres técnicos confirmados;
- separar proceso de implementación;
- separar estándar de personalización;
- conservar evidencias;
- registrar incertidumbre.


==================================================
REGLAS PARA EL AGENTE
==================================================

El agente que complete esta plantilla debe:

1. Buscar primero si el proceso ya existe.
2. Evitar crear procesos duplicados.
3. Reutilizar process_id cuando el proceso ya exista.
4. Diferenciar proceso de subproceso.
5. No crear un nuevo proceso solamente porque exista un nuevo ticket.
6. Mantener relaciones existentes.
7. Agregar nuevas evidencias.
8. Registrar cambios relevantes del proceso.
9. Identificar contradicciones.
10. No inventar pasos.
11. No inventar reglas.
12. No inventar objetos SAP.
13. No inventar integraciones.
14. No asumir comportamiento estándar.
15. Registrar información pendiente.
16. Mantener trazabilidad mediante Git.


==================================================
RELACIÓN CON SAP OBJECTS
==================================================

Los procesos deben referenciar objetos SAP mediante object_id cuando estos ya estén documentados.

Ejemplo conceptual:

PROC-0001
    |
    +--- utiliza ---> OBJ-0001
    |
    +--- utiliza ---> OBJ-0005
    |
    +--- aplica ----> BR-0003

No copiar toda la información del objeto dentro del proceso.

La información debe mantenerse normalizada:

Objeto → documentado en sap-objects

Proceso → documentado en processes

Regla → documentada en business-rules

Relación → documentada en relationships


==================================================
FORMATO FINAL
==================================================

El archivo final debe ser una plantilla Markdown limpia, profesional y reutilizable.

Debe contener:

1. YAML front matter.
2. Título "# Proceso SAP".
3. Metadata.
4. Las 21 secciones definidas.
5. Identificadores consistentes.
6. Tablas donde aporten estructura.
7. Comentarios HTML breves para orientar al usuario.
8. Ningún dato ficticio.
9. Ningún proceso SAP de ejemplo.
10. Ninguna regla inventada.
11. Ningún objeto SAP inventado.
12. Ninguna relación inventada.
13. Compatibilidad con los standards existentes.
14. Compatibilidad con templates existentes.
15. Compatibilidad con knowledge/sap-objects/object.md.

No agregues secciones adicionales fuera de las definidas.

No generes ejemplos de procesos reales.

No inventes información SAP.

No expliques el proceso de creación.
