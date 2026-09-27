Este archivo será la plantilla maestra para documentar RELACIONES entre elementos de conocimiento dentro del repositorio agenteSAP.

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

Ahora se debe crear:

knowledge/relationships/relationships.md

Esta plantilla representa la capa de relaciones del Knowledge Base.

==================================================
OBJETIVO
==================================================

Una RELACIÓN representa una conexión explícita entre dos elementos de conocimiento.

La relación debe permitir expresar:

ELEMENTO A
    ↓
RELACIÓN
    ↓
ELEMENTO B

Por ejemplo, conceptualmente:

OBJETO
→ participa en →
PROCESO

PROCESO
→ aplica →
REGLA

OBJETO
→ actualiza →
OBJETO

REGLA
→ implementada mediante →
OBJETO

PROCESO
→ integra con →
SISTEMA

TICKET
→ documenta →
OBJETO

La relación debe ser tratada como conocimiento independiente.

No debe depender exclusivamente de que un agente interprete texto libre para descubrirla.

==================================================
PRINCIPIO FUNDAMENTAL
==================================================

Una relación debe responder:

- ¿Qué elemento está relacionado?
- ¿Con qué otro elemento?
- ¿Qué tipo de relación existe?
- ¿En qué dirección?
- ¿Qué significa funcionalmente?
- ¿Cuál es la evidencia?
- ¿Qué nivel de certeza tiene?
- ¿Desde cuándo aplica, si corresponde?
- ¿Existe una condición para que la relación aplique?

No crear relaciones solamente porque dos elementos aparecen en el mismo documento.

CO-OCURRENCIA ≠ RELACIÓN

Que dos objetos aparezcan juntos en un ticket no demuestra necesariamente que exista una relación funcional o técnica entre ellos.

==================================================
MODELO DE RELACIÓN
==================================================

Toda relación debe seguir conceptualmente:

SOURCE
    ↓
RELATION
    ↓
TARGET

Ejemplo conceptual:

OBJ-0001
    ↓
participa_en
    ↓
PROC-0001

Donde:

SOURCE = OBJ-0001
RELATION = participa_en
TARGET = PROC-0001

La dirección de la relación debe conservarse.

No invertir automáticamente source y target.

==================================================
METADATA
==================================================

El archivo debe comenzar obligatoriamente con YAML front matter:

---
relationship_id: ""
source_id: ""
source_type: ""
relation_type: ""
target_id: ""
target_type: ""
version: "1.0"
status: "draft"
date: ""
author: ""
---

Luego:

# Relación

## Metadata

Utilizar una tabla:

| Campo | Valor |
|---|---|
| Relationship ID | |
| Source ID | |
| Source Type | |
| Relation Type | |
| Target ID | |
| Target Type | |
| Versión | |
| Estado | |
| Fecha | |
| Autor | |

No inventar valores.

==================================================
RELATIONSHIP_ID
==================================================

Cada relación debe tener un identificador único y estable.

Utilizar:

REL-0001
REL-0002
REL-0003

El relationship_id identifica la relación como conocimiento.

No utilizar:

- ticket_id;
- object_id;
- process_id;
- rule_id

como sustituto del relationship_id.

Una misma relación puede estar respaldada por múltiples tickets y evidencias.


==================================================
SOURCE_ID
==================================================

Identifica el elemento de origen de la relación.

Debe utilizar un identificador existente en el Knowledge Base.

Ejemplos:

OBJ-0001
PROC-0001
BR-0001

No inventar identificadores.

Si el elemento todavía no está documentado, utilizar:

"IDENTIFICADO_NO_DOCUMENTADO"

y registrar la necesidad de documentación correspondiente.

No crear un ID ficticio.


==================================================
SOURCE_TYPE
==================================================

Registrar el tipo del elemento origen.

Tipos permitidos conceptualmente:

- SAP_OBJECT
- PROCESS
- BUSINESS_RULE
- TICKET
- DOCUMENT
- SYSTEM
- ACTOR
- OTHER

Utilizar el tipo que corresponda al elemento real.


==================================================
TARGET_ID
==================================================

Identifica el elemento destino.

Debe utilizar un identificador existente cuando corresponda.

No inventar identificadores.

==================================================
TARGET_TYPE
==================================================

Registrar el tipo del elemento destino.

Utilizar la clasificación correspondiente:

- SAP_OBJECT
- PROCESS
- BUSINESS_RULE
- TICKET
- DOCUMENT
- SYSTEM
- ACTOR
- OTHER


==================================================
1. ELEMENTO ORIGEN
==================================================

## 1. Elemento origen

Documentar:

- ID;
- nombre;
- tipo;
- referencia.

No duplicar toda la documentación del elemento.

El objetivo es permitir identificar inequívocamente el origen.


==================================================
2. TIPO DE RELACIÓN
==================================================

## 2. Tipo de relación

Registrar la relación mediante un vocabulario controlado.

Utilizar preferentemente verbos o relaciones semánticas claras.

Ejemplos:

- utiliza
- participa_en
- contiene
- forma_parte_de
- depende_de
- genera
- actualiza
- lee
- consulta
- ejecuta
- llama
- determina
- valida
- aplica
- implementa
- implementada_mediante
- integra_con
- precede
- sucede_a
- reemplaza
- deriva_de
- documenta
- evidencia
- relacionado_con
- afecta
- requiere
- bloquea
- autoriza
- alimenta
- consume
- transforma

No crear sinónimos innecesarios para la misma relación.

Ejemplo:

Si se decide utilizar:

"utiliza"

no crear posteriormente:

"usa"

"emplea"

"consume"

para representar exactamente el mismo significado, salvo que exista una diferencia semántica real.


==================================================
3. ELEMENTO DESTINO
==================================================

## 3. Elemento destino

Documentar:

- ID;
- nombre;
- tipo;
- referencia.

No duplicar toda la documentación del elemento.


==================================================
4. DESCRIPCIÓN DE LA RELACIÓN
==================================================

## 4. Descripción de la relación

Explicar qué significa la relación.

La descripción debe ser funcional y suficientemente precisa.

Debe responder:

¿Por qué se afirma que A tiene esta relación con B?

Evitar descripciones vagas como:

"Están relacionados."

Utilizar una explicación basada en evidencia.

No inventar causalidad.

==================================================
5. DIRECCIÓN
==================================================

## 5. Dirección

Documentar explícitamente:

SOURCE → RELATION → TARGET

La relación debe ser direccional cuando el significado lo requiera.

Ejemplo conceptual:

OBJ-0001
→ actualiza →
OBJ-0002

No significa automáticamente:

OBJ-0002
→ actualiza →
OBJ-0001

La relación inversa debe documentarse solamente si tiene significado propio.

==================================================
6. CONDICIÓN DE APLICACIÓN
==================================================

## 6. Condición de aplicación

Documentar cuándo aplica la relación.

No todas las relaciones necesitan una condición.

Cuando corresponda puede depender de:

- módulo;
- sociedad;
- centro;
- almacén;
- tipo de documento;
- tipo de movimiento;
- estado;
- fecha;
- configuración;
- escenario;
- proceso;
- versión.

Si la relación es general:

"Sin condición específica identificada."

Si la condición no está confirmada:

"Condición pendiente de validar."


==================================================
7. MOMENTO DEL PROCESO
==================================================

## 7. Momento del proceso

Cuando la relación tenga contexto temporal dentro de un proceso, documentar cuándo ocurre.

Puede ser:

- inicio;
- durante una etapa;
- antes de una actividad;
- después de una actividad;
- cierre;
- condición excepcional.

Utilizar step_id cuando exista:

STEP-01
STEP-02

No inventar pasos.


==================================================
8. EVIDENCIA
==================================================

## 8. Evidencia

Esta es una sección crítica.

Toda relación relevante debe poder rastrearse hacia una evidencia.

Utilizar:

EVID-REL-01
EVID-REL-02

Las fuentes pueden ser:

- documentación oficial SAP;
- configuración;
- código;
- debug;
- análisis;
- investigación;
- prueba funcional;
- especificación;
- ticket;
- documento de proceso;
- comportamiento observado.

Utilizar:

| ID | Fuente | Tipo | Qué demuestra |
|---|---|---|---|

No inventar evidencias.

Una evidencia debe demostrar específicamente la relación y no solamente la existencia de los dos elementos.


==================================================
9. NIVEL DE CERTEZA
==================================================

## 9. Nivel de certeza

Clasificar la relación.

Utilizar:

- CONFIRMADA
- PARCIAL
- EN_VALIDACION
- INFERIDA
- NO_CONFIRMADA

Reglas:

CONFIRMADA:
Existe evidencia suficiente.

PARCIAL:
La relación existe pero alguno de sus detalles no está completamente confirmado.

EN_VALIDACION:
Existe evidencia inicial pero requiere comprobación.

INFERIDA:
La relación se deduce de información disponible pero no está directamente demostrada.

NO_CONFIRMADA:
No existe evidencia suficiente.

Una relación INFERIDA no debe presentarse como CONFIRMADA.


==================================================
10. ALCANCE
==================================================

## 10. Alcance

Indicar dónde aplica la relación.

Puede incluir:

- módulos;
- procesos;
- sociedades;
- centros;
- almacenes;
- tipos de documento;
- escenarios;
- sistemas;
- versiones.

Si la relación es global:

"General."

No asumir alcance global si solamente fue observada en un caso específico.


==================================================
11. VIGENCIA
==================================================

## 11. Vigencia

Cuando corresponda documentar:

- fecha de inicio;
- fecha de fin;
- versión;
- período;
- condición temporal.

Utilizar:

Desde:
Hasta:

Si no existe una vigencia conocida:

"Vigencia no determinada."


==================================================
12. IMPACTO
==================================================

## 12. Impacto

Describir qué significa funcionalmente la relación.

Puede afectar:

- flujo;
- datos;
- documentos;
- contabilización;
- inventario;
- integración;
- autorización;
- validaciones;
- reglas de negocio.

No exagerar el impacto.

Si el impacto no fue confirmado:

"Impacto pendiente de validar."


==================================================
13. RELACIONES INVERSAS
==================================================

## 13. Relaciones inversas

Cuando sea útil, documentar la relación semánticamente inversa.

Ejemplo:

OBJ-0001
→ genera →
OBJ-0002

puede permitir consultar:

OBJ-0002
← generado_por ←
OBJ-0001

No crear automáticamente una segunda relación si la relación inversa puede derivarse de la primera.

Solo registrar una relación inversa independiente cuando tenga significado propio.

==================================================
14. CONFLICTOS O CONTRADICCIONES
==================================================

## 14. Conflictos o contradicciones

Registrar cuando diferentes fuentes indiquen relaciones diferentes.

Utilizar:

CONFLICT-REL-01

Documentar:

- fuente A;
- fuente B;
- diferencia;
- estado de validación.

No resolver arbitrariamente la contradicción.

Si una fuente tiene mayor autoridad, indicar el motivo de su prioridad sin ocultar la existencia de la contradicción.


==================================================
15. INFORMACIÓN PENDIENTE
==================================================

## 15. Información pendiente

Registrar información que todavía necesita validación.

Utilizar:

PEND-REL-01
PEND-REL-02

Tabla:

| ID | Información pendiente | Motivo | Acción requerida |
|---|---|---|---|

Si no existe:

"N/A"


==================================================
16. DOCUMENTACIÓN RELACIONADA
==================================================

## 16. Documentación relacionada

Relacionar la relación con:

- objetos SAP;
- procesos;
- reglas de negocio;
- requirements;
- functional specifications;
- functional tests;
- analysis;
- debug;
- investigations;
- tickets.

Utilizar referencias reales.

No inventar documentos.


==================================================
VOCABULARIO CONTROLADO DE RELACIONES
==================================================

La base de conocimiento debe utilizar un vocabulario controlado para evitar duplicación semántica.

Categorías sugeridas:

ESTRUCTURA:

- contiene
- forma_parte_de
- subproceso_de

DEPENDENCIA:

- depende_de
- requiere

EJECUCIÓN:

- ejecuta
- llama

DATOS:

- lee
- consulta
- actualiza
- genera
- transforma
- alimenta
- consume

FUNCIONAL:

- participa_en
- utiliza
- aplica
- determina
- valida
- afecta
- bloquea
- autoriza

SECUENCIA:

- precede
- sucede_a

INTEGRACIÓN:

- integra_con

IMPLEMENTACIÓN:

- implementa
- implementada_mediante
- configurada_mediante

DOCUMENTACIÓN:

- documenta
- evidencia

ORIGEN:

- deriva_de
- reemplaza

No crear nuevos tipos de relación si uno existente expresa correctamente el significado.


==================================================
RELACIONES ENTRE TIPOS DE CONOCIMIENTO
==================================================

La plantilla debe soportar relaciones como:

SAP_OBJECT → PROCESS

SAP_OBJECT → SAP_OBJECT

SAP_OBJECT → BUSINESS_RULE

PROCESS → BUSINESS_RULE

PROCESS → PROCESS

BUSINESS_RULE → SAP_OBJECT

BUSINESS_RULE → PROCESS

TICKET → SAP_OBJECT

TICKET → PROCESS

TICKET → BUSINESS_RULE

TICKET → RELATIONSHIP

DOCUMENT → SAP_OBJECT

DOCUMENT → PROCESS

DOCUMENT → BUSINESS_RULE

No limitar artificialmente las combinaciones si existe una relación válida y sustentada.


==================================================
RELACIONES VS COINCIDENCIA
==================================================

Una relación NO debe crearse solamente porque:

- dos objetos aparecen en el mismo ticket;
- dos tablas aparecen en una consulta;
- dos nombres aparecen en un documento;
- dos actividades ocurren cerca temporalmente;
- dos objetos pertenecen al mismo módulo.

Debe existir evidencia suficiente para establecer una relación semántica.

Ejemplo conceptual:

Si un análisis menciona:

TABLA A
TABLA B

no significa automáticamente:

TABLA A
→ relacionada_con →
TABLA B

Debe existir una razón funcional o técnica identificable.


==================================================
RELACIONES TÉCNICAS
==================================================

Cuando la relación sea técnica, documentar exactamente lo que fue confirmado.

Ejemplos:

Programa
→ llama →
Function Module

Programa
→ actualiza →
Tabla

Transacción
→ ejecuta →
Programa

Clase
→ utiliza →
Método

No inferir relaciones solamente por nombres similares.


==================================================
RELACIONES FUNCIONALES
==================================================

Cuando la relación sea funcional:

Proceso
→ aplica →
Regla

Proceso
→ utiliza →
Objeto SAP

Regla
→ determina →
Resultado

La relación debe representar el comportamiento funcional conocido.


==================================================
RELACIONES TEMPORALES
==================================================

Cuando corresponda:

Actividad A
→ precede →
Actividad B

o:

Proceso A
→ sucede_a →
Proceso B

Debe existir evidencia del orden.

No inferir secuencias únicamente por una suposición lógica.


==================================================
RELACIÓN CON TICKETS
==================================================

Un ticket representa un caso concreto.

Una relación representa conocimiento reutilizable.

Por lo tanto:

relationship_id = identidad de la relación

ticket_id = evidencia o contexto donde la relación fue descubierta, validada, cuestionada o utilizada.

Un ticket no crea automáticamente una nueva relación.

Si el ticket confirma una relación existente:

agregar el ticket como evidencia.

Si descubre una nueva relación:

crear una relación nueva.


==================================================
RELACIÓN CON SAP OBJECTS
==================================================

Los objetos deben identificarse mediante object_id cuando estén documentados.

Ejemplo conceptual:

OBJ-0001
→ actualiza →
OBJ-0002

La información detallada de cada objeto debe permanecer en:

knowledge/sap-objects/

No duplicar su documentación dentro de la relación.


==================================================
RELACIÓN CON PROCESSES
==================================================

Los procesos deben identificarse mediante process_id.

Ejemplo:

PROC-0001
→ utiliza →
OBJ-0001

La descripción completa del proceso permanece en:

knowledge/processes/


==================================================
RELACIÓN CON BUSINESS RULES
==================================================

Las reglas deben identificarse mediante rule_id.

Ejemplo:

PROC-0001
→ aplica →
BR-0001

La descripción completa de la regla permanece en:

knowledge/business-rules/


==================================================
NORMALIZACIÓN
==================================================

La base de conocimiento debe evitar duplicación.

No copiar:

- descripción completa de objetos;
- descripción completa de procesos;
- descripción completa de reglas;

dentro de relationships.

La relación debe almacenar principalmente:

SOURCE
RELATION
TARGET
CONTEXT
EVIDENCE
CERTAINTY

Esto permitirá mantener un Knowledge Base normalizado.


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

No utilizar datos sensibles como evidencia de relaciones.


==================================================
VERSIONADO
==================================================

Utilizar:

version: "1.0"

Aplicar:

PATCH:
Correcciones editoriales.

MINOR:
Información adicional sobre contexto o evidencia sin cambiar el significado de la relación.

MAJOR:
Cambio significativo en el tipo, dirección, alcance o significado de la relación.

Si una relación confirmada cambia, conservar la trazabilidad mediante Git.


==================================================
PREPARACIÓN PARA IA
==================================================

La estructura debe permitir que el futuro agente responda preguntas como:

- ¿Qué objetos intervienen en este proceso?
- ¿Qué procesos utilizan este objeto?
- ¿Qué reglas afectan este proceso?
- ¿Qué objeto actualiza esta tabla?
- ¿Qué programa ejecuta esta transacción?
- ¿Qué objetos están relacionados con este desarrollo?
- ¿Qué reglas implementa este desarrollo?
- ¿Qué evidencia demuestra esta relación?
- ¿Qué relaciones son inferidas?
- ¿Qué relaciones todavía deben validarse?
- ¿Qué procesos están conectados?
- ¿Qué tickets descubrieron o validaron esta relación?

El agente debe poder recorrer el Knowledge Base siguiendo relaciones:

OBJETO
→ PROCESO
→ REGLA
→ OBJETO
→ TICKET
→ EVIDENCIA

==================================================
REGLAS PARA EL AGENTE
==================================================

El agente que complete esta plantilla debe:

1. Buscar primero si la relación ya existe.
2. Evitar duplicar relaciones.
3. Reutilizar relationship_id cuando corresponda.
4. Validar que source_id exista o esté identificado explícitamente.
5. Validar que target_id exista o esté identificado explícitamente.
6. Utilizar vocabulario controlado.
7. Mantener la dirección de la relación.
8. No invertir automáticamente source y target.
9. No crear relaciones por simple co-ocurrencia.
10. No inventar evidencia.
11. Diferenciar relación confirmada de relación inferida.
12. Registrar contradicciones.
13. Registrar condiciones de aplicación.
14. Mantener referencias hacia objetos, procesos y reglas.
15. No duplicar la documentación de los elementos relacionados.
16. Mantener historial mediante Git.
17. No eliminar silenciosamente relaciones confirmadas.
18. Actualizar una relación existente cuando nueva evidencia cambie su nivel de certeza.
19. Si la relación deja de ser válida, marcarla según el estándar de versionado y conservar su historial.
20. Priorizar evidencia sobre inferencia.


==================================================
MODELO CONCEPTUAL DEL KNOWLEDGE GRAPH
==================================================

La estructura debe permitir construir conceptualmente un grafo:

                    ┌───────────────┐
                    │ SAP OBJECT    │
                    └───────┬───────┘
                            │
                         utiliza
                            │
                            ▼
                    ┌───────────────┐
                    │   PROCESS     │
                    └───────┬───────┘
                            │
                          aplica
                            │
                            ▼
                    ┌───────────────┐
                    │ BUSINESS RULE │
                    └───────┬───────┘
                            │
                       implementada
                            │
                            ▼
                    ┌───────────────┐
                    │ SAP OBJECT    │
                    └───────────────┘

Los tickets y documentos pueden actuar como evidencia y contexto:

TICKET
   │
   ├── documenta ──→ RELATIONSHIP
   │
   ├── documenta ──→ SAP OBJECT
   │
   ├── documenta ──→ PROCESS
   │
   └── documenta ──→ BUSINESS RULE

No implementar el grafo técnicamente en este archivo.

El objetivo de relationships.md es definir la estructura de conocimiento necesaria para que posteriormente un agente pueda construir o consultar dicho grafo.


==================================================
FORMATO FINAL
==================================================

El archivo final debe ser una plantilla Markdown limpia, profesional y reutilizable.

Debe contener:

1. YAML front matter.
2. Título "# Relación".
3. Metadata.
4. Las 16 secciones definidas.
5. Identificadores consistentes.
6. Vocabulario controlado.
7. Tablas donde aporten estructura.
8. Comentarios HTML breves para orientar al usuario.
9. Ninguna relación ficticia.
10. Ningún objeto SAP inventado.
11. Ningún proceso inventado.
12. Ninguna regla inventada.
13. Ninguna evidencia inventada.
14. Compatibilidad con los standards existentes.
15. Compatibilidad con knowledge/sap-objects/object.md.
16. Compatibilidad con knowledge/processes/process.md.
17. Compatibilidad con knowledge/business-rules/business-rule.md.

No agregues secciones adicionales fuera de las definidas.

No generes ejemplos reales de SAP.

No inventes relaciones.

No expliques el proceso de creación.
