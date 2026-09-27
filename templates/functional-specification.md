Actúa como consultor funcional SAP senior, arquitecto de conocimiento y especialista en diseño de especificaciones funcionales para sistemas empresariales y agentes de IA.

Tu tarea es generar ÚNICAMENTE el archivo:

templates/functional-specification.md

Este archivo será el TEMPLATE OFICIAL para documentos de tipo:

document_type: functional-specification

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

La responsabilidad de este archivo es únicamente definir la estructura práctica para documentar una especificación funcional SAP.

Diferencia de responsabilidades:

documentation-standard.md
→ Define las reglas generales de documentación.

versioning-standard.md
→ Define cómo evolucionan y se versionan los documentos.

security-standard.md
→ Define cómo se protege y sanitiza la información.

templates/functional-specification.md
→ Define la estructura que debe utilizar una especificación funcional.

==================================================
2. OBJETIVO
==================================================

El template debe permitir transformar una necesidad o requerimiento funcional en una definición funcional suficientemente clara para:

- usuarios funcionales;
- desarrolladores;
- QA;
- consultores SAP;
- equipos de integración;
- futuros agentes de IA.

La especificación debe permitir comprender:

1. qué problema origina la solución;
2. qué debe hacer funcionalmente;
3. cómo debe comportarse;
4. bajo qué condiciones;
5. qué reglas de negocio debe respetar;
6. qué validaciones deben existir;
7. qué escenarios deben contemplarse;
8. qué datos intervienen;
9. qué objetos SAP están relacionados;
10. qué integraciones existen;
11. qué impactos deben considerarse;
12. qué dependencias existen;
13. qué riesgos deben considerarse;
14. cómo se determinará que la solución cumple lo solicitado;
15. cómo deberá ser validada funcionalmente.

==================================================
3. PRINCIPIO FUNDAMENTAL
==================================================

La especificación funcional debe responder:

¿QUÉ DEBE HACER LA SOLUCIÓN Y BAJO QUÉ CONDICIONES?

No debe confundirse con:

REQUERIMIENTO
→ qué necesita el negocio.

ESPECIFICACIÓN FUNCIONAL
→ cómo debe comportarse funcionalmente la solución.

ESPECIFICACIÓN TÉCNICA
→ cómo se implementará técnicamente.

Por lo tanto, la especificación puede describir:

- comportamiento;
- lógica funcional;
- reglas;
- validaciones;
- escenarios;
- datos;
- documentos;
- objetos SAP relacionados;
- interfaces;
- condiciones;
- resultados esperados.

Pero no debe inventar detalles técnicos de implementación.

==================================================
4. METADATA
==================================================

El documento generado mediante este template debe comenzar exactamente con:

---
ticket_id: ""
document_type: "functional-specification"
version: "1.0"
status: "draft"
date: ""
author: ""
---

Estos campos son obligatorios según:

standards/documentation-standard.md

Si no existe un ticket:

ticket_id: "N/A"

No inventar valores.

La metadata debe permanecer consistente durante toda la vida del documento.

==================================================
5. ESTRUCTURA OBLIGATORIA
==================================================

Después del Front Matter, utilizar exactamente:

# Especificación Funcional

## Metadata

## 1. Antecedente

## 2. Motivo

## 3. Objetivo

## 4. Alcance

## 5. Situación actual

## 6. Solución funcional propuesta

## 7. Flujo funcional

## 8. Reglas de negocio

## 9. Validaciones

## 10. Escenarios

## 11. Datos involucrados

## 12. Objetos SAP relacionados

## 13. Integraciones

## 14. Impactos

## 15. Dependencias

## 16. Riesgos

## 17. Criterios de aceptación

## 18. Consideraciones para pruebas

## 19. Documentación relacionada

No agregar secciones adicionales salvo que el estándar de documentación sea posteriormente modificado.

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
| Tipo de documento | functional-specification |
| Versión | 1.0 |
| Estado | draft |
| Fecha | |
| Autor | |

La metadata visible y el Front Matter deben permanecer consistentes.

==================================================
7. ANTECEDENTE
==================================================

## 1. Antecedente

Debe explicar el contexto que origina la especificación funcional.

Cuando exista un requerimiento relacionado, debe poder referenciarse.

Puede incluir:

- incidente;
- proyecto;
- mejora;
- requerimiento;
- análisis;
- decisión funcional;
- situación histórica.

Debe responder:

"¿Por qué existe esta especificación?"

Utilizar:

<!-- Describir el contexto que origina la especificación funcional y referenciar el requerimiento o antecedente correspondiente cuando exista. -->

==================================================
8. MOTIVO
==================================================

## 2. Motivo

Debe explicar por qué se requiere implementar o modificar la funcionalidad.

Debe diferenciar:

ANTECEDENTE
→ contexto.

MOTIVO
→ razón funcional para realizar el cambio.

Puede incluir:

- problema detectado;
- necesidad de negocio;
- limitación actual;
- cambio de proceso;
- cumplimiento de una regla;
- necesidad de control;
- necesidad de trazabilidad.

Utilizar:

<!-- Describir la razón funcional que motiva la solución. -->

==================================================
9. OBJETIVO
==================================================

## 3. Objetivo

Debe describir qué resultado funcional debe alcanzar la solución.

Debe estar alineado con el requerimiento correspondiente.

Debe responder:

"¿Qué comportamiento o resultado debe obtener el usuario o proceso después de implementar la solución?"

Utilizar:

<!-- Describir el objetivo funcional de la solución. -->

==================================================
10. ALCANCE
==================================================

## 4. Alcance

Debe definir exactamente qué funcionalidades forman parte de esta especificación.

Considerar cuando corresponda:

- procesos;
- subprocesos;
- usuarios;
- áreas;
- sociedades;
- centros;
- almacenes;
- documentos;
- escenarios;
- transacciones;
- aplicaciones;
- integraciones.

Utilizar:

### Incluye

- 
- 
- 

### Fuera de alcance

- 
- 
- 

El alcance de la especificación debe ser consistente con el requerimiento asociado.

==================================================
11. SITUACIÓN ACTUAL
==================================================

## 5. Situación actual

Debe documentar el comportamiento existente antes de implementar la solución.

Puede incluir:

- flujo actual;
- actores;
- documentos;
- transacciones;
- objetos SAP;
- datos;
- controles;
- integraciones;
- limitaciones;
- errores conocidos.

Debe diferenciar:

COMPORTAMIENTO ACTUAL

de

SOLUCIÓN PROPUESTA.

Utilizar:

<!-- Describir cómo funciona actualmente el proceso y qué limitaciones justifican la solución. -->

==================================================
12. SOLUCIÓN FUNCIONAL PROPUESTA
==================================================

## 6. Solución funcional propuesta

Esta es una de las secciones principales del documento.

Debe describir cómo debe comportarse funcionalmente la solución.

Debe responder:

- ¿Qué debe hacer?
- ¿Cuándo debe ejecutarse?
- ¿Quién puede utilizarla?
- ¿Qué condiciones deben cumplirse?
- ¿Qué información debe recibir?
- ¿Qué información debe generar?
- ¿Qué sucede cuando las condiciones se cumplen?
- ¿Qué sucede cuando no se cumplen?

Debe describir comportamiento funcional, no código.

Cuando exista más de un escenario:

- separar claramente cada comportamiento;
- identificar condiciones;
- identificar resultado esperado.

Utilizar:

### Comportamiento funcional

<!-- Describir el comportamiento esperado de la solución. -->

### Entrada

<!-- Describir los datos o condiciones de entrada. -->

### Procesamiento funcional

<!-- Describir las reglas funcionales que deben aplicarse. -->

### Salida

<!-- Describir el resultado funcional esperado. -->

No inventar detalles técnicos no confirmados.

==================================================
13. FLUJO FUNCIONAL
==================================================

## 7. Flujo funcional

Debe representar la secuencia funcional del proceso.

Utilizar una estructura clara:

1. Paso 1:
2. Paso 2:
3. Paso 3:
4. Paso 4:

Cuando sea útil, utilizar:

```text
Inicio
  ↓
Condición
  ↓
Proceso
  ↓
Resultado

Debe permitir comprender el comportamiento sin necesidad de revisar código.

Cuando exista una decisión:

Si condición A
→ comportamiento A

Si condición B
→ comportamiento B

Utilizar:

<!-- Describir el flujo funcional paso a paso. -->
==================================================
14. REGLAS DE NEGOCIO
8. Reglas de negocio

Debe documentar las reglas que determinan el comportamiento funcional.

Cada regla debe tener un identificador.

Utilizar:

RN-01

Regla:

Condición:

Comportamiento esperado:

Fuente:

RN-02

Regla:

Condición:

Comportamiento esperado:

Fuente:

Las reglas deben ser:

claras;
verificables;
trazables;
reutilizables.

No convertir una observación aislada en una regla general sin evidencia.

Si una regla no está confirmada:

Indicar:

"Pendiente de validación."

==================================================
15. VALIDACIONES
9. Validaciones

Debe definir las validaciones funcionales necesarias.

Cada validación debe identificar:

condición;
dato evaluado;
comportamiento esperado;
mensaje o resultado cuando corresponda.

Utilizar:

VAL-01

Condición:

Dato / elemento validado:

Resultado esperado:

Mensaje / comportamiento ante incumplimiento:

VAL-02

Condición:

Dato / elemento validado:

Resultado esperado:

Mensaje / comportamiento ante incumplimiento:

Las validaciones deben ser funcionales.

No inventar mensajes técnicos si no fueron definidos.

==================================================
16. ESCENARIOS
10. Escenarios

Debe documentar los escenarios relevantes de comportamiento.

Separar como mínimo, cuando corresponda:

Escenario principal

Descripción:

Resultado esperado:

Escenarios alternativos
Escenario alternativo 01

Condición:

Comportamiento:

Resultado:

Escenarios de excepción
Escenario de excepción 01

Condición:

Comportamiento esperado:

Resultado:

Escenarios negativos
Escenario negativo 01

Condición:

Comportamiento esperado:

Resultado:

No es obligatorio crear todos los tipos si no aplican.

Cuando no corresponda:

"No aplica."

==================================================
17. DATOS INVOLUCRADOS
11. Datos involucrados

Debe identificar los datos funcionalmente relevantes.

Puede incluir:

campo;
descripción;
origen;
uso;
obligatoriedad;
condición;
resultado.

Utilizar:

Dato / Campo	Descripción	Origen	Uso funcional	Obligatorio
				

No inventar nombres técnicos.

Si un campo técnico no fue confirmado:

"Campo técnico no confirmado."

La tabla puede incluir campos SAP cuando hayan sido identificados mediante evidencia.

==================================================
18. OBJETOS SAP RELACIONADOS
12. Objetos SAP relacionados

Debe identificar los objetos SAP relevantes para comprender la solución.

Utilizar:

Tipo	Objeto	Descripción / Uso	Confirmado
Transacción			
Programa			
Tabla			
Clase			
Función			
Fiori			
Desarrollo Z			
Movimiento			
Documento			

No es obligatorio completar todos los tipos.

No inventar objetos.

Conservar exactamente los nombres técnicos confirmados.

Si un objeto fue mencionado pero no confirmado:

"Objeto no confirmado."

Debe diferenciarse cuando sea posible entre:

estándar SAP;
configuración;
desarrollo Z;
integración;
objeto inferido.
==================================================
19. INTEGRACIONES
13. Integraciones

Debe documentar integraciones relevantes para la funcionalidad.

Puede incluir:

sistema origen;
sistema destino;
interfaz;
middleware;
API;
formato;
frecuencia;
datos intercambiados;
comportamiento ante error.

Utilizar:

Origen	Destino	Integración / Interfaz	Datos	Comportamiento
				

No inventar APIs, endpoints o mecanismos técnicos.

Si no están confirmados:

"No confirmado."

Nunca incluir credenciales o secretos.

==================================================
20. IMPACTOS
14. Impactos

Debe documentar los impactos funcionales conocidos.

Considerar:

procesos;
usuarios;
áreas;
datos;
documentos;
reportes;
integraciones;
controles;
procesos posteriores;
funcionalidades existentes.

Utilizar:

Procesos afectados
Usuarios / áreas afectadas
Datos / documentos afectados
Integraciones afectadas
Procesos posteriores
Otros impactos

Diferenciar impactos confirmados de impactos potenciales.

==================================================
21. DEPENDENCIAS
15. Dependencias

Debe identificar elementos que deben existir o completarse para que la solución funcione.

Puede incluir:

configuraciones;
desarrollos;
interfaces;
datos maestros;
roles;
autorizaciones;
otros proyectos;
procesos previos;
documentos;
servicios externos.

Utilizar:

DEP-01

Dependencia:

Descripción:

Impacto si no está disponible:

No inventar dependencias.

==================================================
22. RIESGOS
16. Riesgos

Debe identificar riesgos funcionales relevantes.

Utilizar:

R-01

Riesgo:

Impacto:

Mitigación:

R-02

Riesgo:

Impacto:

Mitigación:

No utilizar esta sección para especular sin fundamento.

Cuando un riesgo sea potencial:

"Riesgo potencial pendiente de validación."

==================================================
23. CRITERIOS DE ACEPTACIÓN
17. Criterios de aceptación

Debe definir condiciones objetivas que permitan determinar si la solución cumple la especificación.

Cada criterio debe tener un identificador.

Utilizar:

CA-01

Descripción:

Resultado esperado:

CA-02

Descripción:

Resultado esperado:

Los criterios deben ser consistentes con:

solución funcional;
reglas de negocio;
validaciones;
escenarios.

Deben poder convertirse posteriormente en casos de prueba.

No utilizar criterios subjetivos.

==================================================
24. CONSIDERACIONES PARA PRUEBAS
18. Consideraciones para pruebas

Debe identificar qué debe validarse funcionalmente.

Considerar:

escenario principal;
escenarios alternativos;
escenarios negativos;
validaciones;
reglas;
regresión;
datos necesarios;
precondiciones;
resultados esperados.

Utilizar:

Datos requeridos
Precondiciones
Pruebas principales
Pruebas negativas
Pruebas de regresión

No documentar resultados de pruebas que todavía no fueron ejecutadas.

Los resultados reales pertenecen al documento functional-test.

==================================================
25. DOCUMENTACIÓN RELACIONADA
19. Documentación relacionada

Debe conectar la especificación con conocimiento existente.

Utilizar:

Requerimiento relacionado
Tickets relacionados
Análisis relacionados
Debug relacionados
Investigaciones relacionadas
Pruebas funcionales relacionadas
Procesos relacionados
Objetos SAP relacionados

No inventar referencias.

==================================================
26. TRAZABILIDAD

La especificación debe mantener trazabilidad con el requerimiento que la originó cuando exista.

La relación conceptual debe ser:

REQUIREMENT
↓
FUNCTIONAL-SPECIFICATION
↓
IMPLEMENTATION
↓
FUNCTIONAL-TEST
↓
VALIDATION

Cuando exista un cambio importante en la especificación debe evaluarse si afecta:

requerimiento;
implementación;
pruebas;
reglas;
documentación relacionada.
==================================================
27. HECHOS, HIPÓTESIS E INFORMACIÓN FALTANTE

La especificación debe respetar la clasificación definida en:

standards/documentation-standard.md

Debe distinguir:

HECHO
→ confirmado.

HIPÓTESIS
→ pendiente de confirmación.

INFORMACIÓN FALTANTE
→ necesaria pero no disponible.

CONCLUSIÓN
→ derivada de evidencia.

No convertir una hipótesis técnica en una regla funcional.

==================================================
28. REGLA CONTRA LA INVENCIÓN

Si un dato no está confirmado:

NO INVENTAR.

Utilizar:

No confirmado.
Pendiente de definición.
Información faltante.
Requiere validación.
No aplica.

Nunca inventar:

tablas;
campos;
programas;
clases;
funciones;
transacciones;
configuraciones;
APIs;
integraciones;
reglas;
mensajes;
objetos SAP;
datos.
==================================================
29. SEPARACIÓN FUNCIONAL / TÉCNICA

La especificación funcional puede describir lógica funcional detallada.

Sin embargo, NO debe inventar:

nombres de variables;
estructuras ABAP;
métodos;
includes;
arquitectura de clases;
consultas SQL;
BAdIs;
exits;
funciones;
algoritmos técnicos;

salvo que hayan sido confirmados o formen parte explícita de una decisión técnica existente.

Cuando un detalle técnico sea necesario pero no esté definido:

"Implementación técnica: pendiente de definición."

==================================================
30. SEGURIDAD

El template debe cumplir:

standards/security-standard.md

No incluir:

contraseñas;
tokens;
API keys;
credenciales;
claves privadas;
datos personales innecesarios;
datos productivos innecesarios;
información confidencial innecesaria.

Los identificadores SAP pueden conservarse cuando sean necesarios para la trazabilidad funcional.

==================================================
31. VERSIONADO

El template debe cumplir:

standards/versioning-standard.md

La versión inicial será:

version: "1.0"

Un cambio funcional significativo puede requerir una nueva versión.

Las pruebas deben poder identificar qué versión de la especificación validan.

==================================================
32. USO POR EL AGENTE DE IA

Cuando el agente utilice este template deberá:

Buscar el requerimiento relacionado.
Identificar la versión vigente del requerimiento.
Extraer la necesidad funcional.
Definir el comportamiento funcional esperado.
Identificar reglas de negocio.
Identificar validaciones.
Identificar escenarios.
Identificar datos.
Buscar objetos SAP confirmados.
Identificar integraciones.
Evaluar impactos.
Identificar dependencias.
Identificar riesgos.
Definir criterios de aceptación.
Identificar consideraciones para pruebas.
Relacionar documentación existente.
Separar hechos de hipótesis.
Identificar información faltante.
Aplicar las reglas de seguridad.
No inventar información técnica.

El agente debe reutilizar conocimiento existente cuando sea relevante.

==================================================
33. CONSISTENCIA INTERNA

La especificación debe mantener consistencia entre:

SOLUCIÓN FUNCIONAL
↓
FLUJO
↓
REGLAS
↓
VALIDACIONES
↓
ESCENARIOS
↓
CRITERIOS DE ACEPTACIÓN
↓
PRUEBAS

No debe existir una regla que contradiga el flujo.

No debe existir un criterio de aceptación que no pueda relacionarse con el comportamiento definido.

No debe existir una prueba esperada que contradiga la especificación vigente.

==================================================
34. CRITERIO DE CALIDAD

Una especificación funcional completada mediante este template debe permitir que un desarrollador comprenda qué debe implementar sin tener que interpretar la necesidad desde cero.

Debe permitir que QA determine qué debe probar.

Debe permitir que el consultor funcional valide que la solución corresponde al requerimiento.

Debe permitir que un futuro agente de IA comprenda:

problema;
objetivo;
comportamiento;
reglas;
validaciones;
escenarios;
datos;
objetos;
integraciones;
impactos;
dependencias;
criterios de aceptación.
==================================================
35. FORMATO FINAL

El archivo debe comenzar exactamente con:

ticket_id: ""
document_type: "functional-specification"
version: "1.0"
status: "draft"
date: ""
author: ""

Después debe contener exactamente:

Especificación Funcional
Metadata
1. Antecedente
2. Motivo
3. Objetivo
4. Alcance
5. Situación actual
6. Solución funcional propuesta
7. Flujo funcional
8. Reglas de negocio
9. Validaciones
10. Escenarios
11. Datos involucrados
12. Objetos SAP relacionados
13. Integraciones
14. Impactos
15. Dependencias
16. Riesgos
17. Criterios de aceptación
18. Consideraciones para pruebas
19. Documentación relacionada

Cada sección debe contener instrucciones breves mediante comentarios HTML y estructuras vacías listas para completar.

NO incluir:

tickets ficticios;
usuarios ficticios;
sociedades ficticias;
centros ficticios;
objetos SAP ficticios;
reglas ficticias;
datos ficticios;
ejemplos completos de procesos.

El resultado debe ser un TEMPLATE, no una especificación de ejemplo.

==================================================
36. REGLA FINAL DE GENERACIÓN

Genera ÚNICAMENTE:

templates/functional-specification.md

No generar otros templates.

No generar otros estándares.

No modificar otros archivos.

No generar documentación de ejemplo.

No incluir explicaciones fuera del archivo.

El resultado debe estar listo para incorporarse directamente al repositorio agenteSAP.


### La arquitectura que estamos construyendo queda muy bien separada

Con estos dos templates ya tenemos una distinción importante:

```text
REQUIREMENT
    │
    │ ¿Qué necesita el negocio?
    ↓
FUNCTIONAL SPECIFICATION
    │
    │ ¿Qué debe hacer la solución?
    ↓
FUNCTIONAL TEST
    │
    │ ¿La solución cumple?
    ↓
VALIDATION
