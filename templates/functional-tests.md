Actúa como consultor funcional SAP senior, especialista en QA funcional, arquitecto de conocimiento y diseñador de documentación de pruebas para sistemas empresariales y agentes de IA.

Tu tarea es generar ÚNICAMENTE el archivo:

templates/functional-tests.md

Este archivo será el TEMPLATE OFICIAL para documentos de tipo:

document_type: functional-test

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

La responsabilidad de este archivo es únicamente definir la estructura práctica para documentar pruebas funcionales SAP.

Diferencia de responsabilidades:

documentation-standard.md
→ Define las reglas generales de documentación.

versioning-standard.md
→ Define cómo evolucionan y se versionan los documentos.

security-standard.md
→ Define cómo se protege y sanitiza la información.

templates/functional-tests.md
→ Define la estructura que debe utilizar un documento de pruebas funcionales.

==================================================
2. OBJETIVO
==================================================

El template debe permitir documentar de manera estructurada la validación funcional de una solución SAP.

Debe permitir demostrar:

- qué funcionalidad fue validada;
- qué versión fue validada;
- en qué ambiente;
- bajo qué condiciones;
- con qué datos;
- qué casos fueron ejecutados;
- qué se esperaba;
- qué ocurrió realmente;
- qué evidencia existe;
- qué casos fueron exitosos;
- qué casos fallaron;
- qué incidencias fueron encontradas;
- qué resultado general tuvo la validación.

La prueba funcional debe permitir reconstruir el escenario sin depender de la conversación original.

==================================================
3. PRINCIPIO FUNDAMENTAL
==================================================

Una prueba funcional debe distinguir claramente entre:

RESULTADO ESPERADO

y

RESULTADO OBTENIDO.

El resultado esperado debe derivarse de:

- requerimiento;
- especificación funcional;
- regla de negocio;
- criterio de aceptación.

El resultado obtenido debe representar exactamente lo observado durante la ejecución.

Nunca modificar el resultado esperado para hacerlo coincidir con el resultado obtenido.

Ejemplo conceptual:

Resultado esperado:
"El sistema debe bloquear la contabilización."

Resultado obtenido:
"El sistema permitió continuar."

Estado:
"FAIL"

No convertir el resultado esperado en:

"El sistema permite continuar."

para hacer pasar la prueba.

==================================================
4. RELACIÓN CON OTROS DOCUMENTOS
==================================================

La prueba funcional debe mantener trazabilidad con:

REQUIREMENT
↓
FUNCTIONAL-SPECIFICATION
↓
FUNCTIONAL-TEST
↓
VALIDATION

Cuando exista documentación relacionada, debe identificarse.

La prueba debe indicar qué versión funcional está validando.

==================================================
5. METADATA
==================================================

El documento generado mediante este template debe comenzar exactamente con:

---
ticket_id: ""
document_type: "functional-test"
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

La metadata debe mantenerse consistente durante toda la vida del documento.

==================================================
6. ESTRUCTURA OBLIGATORIA
==================================================

Después del Front Matter, utilizar exactamente:

# Pruebas Funcionales

## Metadata

## 1. Objetivo

## 2. Versión funcional validada

## 3. Ambiente

## 4. Precondiciones

## 5. Datos de prueba

## 6. Casos de prueba

## 7. Pruebas negativas

## 8. Pruebas de regresión

## 9. Resultado general

## 10. Incidencias encontradas

## 11. Documentación relacionada

No agregar secciones adicionales salvo que el estándar de documentación sea posteriormente modificado.

==================================================
7. METADATA VISIBLE
==================================================

La sección:

## Metadata

debe representar de forma legible el Front Matter.

Utilizar:

| Campo | Valor |
|---|---|
| Ticket ID | |
| Tipo de documento | functional-test |
| Versión | 1.0 |
| Estado | draft |
| Fecha | |
| Autor | |

La metadata visible y el Front Matter deben permanecer consistentes.

==================================================
8. OBJETIVO
==================================================

## 1. Objetivo

Debe describir qué se pretende validar.

Debe responder:

- ¿Qué funcionalidad se está probando?
- ¿Qué comportamiento se quiere comprobar?
- ¿Qué requerimiento o especificación se está validando?

Utilizar:

<!-- Describir el objetivo de la validación funcional y la funcionalidad que se pretende comprobar. -->

==================================================
9. VERSIÓN FUNCIONAL VALIDADA
==================================================

## 2. Versión funcional validada

Debe identificar qué versión de la especificación funcional está siendo validada.

Utilizar:

| Documento | Versión |
|---|---|
| Requerimiento | |
| Especificación funcional | |

Cuando corresponda, agregar:

| Elemento | Versión / Identificador |
|---|---|
| Desarrollo / cambio | |
| Versión funcional | |

No inventar versiones.

Esta sección es crítica para evitar que una prueba realizada sobre una versión anterior sea interpretada como validación de una versión posterior.

Utilizar:

<!-- Indicar la versión exacta de la funcionalidad que se está validando. -->

==================================================
10. AMBIENTE
==================================================

## 3. Ambiente

Debe identificar el ambiente donde se ejecutó la prueba.

Puede incluir:

- sistema;
- ambiente;
- mandante;
- sociedad;
- centro;
- usuario de prueba;
- fecha;
- transacción;
- aplicación.

Utilizar:

| Elemento | Valor |
|---|---|
| Sistema | |
| Ambiente | |
| Mandante | |
| Sociedad | |
| Centro | |
| Usuario de prueba | |
| Fecha de ejecución | |
| Transacción / Aplicación | |

No almacenar credenciales.

Si un dato no es necesario, no incluirlo.

Si un valor no fue confirmado:

"No confirmado."

==================================================
11. PRECONDICIONES
==================================================

## 4. Precondiciones

Debe identificar las condiciones que deben cumplirse antes de ejecutar las pruebas.

Pueden incluir:

- datos maestros;
- documentos existentes;
- configuraciones;
- autorizaciones;
- stock;
- estados;
- parámetros;
- documentos previos;
- condiciones del proceso;
- interfaces disponibles.

Utilizar:

### PRE-01

Descripción:

### PRE-02

Descripción:

### PRE-03

Descripción:

No inventar precondiciones.

Cuando una precondición sea una hipótesis:

"Pendiente de validar."

==================================================
12. DATOS DE PRUEBA
==================================================

## 5. Datos de prueba

Debe documentar los datos necesarios para reproducir la prueba.

Utilizar:

| Dato | Descripción | Valor | Observación |
|---|---|---|---|
| | | | |

Los datos deben ser suficientes para reproducir el escenario.

No incluir información sensible innecesaria.

Cuando se utilicen datos productivos reales, aplicar:

standards/security-standard.md

Cuando sea posible, utilizar datos de prueba o valores sanitizados.

==================================================
13. CASOS DE PRUEBA
==================================================

## 6. Casos de prueba

Cada caso debe tener un identificador único.

Utilizar:

### Caso de prueba TC-01

#### Objetivo

<!-- Indicar qué comportamiento se valida. -->

#### Precondiciones

- 

#### Datos

- 

#### Pasos

1. 
2. 
3. 
4. 

#### Resultado esperado

<!-- Describir exactamente qué debe ocurrir según la especificación funcional. -->

#### Resultado obtenido

<!-- Registrar exactamente qué ocurrió durante la ejecución. No modificar el resultado esperado para hacerlo coincidir. -->

#### Estado

- PASS
- FAIL
- BLOCKED
- NOT_EXECUTED

#### Evidencia

- 

#### Observaciones

- 

==================================================
14. ESTADOS DE CASOS DE PRUEBA
==================================================

Los estados permitidos para cada caso son:

### PASS

El resultado obtenido cumple el resultado esperado.

### FAIL

El resultado obtenido no cumple el resultado esperado.

### BLOCKED

La prueba no pudo ejecutarse debido a una condición externa o precondición no disponible.

### NOT_EXECUTED

La prueba todavía no fue ejecutada.

No utilizar estados ambiguos como:

- OK;
- Correcto;
- Funciona;
- Listo;
- Revisar.

==================================================
15. PASOS DE PRUEBA
==================================================

Los pasos deben ser:

- secuenciales;
- reproducibles;
- claros;
- suficientemente específicos.

Formato:

1. Ejecutar...
2. Seleccionar...
3. Ingresar...
4. Confirmar...
5. Verificar...

No incluir información sensible.

Los pasos deben permitir que otro consultor pueda repetir la prueba.

==================================================
16. RESULTADO ESPERADO
==================================================

El resultado esperado debe derivarse de:

- especificación funcional;
- regla de negocio;
- criterio de aceptación;
- comportamiento funcional definido.

Debe ser:

- objetivo;
- observable;
- verificable.

Evitar:

"Debe funcionar correctamente."

Preferir:

"El documento debe generarse con estado X y el campo Y debe permanecer vacío."

No inventar resultados esperados.

==================================================
17. RESULTADO OBTENIDO
==================================================

El resultado obtenido debe documentar lo que realmente ocurrió.

Debe utilizar lenguaje factual.

Ejemplo conceptual:

"El documento fue generado, pero el campo Y quedó informado."

No interpretar inmediatamente la causa.

Si la causa fue analizada posteriormente, referenciar el análisis correspondiente.

==================================================
18. EVIDENCIA
==================================================

La sección de evidencia debe permitir demostrar el resultado obtenido.

Puede incluir:

- screenshot;
- documento SAP;
- número de documento;
- log;
- mensaje;
- registro;
- resultado de consulta;
- evidencia funcional;
- referencia a archivo.

Utilizar:

### Evidencia TC-01

- Tipo:
- Referencia:
- Descripción:

No almacenar información sensible innecesaria.

==================================================
19. PRUEBAS NEGATIVAS
==================================================

## 7. Pruebas negativas

Debe validar qué ocurre cuando las condiciones esperadas NO se cumplen.

Ejemplos conceptuales:

- dato obligatorio vacío;
- condición inválida;
- usuario sin autorización;
- documento en estado incorrecto;
- cantidad inválida;
- combinación no permitida;
- registro inexistente.

Utilizar:

### Caso negativo TC-N01

#### Condición

#### Pasos

1.
2.
3.

#### Resultado esperado

#### Resultado obtenido

#### Estado

#### Evidencia

No inventar escenarios negativos que no estén relacionados con la especificación.

==================================================
20. PRUEBAS DE REGRESIÓN
==================================================

## 8. Pruebas de regresión

Debe identificar funcionalidades existentes que podrían verse afectadas por el cambio.

Utilizar:

| Caso | Funcionalidad | Resultado esperado | Resultado obtenido | Estado |
|---|---|---|---|---|
| REG-01 | | | | |
| REG-02 | | | | |

La regresión debe considerar especialmente:

- procesos relacionados;
- funcionalidades existentes;
- escenarios anteriores;
- integraciones;
- reglas compartidas;
- objetos SAP reutilizados.

No declarar una prueba como regresión simplemente porque fue ejecutada después de un cambio.

Debe existir una relación funcional con una conducta previamente existente.

==================================================
21. RESULTADO GENERAL
==================================================

## 9. Resultado general

Debe presentar el resultado consolidado de la validación.

Utilizar:

| Métrica | Resultado |
|---|---|
| Casos ejecutados | |
| PASS | |
| FAIL | |
| BLOCKED | |
| NOT_EXECUTED | |
| Casos negativos ejecutados | |
| Casos de regresión ejecutados | |

Luego:

### Resultado de la validación

Utilizar uno de:

- PASS
- FAIL
- PARTIAL
- BLOCKED

No utilizar "PASS" si existen fallos que impiden considerar validada la funcionalidad, salvo que exista una decisión funcional explícita documentada.

Si el resultado general depende de una decisión pendiente:

"Pendiente de definición."

==================================================
22. INCIDENCIAS ENCONTRADAS
==================================================

## 10. Incidencias encontradas

Debe documentar cualquier desviación encontrada durante las pruebas.

Utilizar:

### Incidencia INC-01

**Caso de prueba relacionado:**

**Descripción:**

**Resultado esperado:**

**Resultado obtenido:**

**Impacto:**

**Estado:**

**Ticket relacionado:**

**Evidencia:**

No asumir la causa raíz.

Si la causa fue determinada mediante análisis o debug, referenciar el documento correspondiente.

==================================================
23. DOCUMENTACIÓN RELACIONADA
==================================================

## 11. Documentación relacionada

Debe permitir relacionar las pruebas con:

### Requerimiento

-

### Especificación funcional

-

### Tickets relacionados

-

### Análisis relacionados

-

### Debug relacionados

-

### Investigaciones relacionadas

-

### Incidencias relacionadas

-

No inventar referencias.

==================================================
24. TRAZABILIDAD DE PRUEBAS
==================================================

Cada caso de prueba debe poder relacionarse con uno o más elementos funcionales.

La trazabilidad conceptual debe ser:

REQUERIMIENTO
↓
CRITERIO DE ACEPTACIÓN
↓
REGLA / VALIDACIÓN / ESCENARIO
↓
CASO DE PRUEBA
↓
RESULTADO
↓
EVIDENCIA

Cuando sea posible, indicar el criterio de aceptación validado:

### Caso de prueba TC-01

Criterio de aceptación relacionado:
CA-01

Regla relacionada:
RN-01

Esto permite determinar qué parte de la funcionalidad fue realmente validada.

==================================================
25. COBERTURA FUNCIONAL
==================================================

Cuando exista información suficiente, el documento debe permitir identificar cobertura de:

- criterios de aceptación;
- reglas de negocio;
- validaciones;
- escenarios principales;
- escenarios alternativos;
- escenarios negativos;
- regresión.

Utilizar opcionalmente:

| Elemento funcional | Casos de prueba | Cobertura |
|---|---|---|
| CA-01 | TC-01 | Validado |
| RN-01 | TC-02 | Validado |
| VAL-01 | TC-03 | Pendiente |

No indicar "Validado" si no existe evidencia de ejecución satisfactoria.

==================================================
26. REGLA DE NO ALTERACIÓN DE RESULTADOS
==================================================

Una vez ejecutada una prueba:

El resultado obtenido debe conservarse tal como fue observado.

No modificarlo para:

- hacer coincidir la prueba;
- ocultar una falla;
- justificar una decisión;
- conseguir un PASS;
- evitar registrar una incidencia.

Si el resultado obtenido contradice la especificación:

registrar:

Estado: FAIL

y documentar la desviación.

==================================================
27. REGLA DE REEJECUCIÓN
==================================================

Si una prueba FAIL es corregida y posteriormente ejecutada nuevamente, no borrar el resultado anterior.

Registrar una nueva ejecución o evidencia.

Ejemplo:

### Ejecución 1

Resultado:
FAIL

### Corrección

Referencia:

### Ejecución 2

Resultado:
PASS

Esto preserva la trazabilidad.

==================================================
28. PRUEBAS BLOCKED
==================================================

Cuando una prueba no pueda ejecutarse por una dependencia externa:

Estado:

BLOCKED

Debe documentarse:

- qué impidió la ejecución;
- qué dependencia falta;
- qué debe ocurrir para desbloquearla.

No marcar como PASS.

==================================================
29. PRUEBAS NO EJECUTADAS
==================================================

Si una prueba está definida pero todavía no fue ejecutada:

Estado:

NOT_EXECUTED

No registrar un resultado obtenido ficticio.

Utilizar:

"Pendiente de ejecución."

==================================================
30. HECHOS, HIPÓTESIS E INFORMACIÓN FALTANTE
==================================================

El documento debe distinguir:

HECHO
→ resultado observado.

HIPÓTESIS
→ posible explicación aún no confirmada.

INFORMACIÓN FALTANTE
→ información necesaria para determinar un resultado o causa.

CONCLUSIÓN
→ resultado derivado de evidencia.

Una prueba funcional debe registrar principalmente hechos observables.

La explicación de una causa raíz pertenece al análisis o debug correspondiente.

==================================================
31. REGLA CONTRA LA INVENCIÓN
==================================================

No inventar:

- resultados;
- evidencias;
- documentos SAP;
- números de documento;
- datos de prueba;
- mensajes;
- estados;
- causas;
- tickets;
- objetos;
- resultados de ejecución.

Si una prueba no fue ejecutada:

NOT_EXECUTED

Si no se pudo ejecutar:

BLOCKED

Si no existe evidencia:

"Sin evidencia registrada."

==================================================
32. SEGURIDAD
==================================================

El template debe cumplir:

standards/security-standard.md

No incluir:

- contraseñas;
- tokens;
- API keys;
- credenciales;
- claves privadas;
- datos personales innecesarios;
- datos productivos innecesarios;
- información confidencial innecesaria.

Las evidencias deben ser revisadas antes de incorporarse.

Los números de documentos SAP pueden utilizarse cuando sean necesarios para reproducir el escenario, pero deben sanitizarse cuando no sean necesarios.

==================================================
33. VERSIONADO
==================================================

El template debe cumplir:

standards/versioning-standard.md

La versión inicial será:

version: "1.0"

La documentación de pruebas debe indicar explícitamente qué versión funcional fue validada.

Una modificación significativa de la funcionalidad puede requerir:

- actualización de casos;
- nuevos casos;
- regresión;
- nueva versión del documento de pruebas.

==================================================
34. USO POR EL AGENTE DE IA
==================================================

Cuando el agente utilice este template deberá:

1. Buscar la especificación funcional vigente.
2. Identificar la versión funcional que debe validarse.
3. Identificar criterios de aceptación.
4. Identificar reglas de negocio.
5. Identificar validaciones.
6. Identificar escenarios.
7. Diseñar casos de prueba funcionales.
8. Incluir escenarios negativos cuando correspondan.
9. Identificar necesidades de regresión.
10. Registrar únicamente resultados realmente ejecutados.
11. Separar resultado esperado de resultado obtenido.
12. Registrar evidencia disponible.
13. Identificar incidencias.
14. Mantener trazabilidad.
15. Aplicar las reglas de seguridad.
16. No inventar resultados.

El agente puede PROPONER casos de prueba antes de su ejecución.

Pero no puede marcar un caso como PASS sin evidencia de ejecución.

==================================================
35. CRITERIO DE CALIDAD
==================================================

Un documento de pruebas funcionales completo debe permitir responder:

- ¿Qué se está validando?
- ¿Qué versión se validó?
- ¿Dónde se validó?
- ¿Con qué datos?
- ¿Qué precondiciones existían?
- ¿Qué casos se ejecutaron?
- ¿Qué se esperaba?
- ¿Qué ocurrió?
- ¿Cuál fue el resultado?
- ¿Existe evidencia?
- ¿Qué falló?
- ¿Qué incidencias se encontraron?
- ¿Qué funcionalidades quedaron sin validar?
- ¿Qué regresión se ejecutó?
- ¿Cuál es el resultado general?

==================================================
36. CONSISTENCIA CON LA ESPECIFICACIÓN
==================================================

Las pruebas deben ser consistentes con:

- objetivo;
- alcance;
- reglas;
- validaciones;
- escenarios;
- criterios de aceptación;

de la especificación funcional vigente.

Si una prueba requiere comportamiento que no está definido en la especificación:

No asumir que el comportamiento debe existir.

Registrar:

"Comportamiento no definido en la especificación funcional. Requiere validación."

==================================================
37. FORMATO FINAL
==================================================

El archivo generado debe comenzar exactamente con:

---
ticket_id: ""
document_type: "functional-test"
version: "1.0"
status: "draft"
date: ""
author: ""
---

Después debe contener exactamente:

# Pruebas Funcionales

## Metadata

## 1. Objetivo

## 2. Versión funcional validada

## 3. Ambiente

## 4. Precondiciones

## 5. Datos de prueba

## 6. Casos de prueba

## 7. Pruebas negativas

## 8. Pruebas de regresión

## 9. Resultado general

## 10. Incidencias encontradas

## 11. Documentación relacionada

Cada sección debe contener instrucciones breves mediante comentarios HTML y estructuras vacías listas para completar.

No incluir:

- tickets ficticios;
- documentos ficticios;
- resultados ficticios;
- evidencias ficticias;
- usuarios ficticios;
- sociedades ficticias;
- centros ficticios;
- objetos SAP ficticios;
- datos ficticios.

El resultado debe ser un TEMPLATE, no un documento de pruebas de ejemplo.

==================================================
38. REGLA FINAL DE GENERACIÓN
==================================================

Genera ÚNICAMENTE:

templates/functional-tests.md

No generar otros templates.

No generar otros estándares.

No modificar otros archivos.

No generar documentación de ejemplo.

No incluir explicaciones fuera del archivo.

El resultado debe estar listo para incorporarse directamente al repositorio `agenteSAP`.
