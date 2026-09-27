Actúa como arquitecto de conocimiento, consultor funcional SAP senior y especialista en documentación técnica y funcional.

Tu tarea es generar el archivo:

standards/documentation-standard.md

Este archivo será el ESTÁNDAR MAESTRO DE DOCUMENTACIÓN del repositorio `agenteSAP`.

IMPORTANTE:
No debes crear templates separados en esta tarea.
No debes crear otros estándares.
No debes modificar otros archivos.
Debes generar únicamente el contenido completo de:

standards/documentation-standard.md

El documento debe ser claro, normativo, reutilizable por humanos y agentes de IA, y suficientemente preciso para que cualquier documentación futura del repositorio siga una estructura homogénea.

==================================================
1. CONTEXTO DEL PROYECTO
==================================================

El repositorio `agenteSAP` tiene como objetivo construir una base de conocimiento para un futuro agente de IA especializado en consultoría funcional SAP.

El agente deberá poder:

- comprender documentación funcional;
- analizar requerimientos;
- comprender especificaciones funcionales;
- analizar incidentes;
- analizar investigaciones;
- interpretar sesiones de debug;
- relacionar tickets con objetos SAP;
- relacionar procesos con reglas de negocio;
- identificar dependencias;
- recuperar conocimiento histórico;
- reutilizar análisis anteriores;
- mantener trazabilidad;
- distinguir hechos de hipótesis;
- identificar información faltante;
- evitar inventar comportamiento SAP;
- generar nueva documentación basada en evidencia existente.

La documentación debe estar diseñada tanto para:

1. consumo humano;
2. consumo por modelos de IA;
3. búsqueda semántica;
4. recuperación por `ticket_id`;
5. construcción futura de relaciones entre conocimiento.

La documentación debe priorizar:

- claridad;
- trazabilidad;
- evidencia;
- consistencia;
- versionado;
- reutilización;
- seguridad;
- precisión funcional.

==================================================
2. OBJETIVO DEL ESTÁNDAR
==================================================

Definir una estructura única y obligatoria para toda la documentación funcional y de consultoría del repositorio.

Este estándar debe establecer:

- tipos de documentos;
- metadata obligatoria;
- estructura mínima;
- estados;
- clasificación de información;
- reglas de documentación;
- trazabilidad;
- relación entre documentos;
- relación con objetos SAP;
- relación con procesos;
- relación con reglas de negocio;
- tratamiento de evidencia;
- tratamiento de hipótesis;
- manejo de información faltante;
- versionado documental;
- seguridad;
- criterios de calidad.

El estándar debe funcionar como un contrato documental.

Cualquier documento nuevo deberá cumplir este estándar.

==================================================
3. PRINCIPIO FUNDAMENTAL
==================================================

La documentación debe transformar información dispersa en conocimiento reutilizable.

La cadena conceptual es:

DOCUMENTACIÓN
      ↓
TRAZABILIDAD
      ↓
CONTEXTO
      ↓
EVIDENCIA
      ↓
CONOCIMIENTO
      ↓
RELACIONES
      ↓
REUTILIZACIÓN

Un documento no debe limitarse a describir lo ocurrido.

Debe permitir comprender:

- qué ocurrió;
- por qué ocurrió;
- qué se sabe;
- qué no se sabe;
- qué evidencia existe;
- qué se concluyó;
- qué objetos están involucrados;
- qué proceso está afectado;
- qué reglas aplican;
- qué documentación está relacionada.

==================================================
4. TICKET_ID COMO ÍNDICE TRANSVERSAL
==================================================

`ticket_id` será el principal identificador transversal para relacionar documentación asociada a una misma necesidad, incidente, mejora, análisis o investigación.

Ejemplo:

ticket_id: "33007"

Un mismo ticket puede tener:

- requerimiento;
- especificación funcional;
- pruebas funcionales;
- análisis;
- debug;
- investigación;
- documentación histórica;
- documentación relacionada.

El `ticket_id` NO debe interpretarse como la única entidad del conocimiento.

Un objeto SAP puede aparecer en múltiples tickets.

Un proceso SAP puede aparecer en múltiples tickets.

Una regla de negocio puede aparecer en múltiples tickets.

Una relación entre documentos debe poder mantenerse incluso cuando los documentos pertenezcan a tickets diferentes.

Cuando un documento no esté asociado a ningún ticket:

ticket_id: "N/A"

Nunca inventar un `ticket_id`.

==================================================
5. TIPOS OFICIALES DE DOCUMENTACIÓN
==================================================

El estándar debe reconocer únicamente los siguientes tipos oficiales.

DOCUMENTACIÓN OFICIAL:

1. `requirement`
2. `functional-specification`
3. `functional-test`

ACTIVIDADES DE CONSULTORÍA:

4. `analysis`
5. `debug`
6. `investigation`

Estos tipos representan diferentes niveles de conocimiento y no deben mezclarse indiscriminadamente.

--------------------------------------------------
5.1 REQUIREMENT
--------------------------------------------------

Representa la necesidad funcional o problema de negocio que origina una solicitud.

Debe responder:

- ¿qué necesidad existe?
- ¿qué problema se quiere resolver?
- ¿cuál es el objetivo?
- ¿qué alcance tiene?
- ¿cómo se determinará que la necesidad fue satisfecha?

No debe convertirse prematuramente en una solución técnica.

--------------------------------------------------
5.2 FUNCTIONAL-SPECIFICATION
--------------------------------------------------

Representa la definición funcional de la solución requerida.

Debe explicar:

- qué debe hacer la solución;
- bajo qué condiciones;
- qué reglas debe cumplir;
- qué validaciones deben existir;
- qué escenarios deben contemplarse;
- qué datos intervienen;
- qué objetos SAP están involucrados;
- qué integraciones existen;
- qué impactos y dependencias deben considerarse.

La especificación funcional debe separar claramente:

NECESIDAD FUNCIONAL

de

SOLUCIÓN TÉCNICA.

No debe inventar detalles técnicos que no hayan sido confirmados.

--------------------------------------------------
5.3 FUNCTIONAL-TEST
--------------------------------------------------

Representa la validación funcional de una solución.

Debe documentar:

- ambiente;
- versión validada;
- datos;
- precondiciones;
- pasos;
- resultados esperados;
- resultados obtenidos;
- evidencias;
- estado;
- incidencias encontradas.

--------------------------------------------------
5.4 ANALYSIS
--------------------------------------------------

Representa una actividad de análisis funcional.

Puede utilizarse para:

- analizar un incidente;
- comprender un proceso;
- evaluar una inconsistencia;
- investigar datos;
- estudiar impactos;
- analizar una solución existente;
- preparar una especificación.

Debe separar hechos, hipótesis, información faltante y conclusiones.

--------------------------------------------------
5.5 DEBUG
--------------------------------------------------

Representa una actividad de análisis técnico/funcional realizada mediante debug.

Debe registrar:

- ambiente;
- escenario;
- programa;
- clase;
- método;
- función;
- include;
- transacción;
- parámetros;
- datos observados;
- flujo;
- puntos relevantes;
- comportamiento observado;
- hipótesis;
- conclusión técnica.

No debe presentar una hipótesis como causa confirmada.

--------------------------------------------------
5.6 INVESTIGATION
--------------------------------------------------

Representa una investigación documental, funcional o técnica.

Puede incluir:

- documentación SAP;
- comportamiento estándar;
- análisis de desarrollos Z;
- configuraciones;
- tablas;
- procesos;
- integraciones;
- antecedentes históricos;
- documentación interna.

Debe identificar claramente las fuentes consultadas.

==================================================
6. METADATA OBLIGATORIA
==================================================

TODO documento debe comenzar con un bloque de metadata.

La metadata es obligatoria.

Formato:

```yaml
ticket_id:
document_type:
version:
status:
date:
author:

Ejemplo:

ticket_id: "33007"
document_type: "functional-specification"
version: "1.0"
status: "draft"
date: "2026-09-03"
author: "Analista Funcional"
6.1 ticket_id

Identificador del ticket asociado.

Si no existe:

ticket_id: "N/A"

Nunca inventar valores.

6.2 document_type

Debe utilizar exclusivamente uno de los valores permitidos:

requirement
functional-specification
functional-test
analysis
debug
investigation
6.3 version

Indica la versión del documento.

Ejemplo:

version: "1.0"

El versionado documental deberá permitir identificar cambios posteriores.

No sobrescribir silenciosamente una versión anterior cuando el cambio sea relevante.

6.4 status

Valores permitidos:

draft
in_review
approved
implemented
validated
obsolete

Utilizar el estado que represente realmente la situación del documento.

6.5 date

Fecha de creación o actualización de la versión documentada.

Formato recomendado:

YYYY-MM-DD

Ejemplo:

date: "2026-09-03"
6.6 author

Persona o rol responsable de la elaboración de la versión.

Ejemplo:

author: "Analista Funcional"

No inventar nombres.

6.7 METADATA OPCIONAL

Podrán existir posteriormente campos adicionales como:

document_id:
parent_document:

Estos campos son opcionales en la primera versión del estándar.

No deben convertirse en obligatorios salvo que otro estándar posterior los defina como tales.

==================================================
7. ESTADOS DOCUMENTALES

Los estados permitidos son:

draft

Documento en elaboración.

in_review

Documento pendiente de revisión.

approved

Documento aprobado funcionalmente.

implemented

La solución documentada fue implementada.

validated

La solución fue validada mediante pruebas funcionales.

obsolete

Documento que ya no representa el comportamiento vigente, pero debe conservarse por trazabilidad histórica.

No eliminar documentación histórica únicamente porque haya quedado obsoleta.

==================================================
8. CLASIFICACIÓN DE INFORMACIÓN

Toda documentación de análisis debe distinguir como mínimo:

HECHO

Información confirmada mediante evidencia.

Ejemplo:

"El programa ZMM_IM_0004 genera el documento K4."

Solo afirmar esto si existe evidencia suficiente.

HIPÓTESIS

Explicación posible aún no confirmada.

Ejemplo:

"Se plantea como hipótesis que la posición marcada para borrado provoca el comportamiento observado."

INFORMACIÓN FALTANTE

Información necesaria para confirmar una conclusión pero que todavía no está disponible.

Ejemplo:

"No se dispone del resultado del debug en ambiente PRD."

CONCLUSIÓN

Resultado del análisis basado en hechos y evidencia.

Las conclusiones deben indicar claramente si están confirmadas o si dependen de hipótesis.

Nunca presentar una hipótesis como hecho.

==================================================
9. ESTRUCTURA DE REQUIREMENT

Un documento requirement debe utilizar, como mínimo:

Requerimiento
Metadata
1. Antecedente
2. Situación actual
3. Necesidad / Problema
4. Objetivo
5. Alcance
6. Fuera de alcance
7. Impacto funcional
8. Criterios de aceptación
9. Información adicional
10. Documentación relacionada

No completar secciones con información inventada.

Cuando una sección no aplique, indicar:

"No aplica."

==================================================
10. ESTRUCTURA DE FUNCTIONAL-SPECIFICATION

Un documento functional-specification debe utilizar, como mínimo:

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

La especificación debe ser suficientemente precisa para que un equipo técnico pueda comprender qué comportamiento debe implementarse.

No debe definir detalles técnicos no confirmados.

==================================================
11. ESTRUCTURA DE FUNCTIONAL-TEST

Un documento functional-test debe utilizar:

Pruebas Funcionales
Metadata
1. Objetivo
2. Versión funcional validada
3. Ambiente
4. Precondiciones
5. Datos de prueba
6. Casos de prueba
Caso de prueba XX
Objetivo
Precondiciones
Datos
Pasos
Resultado esperado
Resultado obtenido
Estado
Evidencia
7. Pruebas negativas
8. Pruebas de regresión
9. Resultado general
10. Incidencias encontradas
11. Documentación relacionada

Los resultados esperados y obtenidos deben mantenerse separados.

Nunca modificar retrospectivamente el resultado esperado para hacerlo coincidir con el comportamiento observado.

==================================================
12. ESTRUCTURA DE ANALYSIS

Un documento analysis debe utilizar:

Análisis
Metadata
1. Objetivo del análisis
2. Contexto
3. Información disponible
4. Hechos identificados
5. Evidencias
6. Análisis funcional
7. Hipótesis
8. Información faltante
9. Impactos identificados
10. Dependencias
11. Conclusión
12. Próximos pasos
13. Documentación relacionada

El análisis debe priorizar razonamiento basado en evidencia.

==================================================
13. ESTRUCTURA DE DEBUG

Un documento debug debe utilizar:

Debug
Metadata
1. Objetivo
2. Ambiente
3. Escenario reproducido
4. Objeto analizado

Programa:
Clase:
Método:
Función:
Include:
Transacción:

5. Parámetros relevantes
6. Datos observados
7. Flujo analizado
8. Puntos relevantes del debug
9. Evidencia
10. Comportamiento observado
11. Hipótesis
12. Conclusión técnica
13. Información faltante
14. Documentación relacionada

Debe distinguir:

COMPORTAMIENTO OBSERVADO

de

CAUSA CONFIRMADA.

El hecho de encontrar un comportamiento en debug no significa automáticamente que se haya confirmado la causa raíz.

==================================================
14. ESTRUCTURA DE INVESTIGATION

Un documento investigation debe utilizar:

Investigación
Metadata
1. Objetivo
2. Pregunta de investigación
3. Fuentes consultadas
4. Información encontrada
5. Análisis
6. Relaciones identificadas
7. Conclusiones
8. Información pendiente de validar
9. Documentación relacionada

Toda afirmación derivada de una fuente debe poder rastrearse hasta dicha fuente.

==================================================
15. OBJETOS SAP

Los documentos pueden registrar objetos SAP como:

transacciones;
programas;
clases;
métodos;
funciones;
tablas;
estructuras;
CDS;
BAdIs;
exits;
SmartForms;
Adobe Forms;
aplicaciones Fiori;
roles;
catálogos;
movimientos de mercancía;
tipos de documento;
clases de documento;
configuraciones;
desarrollos Z;
integraciones.

Los nombres técnicos deben conservarse exactamente como fueron confirmados.

Ejemplo:

ZMM_IM_0004

No modificar arbitrariamente nombres técnicos.

Nunca inventar un objeto SAP.

Si un objeto fue mencionado pero no confirmado:

Objeto: no confirmado
==================================================
16. PROCESOS SAP

La documentación debe identificar, cuando sea posible:

proceso;
subproceso;
módulo;
transacción;
objeto principal;
documentos SAP involucrados;
integraciones;
entradas;
salidas;
reglas relevantes.

Debe distinguirse entre:

comportamiento estándar SAP;
configuración SAP;
desarrollo personalizado;
integración externa;
comportamiento inferido.

Nunca afirmar que algo es estándar SAP sin evidencia suficiente.

==================================================
17. REGLAS DE NEGOCIO

Las reglas de negocio deben documentarse explícitamente cuando sean relevantes.

Una regla debe ser:

clara;
verificable;
trazable;
reutilizable.

Formato recomendado:

Regla:
Condición:
Comportamiento esperado:
Fuente:

Una observación aislada no debe convertirse automáticamente en una regla general.

Ejemplo:

Observar que un material fue tratado de determinada manera en un caso concreto no significa que esa conducta sea una regla global del proceso.

==================================================
18. RELACIONES ENTRE CONOCIMIENTO

El estándar debe permitir identificar relaciones entre:

tickets;
documentos;
objetos SAP;
procesos;
reglas de negocio;
análisis;
causas;
soluciones;
pruebas.

Relaciones iniciales permitidas:

related_ticket
related_object
related_process
related_rule
implemented_by
tested_by
derived_from
caused_by
resolved_by

Estas relaciones podrán evolucionar posteriormente.

No deben inventarse relaciones.

Una relación debe estar respaldada por evidencia o documentación.

==================================================
19. TRAZABILIDAD

Toda conclusión importante debe poder rastrearse hasta:

requerimiento;
evidencia;
documento;
debug;
investigación;
prueba;
fuente;
objeto SAP;
dato observado.

Cuando una conclusión sea una inferencia, debe indicarse explícitamente.

Ejemplo:

Conclusión:
[CONCLUSIÓN INFERIDA]

Base:
- Evidencia 1
- Evidencia 2

Validación pendiente:
- Debug en PRD

La trazabilidad debe permitir responder:

"¿Por qué creemos que esto es cierto?"

==================================================
20. DOCUMENTACIÓN RELACIONADA

Los documentos deben incluir una sección:

Documentación relacionada

Debe utilizarse para conectar conocimiento existente.

Ejemplo:

- Ticket: 33007
- Requerimiento: ...
- Especificación funcional: ...
- Análisis: ...
- Debug: ...
- Pruebas funcionales: ...

No inventar referencias.

Cuando una relación exista pero el documento todavía no esté disponible, indicarlo claramente.

==================================================
21. CONOCIMIENTO REUTILIZABLE

Cuando un análisis revele conocimiento que pueda reutilizarse en otros casos, debe identificarse.

Ejemplos:

una regla de negocio;
una relación entre tablas;
una relación entre documentos;
un comportamiento conocido de una transacción;
una dependencia;
un objeto SAP;
una integración;
una validación;
una causa recurrente;
un patrón de error.

El objetivo es evitar que el conocimiento quede encerrado dentro de un único ticket.

Un análisis de un incidente puede convertirse posteriormente en conocimiento transversal.

==================================================
22. CONSISTENCIA DOCUMENTAL

La documentación debe mantener consistencia entre:

requerimiento;
especificación;
implementación;
pruebas;
análisis;
debug;
investigación.

Debe poder identificarse si:

el requerimiento cambió;
la solución cambió;
las pruebas corresponden a la versión correcta;
existe una diferencia entre comportamiento esperado y observado;
una documentación quedó obsoleta.

Nunca asumir que dos documentos son equivalentes solamente porque tienen el mismo ticket_id.

==================================================
23. REGLAS PARA GENERACIÓN AUTOMÁTICA

Cuando el agente genere documentación deberá:

Identificar el ticket_id.
Identificar el document_type.
Identificar la versión.
Identificar el estado.
Identificar fecha y autor cuando estén disponibles.
Utilizar la estructura correspondiente al tipo de documento.
Utilizar únicamente información disponible.
Separar hechos de hipótesis.
Identificar información faltante.
No inventar objetos SAP.
No inventar reglas de negocio.
No inventar comportamiento estándar SAP.
Mantener nombres técnicos confirmados.
Registrar evidencias.
Mantener trazabilidad.
Relacionar documentación existente cuando corresponda.
Indicar incertidumbre cuando exista.
Preservar información histórica relevante.
Aplicar las reglas de seguridad.
Mantener consistencia con documentación existente.

Si la información disponible no es suficiente, el agente debe indicarlo.

No debe completar los vacíos mediante suposiciones.

==================================================
24. ACTUALIZACIÓN DE DOCUMENTOS

Cuando se solicite modificar un documento existente, el agente debe:

Recuperar la versión vigente.
Identificar qué cambió.
Identificar por qué cambió.
Determinar si el cambio es:
documental;
funcional;
técnico;
histórico.
Evaluar impacto.
Actualizar la versión según el estándar de versionado.
Mantener trazabilidad del cambio.
Evitar eliminar información histórica relevante.
Verificar consistencia con documentos relacionados.

Nunca modificar silenciosamente una versión aprobada.

==================================================
25. DOCUMENTACIÓN HISTÓRICA

La documentación histórica debe conservarse cuando tenga valor para:

auditoría;
trazabilidad;
comprensión de incidentes;
análisis de cambios;
evolución del sistema;
comportamiento anterior;
decisiones funcionales.

Un documento histórico puede estar en estado:

obsolete

Esto significa que ya no representa necesariamente el comportamiento actual.

No significa que deba eliminarse.

Cuando exista diferencia entre comportamiento histórico y actual, debe indicarse explícitamente.

==================================================
26. PRINCIPIO DE REUTILIZACIÓN

Antes de crear nuevo conocimiento, el agente debe buscar conocimiento existente.

Debe buscar por:

ticket_id;
objetos SAP;
procesos;
reglas;
transacciones;
tablas;
programas;
funciones;
clases;
términos funcionales;
síntomas;
causas;
integraciones.

El objetivo es evitar análisis duplicados.

Si existe un análisis previo relevante, debe reutilizarse y referenciarse.

No duplicar conocimiento innecesariamente.

==================================================
27. PRINCIPIO DE EVIDENCIA

La evidencia tiene prioridad sobre la interpretación.

Orden recomendado:

EVIDENCIA
↓
HECHO
↓
ANÁLISIS
↓
HIPÓTESIS
↓
CONCLUSIÓN

Nunca invertir este orden para justificar una conclusión previamente asumida.

Cuando exista conflicto entre información documental y evidencia observada:

documentar el conflicto;
no ocultarlo;
indicar qué fuente respalda cada posición;
determinar qué información falta para resolverlo.
==================================================
28. SEGURIDAD Y SANITIZACIÓN

La documentación no debe almacenar:

contraseñas;
tokens;
API keys;
credenciales;
certificados privados;
claves privadas;
secretos;
información sensible innecesaria.

Debe sanitizarse información como:

nombres personales cuando no sean necesarios;
correos;
teléfonos;
documentos personales;
datos bancarios;
información sensible de proveedores;
datos productivos innecesarios;
información confidencial.

Sin embargo, no deben eliminarse automáticamente identificadores técnicos SAP relevantes.

Ejemplos que pueden ser necesarios:

sociedades;
centros;
almacenes;
movimientos;
transacciones;
tablas;
programas;
clases;
funciones;
documentos SAP;
desarrollos Z.

La sanitización no debe destruir el contexto funcional necesario para comprender el problema.

==================================================
29. CALIDAD DOCUMENTAL

Antes de considerar un documento terminado, verificar:

Identificación
¿Tiene ticket_id?
¿Tiene document_type?
¿Tiene version?
¿Tiene status?
¿Tiene date?
¿Tiene author?
Contenido
¿Utiliza la estructura correcta?
¿El objetivo está claro?
¿El alcance está definido?
¿Las conclusiones son comprensibles?
Evidencia
¿Los hechos están respaldados?
¿Las hipótesis están identificadas?
¿La información faltante está indicada?
¿Las conclusiones se derivan de la evidencia?
SAP
¿Los objetos SAP fueron confirmados?
¿Se evitaron objetos inventados?
¿Se distingue estándar de customización/desarrollo?
¿Se documentaron las relaciones relevantes?
Trazabilidad
¿Se puede rastrear el origen de la información?
¿Se relacionaron documentos existentes?
¿Se identificaron dependencias?
Seguridad
¿Se eliminaron secretos?
¿Se evitó información sensible innecesaria?
¿Se conservó el contexto técnico necesario?
==================================================
30. REGLA CONTRA LA INVENCIÓN

Esta es una regla crítica del estándar.

El agente NO debe inventar:

transacciones;
tablas;
campos;
programas;
clases;
funciones;
reglas;
procesos;
configuraciones;
comportamiento SAP;
relaciones;
datos;
causas;
resultados;
documentación inexistente.

Cuando algo no esté confirmado, utilizar expresiones como:

"No confirmado."
"Información faltante."
"Hipótesis."
"Requiere validación."
"No se dispone de evidencia suficiente."

La precisión tiene prioridad sobre la completitud aparente.

==================================================
31. PRINCIPIO DE CONSULTORÍA FUNCIONAL

La documentación debe ayudar al consultor a pensar, no solamente a registrar información.

Debe facilitar la separación entre:

PROBLEMA
↓
CONTEXTO
↓
HECHOS
↓
EVIDENCIA
↓
ANÁLISIS
↓
HIPÓTESIS
↓
VALIDACIÓN
↓
CONCLUSIÓN
↓
SOLUCIÓN
↓
PRUEBA
↓
CONOCIMIENTO REUTILIZABLE

El agente debe evitar saltar directamente desde:

"el usuario reporta un error"

a

"la solución es X"

sin documentar el razonamiento intermedio.

==================================================
32. PRINCIPIO DE SEPARACIÓN FUNCIONAL / TÉCNICA

La documentación funcional debe explicar:

qué necesita el negocio;
qué comportamiento debe existir;
qué reglas aplican;
qué escenarios deben cumplirse.

La documentación técnica puede explicar posteriormente:

cómo se implementará;
qué programa se modificará;
qué clase se utilizará;
qué tablas serán afectadas;
qué lógica ABAP se implementará.

No mezclar innecesariamente ambas perspectivas.

Una especificación funcional puede mencionar objetos técnicos cuando sean relevantes, pero no debe inventar la implementación.

==================================================
33. PRINCIPIO DE HISTORIAL Y VERSIONADO

La documentación debe permitir comprender la evolución de una solución.

Debe ser posible responder:

¿qué se solicitó originalmente?
¿qué se especificó?
¿qué cambió?
¿por qué cambió?
¿qué versión se implementó?
¿qué versión fue probada?
¿qué comportamiento fue validado?
¿qué documentación quedó obsoleta?

La versión documental debe mantenerse alineada con el estado real de la solución.

==================================================
34. REGLA PARA INFORMACIÓN INCOMPLETA

Si faltan datos necesarios para completar un documento:

NO inventarlos.

Utilizar:

Información faltante:
- ...

o:

Pendiente de validación:
- ...

El documento puede quedar incompleto si la evidencia disponible es insuficiente.

Es preferible una documentación explícitamente incompleta que una documentación completa basada en información inventada.

==================================================
35. PRINCIPIO DE MÍNIMA DOCUMENTACIÓN SUFICIENTE

La documentación debe ser completa respecto de su propósito, pero no debe generar contenido innecesario.

Debe evitar:

repetir información sin valor;
documentación burocrática;
explicaciones redundantes;
campos sin utilidad;
detalles técnicos irrelevantes;
información no relacionada.

El objetivo es producir documentación:

CLARA
+
PRECISA
+
TRAZABLE
+
REUTILIZABLE.

==================================================
36. REGLA DE DOCUMENTACIÓN RELACIONADA

Cuando un documento dependa de otro, debe indicarse.

Ejemplo:

derived_from:
- REQ-33007

implemented_by:
- FS-33007

tested_by:
- FT-33007

Sin embargo, estas relaciones no deben inventarse.

Si no existe evidencia suficiente para establecer una relación, no debe declararse.

==================================================
37. PRINCIPIO DE EVOLUCIÓN DEL ESTÁNDAR

Este documento constituye la versión inicial del estándar de documentación.

El estándar podrá evolucionar cuando se identifiquen nuevas necesidades del agente.

Las futuras extensiones pueden incluir:

identificadores documentales;
taxonomías;
ontología SAP;
relaciones más detalladas;
metadata adicional;
automatización;
validación automática;
reglas de calidad;
integración con GitHub;
indexación semántica;
generación automática de knowledge graph.

Las extensiones futuras no deben romper innecesariamente la estructura existente.

==================================================
38. RESULTADO ESPERADO

El estándar debe permitir que un futuro agente SAP pueda recibir una consulta como:

"¿Qué sabemos sobre el incidente 33007?"

y encontrar:

requerimiento;
especificación;
análisis;
debug;
pruebas;
objetos SAP relacionados;
procesos afectados;
reglas de negocio;
evidencias;
conclusiones;
documentación histórica.

También debe permitir consultas como:

"¿En qué tickets aparece ZMM_IMX_0004?"

"¿Qué incidentes afectan al proceso de SNC?"

"¿Qué análisis anteriores existen sobre documentos K1?"

"¿Qué reglas de negocio están relacionadas con determinado proceso?"

"¿Qué pruebas validaron esta solución?"

"¿Cuál fue la causa identificada en incidentes similares?"

La estructura documental debe hacer posible este tipo de recuperación de conocimiento.

==================================================
39. CRITERIO FINAL

La documentación del repositorio agenteSAP no debe ser considerada únicamente como archivos Markdown.

Debe considerarse una BASE DE CONOCIMIENTO ESTRUCTURADA.

Cada documento debe aportar:

contexto;
evidencia;
conocimiento;
trazabilidad;
relaciones;
reutilización.

El objetivo final es que el conocimiento generado durante la operación SAP no se pierda dentro de tickets, correos, chats o conversaciones aisladas.

Debe transformarse en conocimiento estructurado que pueda ser recuperado, relacionado y reutilizado por futuros consultores y por el agente de IA.

==================================================
40. INSTRUCCIÓN FINAL PARA LA GENERACIÓN

Genera únicamente el archivo:

standards/documentation-standard.md

El archivo debe:

estar completamente escrito en Markdown;
ser autocontenido;
utilizar lenguaje profesional;
ser normativo;
ser claro para consultores funcionales SAP;
ser interpretable por agentes de IA;
no contener explicaciones externas al estándar;
no incluir comentarios sobre esta instrucción;
no inventar información;
no crear otros archivos.

El resultado debe ser directamente utilizable como el estándar maestro de documentación del repositorio agenteSAP.
