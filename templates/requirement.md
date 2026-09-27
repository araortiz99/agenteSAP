Actúa como consultor funcional SAP senior, arquitecto de conocimiento y especialista en diseño de documentación funcional para sistemas empresariales y agentes de IA.

Tu tarea es generar ÚNICAMENTE el archivo:

templates/requirement.md

Este archivo será el TEMPLATE OFICIAL para documentos de tipo:

document_type: requirement

del repositorio `agenteSAP`.

==================================================
1. ESTÁNDARES OBLIGATORIOS
==================================================

El template debe cumplir y ser compatible con:

- standards/documentation-standard.md
- standards/versioning-standard.md
- standards/security-standard.md

Estos documentos son normativos.

No debes redefinir sus reglas ni contradecirlas.

La responsabilidad de este template es únicamente definir la estructura práctica que se utilizará para crear un documento de tipo `requirement`.

Diferencia de responsabilidades:

documentation-standard.md
→ Define las reglas generales de documentación.

versioning-standard.md
→ Define cómo evolucionan y se versionan los documentos.

security-standard.md
→ Define cómo se protege y sanitiza la información.

templates/requirement.md
→ Define la estructura que debe utilizar un requerimiento.

==================================================
2. OBJETIVO
==================================================

El template debe permitir documentar una necesidad funcional SAP de forma:

- clara;
- estructurada;
- trazable;
- verificable;
- reutilizable;
- comprensible por humanos;
- interpretable por agentes de IA.

El requerimiento debe permitir comprender:

1. por qué existe la necesidad;
2. cuál es la situación actual;
3. cuál es el problema;
4. qué necesita el negocio;
5. qué objetivo se busca;
6. qué está incluido;
7. qué está excluido;
8. qué impacto funcional existe;
9. cómo se determinará que el requerimiento fue satisfecho;
10. qué información todavía falta.

==================================================
3. PRINCIPIO FUNCIONAL
==================================================

El requerimiento debe describir:

QUÉ necesita el negocio.

No debe definir prematuramente:

CÓMO será implementado técnicamente.

Por lo tanto, el template NO debe exigir:

- código ABAP;
- diseño técnico;
- estructuras internas;
- clases;
- métodos;
- lógica de programación;
- diseño de tablas;
- arquitectura técnica;
- solución técnica no aprobada.

Los objetos SAP pueden mencionarse cuando sean relevantes para comprender el contexto, pero su presencia no implica que constituyan la solución técnica.

==================================================
4. METADATA
==================================================

El documento generado mediante este template debe comenzar exactamente con:

---
ticket_id: ""
document_type: "requirement"
version: "1.0"
status: "draft"
date: ""
author: ""
---

Estos campos son obligatorios según `standards/documentation-standard.md`.

No agregar nuevos campos obligatorios.

Si el requerimiento no está asociado a un ticket:

ticket_id: "N/A"

No inventar valores.

La metadata debe mantenerse consistente durante toda la vida del documento.

==================================================
5. ESTRUCTURA OBLIGATORIA
==================================================

Después del Front Matter, utilizar exactamente:

# Requerimiento

## Metadata

## 1. Antecedente

## 2. Situación actual

## 3. Necesidad / Problema

## 4. Objetivo

## 5. Alcance

## 6. Fuera de alcance

## 7. Impacto funcional

## 8. Criterios de aceptación

## 9. Información adicional

## 10. Documentación relacionada

No agregar secciones adicionales salvo que posteriormente el estándar de documentación las defina.

==================================================
6. METADATA VISIBLE
==================================================

La sección:

## Metadata

debe representar de forma legible el Front Matter.

Utilizar:

| Campo | Valor |
|---|---|
| Ticket ID | |
| Tipo de documento | requirement |
| Versión | 1.0 |
| Estado | draft |
| Fecha | |
| Autor | |

La metadata visible no debe introducir información diferente al Front Matter.

==================================================
7. ANTECEDENTE
==================================================

## 1. Antecedente

Debe documentar el contexto que originó la necesidad.

Puede incluir:

- incidente;
- proyecto;
- mejora;
- solicitud de usuario;
- cambio de proceso;
- necesidad de negocio;
- situación histórica relevante.

Debe responder:

"¿Qué contexto originó este requerimiento?"

No debe definir todavía la solución.

Utilizar como instrucción:

<!-- Describir el contexto que origina el requerimiento y los antecedentes relevantes. -->

==================================================
8. SITUACIÓN ACTUAL
==================================================

## 2. Situación actual

Debe describir cómo funciona actualmente el proceso.

Cuando corresponda, documentar:

- proceso;
- subproceso;
- usuarios;
- áreas;
- sistemas;
- transacciones;
- documentos;
- objetos SAP;
- integraciones;
- comportamiento actual;
- restricciones conocidas.

Debe diferenciar:

COMPORTAMIENTO ACTUAL

de

PROBLEMA / NECESIDAD.

Utilizar:

<!-- Describir el comportamiento actual y los elementos relevantes del proceso. No definir todavía la solución propuesta. -->

==================================================
9. NECESIDAD / PROBLEMA
==================================================

## 3. Necesidad / Problema

Debe expresar de forma concreta qué problema o necesidad debe resolverse.

Debe responder:

- ¿Qué problema existe?
- ¿Quién se ve afectado?
- ¿En qué escenario?
- ¿Cuál es la consecuencia funcional?
- ¿Qué necesidad debe satisfacerse?

Evitar expresiones genéricas como:

"Mejorar el proceso."

"Corregir SAP."

"Hacer más rápido."

La descripción debe ser suficientemente precisa para que otro consultor comprenda el problema sin consultar la conversación original.

Utilizar:

<!-- Describir el problema o necesidad de negocio de forma concreta y verificable. -->

==================================================
10. OBJETIVO
==================================================

## 4. Objetivo

Debe expresar el resultado funcional que se desea alcanzar.

Debe responder:

"¿Qué debe lograrse?"

No:

"¿Cómo debe programarse?"

El objetivo debe ser:

- específico;
- comprensible;
- verificable;
- orientado al resultado funcional.

Utilizar:

<!-- Describir el resultado funcional que se espera alcanzar. -->

==================================================
11. ALCANCE
==================================================

## 5. Alcance

Debe definir explícitamente qué forma parte del requerimiento.

Cuando corresponda considerar:

- procesos;
- subprocesos;
- áreas;
- usuarios;
- sociedades;
- centros;
- almacenes;
- documentos;
- escenarios;
- funcionalidades.

Utilizar:

### Incluye

- 
- 
- 

No inventar elementos.

Utilizar:

<!-- Indicar qué procesos, escenarios, usuarios o funcionalidades forman parte del requerimiento. -->

==================================================
12. FUERA DE ALCANCE
==================================================

## 6. Fuera de alcance

Debe identificar explícitamente qué NO forma parte del requerimiento.

Utilizar:

### No incluye

- 
- 
- 

Si todavía no fue definido:

Pendiente de definición.

El objetivo es evitar interpretaciones posteriores sobre funcionalidades no solicitadas.

Utilizar:

<!-- Indicar qué elementos quedan explícitamente fuera del alcance. -->

==================================================
13. IMPACTO FUNCIONAL
==================================================

## 7. Impacto funcional

Debe identificar los impactos conocidos o potenciales sobre:

- procesos;
- subprocesos;
- usuarios;
- áreas;
- documentos SAP;
- datos;
- integraciones;
- controles;
- reportes;
- procesos posteriores.

Utilizar:

### Procesos afectados

-

### Usuarios / áreas afectadas

-

### Datos / documentos afectados

-

### Integraciones afectadas

-

### Otros impactos

-

No realizar aquí un análisis técnico detallado.

Si un impacto es una hipótesis, debe identificarse como tal.

Utilizar:

<!-- Documentar los impactos funcionales identificados. Diferenciar impactos confirmados de impactos pendientes de validar. -->

==================================================
14. CRITERIOS DE ACEPTACIÓN
==================================================

## 8. Criterios de aceptación

Debe definir condiciones objetivas y verificables para determinar si el requerimiento fue satisfecho.

Utilizar:

### CA-01

Descripción:

### CA-02

Descripción:

### CA-03

Descripción:

Los criterios deben ser:

- claros;
- específicos;
- verificables;
- orientados al comportamiento funcional.

Deben poder utilizarse posteriormente como base para pruebas funcionales.

Evitar criterios subjetivos como:

"El sistema debe funcionar correctamente."

Preferir condiciones observables.

Utilizar:

<!-- Definir condiciones funcionales objetivas que permitan determinar si el requerimiento fue cumplido. -->

==================================================
15. INFORMACIÓN ADICIONAL
==================================================

## 9. Información adicional

Debe contener información relevante que no corresponda a las secciones anteriores.

Puede incluir:

- restricciones;
- supuestos;
- dependencias preliminares;
- observaciones;
- información faltante;
- puntos pendientes de definición.

Cuando corresponda utilizar:

### Información faltante

-

### Pendiente de definición

-

### Hipótesis

-

No presentar hipótesis como hechos confirmados.

Utilizar:

<!-- Registrar restricciones, supuestos, información faltante y puntos pendientes. Diferenciar hechos de hipótesis. -->

==================================================
16. DOCUMENTACIÓN RELACIONADA
==================================================

## 10. Documentación relacionada

Debe permitir conectar el requerimiento con conocimiento existente.

Utilizar:

### Tickets relacionados

-

### Documentos relacionados

-

### Análisis relacionados

-

### Investigaciones relacionadas

-

### Procesos relacionados

-

### Objetos SAP relacionados

-

No inventar referencias.

Cuando no exista documentación relacionada:

No identificada.

Utilizar:

<!-- Referenciar únicamente documentación, procesos u objetos SAP existentes y confirmados. -->

==================================================
17. HECHOS, HIPÓTESIS E INFORMACIÓN FALTANTE
==================================================

El template debe ser compatible con la clasificación establecida en:

standards/documentation-standard.md

Debe poder distinguir:

HECHO
→ información confirmada mediante evidencia.

HIPÓTESIS
→ interpretación aún no confirmada.

INFORMACIÓN FALTANTE
→ información necesaria que todavía no está disponible.

CONCLUSIÓN
→ resultado basado en evidencia.

Un requerimiento no debe presentar una interpretación como hecho confirmado sin evidencia suficiente.

==================================================
18. REGLA CONTRA LA INVENCIÓN
==================================================

Cuando la información necesaria no esté disponible:

NO INVENTAR.

Utilizar expresiones como:

- Pendiente de definición.
- Información faltante.
- No confirmado.
- Requiere validación.
- No aplica.

Nunca inventar:

- transacciones;
- tablas;
- campos;
- programas;
- clases;
- funciones;
- procesos;
- reglas;
- usuarios;
- sociedades;
- centros;
- documentos;
- integraciones;
- configuraciones.

Los nombres técnicos SAP deben conservarse exactamente cuando hayan sido confirmados.

==================================================
19. SEGURIDAD
==================================================

El template debe cumplir:

standards/security-standard.md

No incorporar:

- contraseñas;
- tokens;
- API keys;
- credenciales;
- claves privadas;
- datos personales innecesarios;
- información financiera innecesaria;
- datos productivos innecesarios;
- información confidencial sin utilidad funcional.

Los identificadores SAP pueden conservarse cuando sean necesarios para la trazabilidad.

La sanitización no debe destruir el contexto necesario para comprender el requerimiento.

==================================================
20. VERSIONADO
==================================================

El template debe cumplir:

standards/versioning-standard.md

La versión inicial será:

version: "1.0"

Los cambios posteriores deben gestionarse conforme al estándar de versionado.

No modificar silenciosamente una versión histórica.

==================================================
21. USO POR EL AGENTE DE IA
==================================================

Cuando el agente utilice este template deberá seguir este flujo:

1. Identificar el ticket.
2. Identificar el contexto.
3. Extraer la situación actual.
4. Identificar el problema o necesidad.
5. Determinar el objetivo.
6. Delimitar el alcance.
7. Identificar el fuera de alcance.
8. Identificar impactos.
9. Definir criterios de aceptación únicamente con información suficiente.
10. Identificar información faltante.
11. Buscar documentación relacionada.
12. Validar que no se inventó información.
13. Aplicar las reglas de seguridad.
14. Mantener la metadata consistente.

Si existe información insuficiente, debe indicarse explícitamente.

No completar vacíos mediante suposiciones.

==================================================
22. REGLA DE SEPARACIÓN FUNCIONAL
==================================================

El agente debe mantener separadas:

NECESIDAD

OBJETIVO

ALCANCE

CRITERIOS DE ACEPTACIÓN

SOLUCIÓN TÉCNICA

La solución técnica pertenece a la especificación funcional o documentación técnica correspondiente.

No introducir una solución técnica simplemente porque parece conveniente.

==================================================
23. CRITERIO DE CALIDAD
==================================================

Un requerimiento completado mediante este template debe permitir que un consultor que no participó en la conversación original pueda comprender:

- el contexto;
- la situación actual;
- el problema;
- la necesidad;
- el objetivo;
- el alcance;
- el fuera de alcance;
- el impacto;
- los criterios de aceptación;
- la información faltante;
- las relaciones existentes.

El documento debe ser suficientemente completo para iniciar posteriormente una especificación funcional.

==================================================
24. FORMATO FINAL DEL TEMPLATE
==================================================

El archivo generado debe comenzar exactamente con:

---
ticket_id: ""
document_type: "requirement"
version: "1.0"
status: "draft"
date: ""
author: ""
---

Después debe contener:

# Requerimiento

## Metadata

## 1. Antecedente

## 2. Situación actual

## 3. Necesidad / Problema

## 4. Objetivo

## 5. Alcance

## 6. Fuera de alcance

## 7. Impacto funcional

## 8. Criterios de aceptación

## 9. Información adicional

## 10. Documentación relacionada

Cada sección debe contener instrucciones breves mediante comentarios HTML y espacios/listas preparados para completar.

NO incluir:

- tickets ficticios;
- usuarios ficticios;
- sociedades ficticias;
- centros ficticios;
- objetos SAP ficticios;
- datos ficticios;
- ejemplos de negocio completos.

El template debe ser una plantilla, no un documento de ejemplo.

==================================================
25. REGLA FINAL DE GENERACIÓN
==================================================

Genera ÚNICAMENTE:

templates/requirement.md

No generar otros archivos.

No modificar otros archivos.

No generar documentación adicional.

No incluir explicaciones fuera del archivo.

El resultado debe estar listo para incorporarse directamente al repositorio `agenteSAP`.
