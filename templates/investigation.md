Quiero que crees el archivo:

templates/investigation.md

Este archivo será la plantilla oficial para documentar INVESTIGACIONES dentro del repositorio agenteSAP.

IMPORTANTE:
Antes de generar el contenido, considera como fuente normativa los siguientes archivos existentes del repositorio:

- standards/documentation-standard.md
- standards/versioning-standard.md
- standards/security-standard.md

La plantilla debe ser compatible con esos estándares y con las plantillas existentes:

- templates/requirement.md
- templates/functional-specification.md
- templates/functional-tests.md
- templates/analysis.md
- templates/debug.md

==================================================
OBJETIVO DE investigation.md
==================================================

La plantilla debe servir para documentar investigaciones realizadas para obtener, validar, contrastar o consolidar conocimiento.

Una INVESTIGACIÓN debe responder principalmente:

- ¿Qué se está investigando?
- ¿Por qué es necesario investigarlo?
- ¿Qué fuentes fueron consultadas?
- ¿Qué información se encontró?
- ¿Qué información está confirmada?
- ¿Qué información es configuración, desarrollo propio, estándar SAP o inferencia?
- ¿Qué relaciones se identificaron?
- ¿Qué conclusiones pueden extraerse?
- ¿Qué información todavía necesita validación?

La investigación debe preservar la trazabilidad entre:

PREGUNTA
→ FUENTES
→ INFORMACIÓN ENCONTRADA
→ ANÁLISIS
→ RELACIONES
→ CONCLUSIONES
→ VALIDACIONES PENDIENTES

No debe convertirse en una especificación funcional, un análisis de incidente ni un documento técnico de implementación.

==================================================
DIFERENCIA CON ANALYSIS Y DEBUG
==================================================

La plantilla debe dejar clara esta separación:

INVESTIGATION:
Busca y consolida conocimiento a partir de fuentes.

ANALYSIS:
Analiza un caso, problema o situación utilizando información y evidencias disponibles.

DEBUG:
Investiga el comportamiento técnico de un desarrollo mediante ejecución, código, variables, estructuras, funciones, clases, métodos, etc.

FUNCTIONAL SPECIFICATION:
Define cómo debe comportarse funcionalmente una solución.

Por lo tanto, una investigación puede ser utilizada posteriormente como fuente para un análisis, una especificación funcional o una prueba.

==================================================
METADATA
==================================================

El archivo debe comenzar obligatoriamente con YAML front matter:

---
ticket_id: ""
document_type: "investigation"
version: "1.0"
status: "draft"
date: ""
author: ""
---

Luego debe contener:

# Investigación

Y una sección:

## Metadata

Debe incluir una tabla con:

| Campo | Valor |
|---|---|
| Ticket ID | |
| Tipo de documento | investigation |
| Versión | |
| Estado | |
| Fecha | |
| Autor | |

Si la investigación no está asociada a un ticket, utilizar:

ticket_id: "N/A"

No inventar valores.

==================================================
ESTRUCTURA OBLIGATORIA
==================================================

La plantilla debe utilizar exactamente esta estructura:

## 1. Objetivo

## 2. Pregunta de investigación

## 3. Fuentes consultadas

## 4. Información encontrada

## 5. Análisis

## 6. Relaciones identificadas

## 7. Conclusiones

## 8. Información pendiente de validar

## 9. Documentación relacionada


==================================================
1. OBJETIVO
==================================================

Explicar claramente qué se pretende conseguir con la investigación.

Debe indicar:

- qué conocimiento se busca obtener;
- cuál es el contexto que motiva la investigación;
- para qué será utilizada la información obtenida.

No incluir soluciones inventadas.

Ejemplos de objetivos válidos conceptualmente:

- comprender el funcionamiento estándar de un proceso SAP;
- identificar qué configuración interviene en determinado comportamiento;
- determinar qué objetos SAP están relacionados con un proceso;
- validar si un comportamiento corresponde al estándar SAP o a una personalización;
- consolidar conocimiento disperso sobre un proceso.

No incluir ejemplos ficticios en la plantilla final.

Agregar un comentario HTML breve explicando qué debe documentarse en esta sección.


==================================================
2. PREGUNTA DE INVESTIGACIÓN
==================================================

Definir claramente la pregunta que debe responder la investigación.

La pregunta debe ser concreta y verificable.

Cuando existan varias preguntas, identificarlas como:

PREG-01
PREG-02
PREG-03

Cada pregunta debe poder relacionarse posteriormente con información encontrada y conclusiones.

Evitar preguntas excesivamente amplias cuando puedan dividirse en preguntas más específicas.


==================================================
3. FUENTES CONSULTADAS
==================================================

Esta sección debe registrar todas las fuentes utilizadas para obtener información.

Debe permitir identificar:

- fuente;
- tipo de fuente;
- referencia;
- fecha de consulta cuando sea relevante;
- alcance de la información obtenida;
- nivel de confiabilidad cuando corresponda.

Utilizar una tabla con una estructura similar a:

| ID | Fuente | Tipo | Referencia | Fecha | Observación |
|---|---|---|---|---|---|

Los IDs deben utilizar:

SRC-01
SRC-02
SRC-03

Tipos de fuente pueden incluir, cuando corresponda:

- SAP Help
- SAP Notes
- documentación oficial SAP
- documentación interna
- configuración SAP
- desarrollo Z
- código ABAP
- tablas SAP
- logs
- evidencias funcionales
- tickets
- pruebas
- documentación de proyecto
- conocimiento proporcionado por usuarios o equipos técnicos

No inventar referencias.

Cuando una fuente no pueda ser identificada completamente, indicarlo explícitamente.

Distinguir siempre entre:

- fuente oficial;
- fuente interna;
- evidencia técnica;
- información proporcionada por terceros;
- interpretación propia.

La plantilla debe promover el uso prioritario de fuentes oficiales y evidencias verificables cuando estén disponibles.


==================================================
4. INFORMACIÓN ENCONTRADA
==================================================

Documentar la información obtenida de las fuentes.

Cada hallazgo relevante debe tener un identificador:

HALL-01
HALL-02
HALL-03

Para cada hallazgo debe poder indicarse:

- descripción;
- fuente de origen;
- estado de validación;
- observaciones.

Utilizar una estructura similar a:

| ID | Información encontrada | Fuente | Estado |
|---|---|---|---|

Los estados deben permitir diferenciar como mínimo:

- CONFIRMADO
- NO CONFIRMADO
- PARCIAL
- EN VALIDACIÓN

No presentar como hecho una información que solamente sea una hipótesis o interpretación.

Cuando sea relevante, distinguir entre:

- comportamiento estándar SAP;
- configuración;
- desarrollo personalizado;
- integración;
- comportamiento observado;
- información documental;
- inferencia.

No asumir que un comportamiento observado en un sistema corresponde al estándar SAP.


==================================================
5. ANÁLISIS
==================================================

Interpretar la información encontrada sin convertirla en una conclusión no sustentada.

El análisis debe explicar:

- qué significan los hallazgos;
- cómo se relacionan;
- qué diferencias existen entre las fuentes;
- qué información está respaldada por evidencia;
- qué información es interpretación;
- qué aspectos permanecen inciertos.

Cuando exista información contradictoria:

1. identificar la contradicción;
2. indicar qué fuentes la presentan;
3. explicar qué debe validarse;
4. no seleccionar arbitrariamente una versión como verdadera.

Utilizar identificadores de hallazgos para mantener trazabilidad.

Por ejemplo conceptualmente:

HALL-01 + HALL-03 → interpretación correspondiente.

No inventar relaciones que no estén sustentadas.


==================================================
6. RELACIONES IDENTIFICADAS
==================================================

Documentar las relaciones relevantes descubiertas durante la investigación.

Las relaciones pueden involucrar:

- procesos;
- módulos SAP;
- transacciones;
- programas;
- clases;
- métodos;
- funciones;
- tablas;
- estructuras;
- campos;
- movimientos;
- documentos;
- configuraciones;
- integraciones;
- desarrollos Z;
- reglas de negocio;
- otros documentos.

Cuando se conozca una relación, documentarla explícitamente.

Utilizar una tabla como:

| ID | Elemento origen | Relación | Elemento destino | Evidencia |
|---|---|---|---|---|

Ejemplos de tipos de relación conceptuales:

- utiliza;
- depende de;
- genera;
- actualiza;
- determina;
- valida;
- integra;
- precede;
- sucede después de;
- está relacionado con.

No inventar objetos SAP ni relaciones técnicas.

Si un objeto fue mencionado pero no fue confirmado:

"Objeto: no confirmado"

Si una relación es inferida y no está directamente evidenciada:

"Relación inferida — requiere validación"


==================================================
7. CONCLUSIONES
==================================================

Documentar las conclusiones obtenidas a partir de la investigación.

Cada conclusión debe tener un identificador:

CON-01
CON-02
CON-03

Cada conclusión debe indicar, cuando sea posible:

- conclusión;
- hallazgos que la sustentan;
- fuente principal;
- nivel de certeza.

Utilizar estados como:

- CONFIRMADA
- SUSTENTADA
- INFERIDA
- PENDIENTE

Una conclusión debe poder rastrearse hacia los hallazgos y fuentes que la sustentan.

No generar conclusiones simplemente para completar la sección.

Si la investigación no permite responder la pregunta, indicarlo explícitamente.

Ejemplo conceptual:

CON-01
Conclusión: [conclusión]
Sustentada por: HALL-02, HALL-05
Estado: SUSTENTADA


==================================================
8. INFORMACIÓN PENDIENTE DE VALIDAR
==================================================

Registrar todo aquello que todavía requiere validación.

Utilizar identificadores:

VAL-01
VAL-02
VAL-03

Utilizar una tabla como:

| ID | Información pendiente | Motivo | Acción de validación | Responsable |
|---|---|---|---|---|

No inventar responsables ni fechas.

Si no existe información pendiente:

"N/A"


==================================================
9. DOCUMENTACIÓN RELACIONADA
==================================================

Registrar documentos relacionados con la investigación.

Incluir, cuando corresponda:

- requerimientos;
- especificaciones funcionales;
- pruebas;
- análisis;
- debug;
- otras investigaciones;
- tickets;
- documentación SAP;
- documentación de procesos.

Utilizar referencias reales.

No inventar nombres de documentos.

Cuando exista relación con otro documento del repositorio, mantener el ticket_id y/o referencia correspondiente.


==================================================
CLASIFICACIÓN DE INFORMACIÓN
==================================================

La plantilla debe aplicar obligatoriamente la clasificación definida por:

standards/documentation-standard.md

Toda información debe poder distinguirse entre:

- HECHO
- HIPÓTESIS
- INFORMACIÓN FALTANTE
- CONCLUSIÓN

No mezclar hechos con interpretaciones.

Cuando una afirmación no pueda ser respaldada, debe quedar marcada como:

NO CONFIRMADO

o

PENDIENTE DE VALIDAR


==================================================
FUENTES Y CALIDAD DEL CONOCIMIENTO
==================================================

La investigación debe priorizar fuentes de mayor autoridad.

Cuando sea posible, utilizar este orden conceptual:

1. documentación oficial SAP;
2. SAP Notes / documentación oficial aplicable;
3. configuración real del sistema;
4. desarrollos y objetos técnicos reales;
5. evidencias de ejecución;
6. documentación interna;
7. información proporcionada por usuarios;
8. interpretación propia.

Este orden no significa que una fuente de menor nivel sea inválida.

Debe evaluarse el contexto y la naturaleza de cada afirmación.

Distinguir claramente entre:

"Según documentación SAP..."

"Según configuración observada..."

"Según desarrollo Z identificado..."

"Según información proporcionada..."

"Se infiere que..."

No presentar una inferencia como documentación oficial.


==================================================
INVESTIGACIÓN SOBRE SAP
==================================================

Cuando la investigación involucre SAP:

- preservar nombres técnicos confirmados;
- preservar nombres de transacciones;
- preservar programas;
- preservar clases;
- preservar métodos;
- preservar funciones;
- preservar tablas;
- preservar campos;
- preservar movimientos;
- preservar objetos de customizing;
- preservar integraciones.

No modificar nombres técnicos.

No inventar objetos.

No asumir que un objeto existe solamente porque sería habitual en SAP.

Cuando el objeto no haya sido confirmado:

"Objeto: no confirmado"


==================================================
TRAZABILIDAD
==================================================

La plantilla debe permitir construir la siguiente cadena:

Pregunta
→ Fuente
→ Hallazgo
→ Análisis
→ Relación
→ Conclusión
→ Validación pendiente

Utilizar identificadores consistentes:

PREG-xx
SRC-xx
HALL-xx
CON-xx
VAL-xx

Esto permitirá posteriormente que un agente de IA pueda recuperar y relacionar conocimiento de manera estructurada.


==================================================
RELACIÓN CON TICKET_ID
==================================================

ticket_id es el identificador transversal definido por:

standards/documentation-standard.md

Una investigación puede:

- originarse en un ticket;
- apoyar un ticket;
- alimentar varios documentos del mismo ticket;
- existir como investigación independiente.

No asumir que toda investigación debe tener ticket.

Cuando corresponda:

ticket_id: "N/A"


==================================================
SEGURIDAD
==================================================

La plantilla debe cumplir obligatoriamente con:

standards/security-standard.md

No incluir:

- contraseñas;
- tokens;
- API keys;
- credenciales;
- claves privadas;
- secretos;
- información sensible innecesaria.

Si una evidencia contiene información sensible, documentar solamente la información necesaria para comprender la investigación.

Los datos productivos, personales o financieros deben minimizarse.

Los identificadores técnicos SAP pueden conservarse cuando sean necesarios para comprender el proceso.


==================================================
VERSIONADO
==================================================

La plantilla debe ser compatible con:

standards/versioning-standard.md

El documento debe utilizar:

version: "1.0"

Las modificaciones posteriores deben respetar:

PATCH:
Cambios editoriales o de formato.

MINOR:
Información adicional sin modificar el significado fundamental.

MAJOR:
Cambio significativo del contenido o de las conclusiones.

No eliminar silenciosamente conocimiento relevante.

Cuando una investigación sea actualizada, conservar la trazabilidad de los cambios mediante Git.


==================================================
REGLAS PARA EL AGENTE
==================================================

El agente que utilice esta plantilla debe cumplir:

1. No inventar información.
2. No inventar fuentes.
3. No inventar objetos SAP.
4. No inventar resultados.
5. No transformar hipótesis en hechos.
6. No transformar inferencias en conclusiones confirmadas.
7. Mantener trazabilidad entre fuentes y conclusiones.
8. Identificar información faltante.
9. Registrar contradicciones entre fuentes.
10. Diferenciar estándar SAP de configuración y desarrollo personalizado.
11. Mantener los nombres técnicos confirmados.
12. Aplicar las reglas de seguridad.
13. Respetar el versionado.
14. Mantener relación con ticket_id cuando corresponda.
15. Priorizar evidencia sobre interpretación.


==================================================
FORMATO FINAL DEL ARCHIVO
==================================================

El archivo generado debe contener:

1. YAML front matter.
2. Título "# Investigación".
3. Sección "## Metadata".
4. Las nueve secciones obligatorias.
5. Comentarios HTML breves donde ayuden a explicar qué debe documentarse.
6. Tablas únicamente cuando aporten estructura.
7. Identificadores consistentes para preguntas, fuentes, hallazgos, conclusiones y validaciones.
8. Ningún dato ficticio.
9. Ningún ejemplo con información SAP inventada.
10. Ninguna conclusión inventada.

El resultado debe ser una plantilla Markdown limpia, profesional, reutilizable y preparada para ser utilizada tanto por consultores funcionales como por un futuro agente de IA.

No agregues secciones adicionales fuera de las definidas anteriormente.

No expliques el proceso de creación.

Entrega únicamente el contenido final que debe guardarse en:

templates/investigation.md
