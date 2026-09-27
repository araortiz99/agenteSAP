Quiero que crees el archivo:

knowledge/business-rules/business-rule.md

Este archivo será la plantilla maestra para documentar REGLAS DE NEGOCIO dentro del repositorio agenteSAP.

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

Ahora se debe crear:

knowledge/business-rules/business-rule.md

Esta plantilla permitirá documentar reglas de negocio como unidades de conocimiento independientes y reutilizables.

==================================================
OBJETIVO
==================================================

Una REGLA DE NEGOCIO representa una condición, restricción, criterio, decisión o comportamiento que determina cómo debe funcionar un proceso de negocio.

Debe responder, cuando corresponda:

- ¿Cuál es la regla?
- ¿Por qué existe?
- ¿A qué proceso aplica?
- ¿Cuándo se aplica?
- ¿Sobre qué datos se evalúa?
- ¿Cuál es la condición?
- ¿Qué sucede cuando se cumple?
- ¿Qué sucede cuando no se cumple?
- ¿Qué objetos SAP están involucrados?
- ¿Qué configuración la sustenta?
- ¿Qué evidencia demuestra que existe?
- ¿Qué documentación la define?
- ¿Está confirmada o requiere validación?

La regla debe poder existir independientemente de un ticket.

==================================================
PRINCIPIO FUNDAMENTAL
==================================================

Una regla de negocio debe representar:

CONDICIÓN
      ↓
EVALUACIÓN
      ↓
DECISIÓN
      ↓
COMPORTAMIENTO / RESULTADO

Conceptualmente:

SI [condición]
ENTONCES [resultado]
DE LO CONTRARIO [resultado alternativo]

No todas las reglas necesitan tener explícitamente una rama "de lo contrario", pero la estructura debe permitir documentarla cuando corresponda.

Una regla debe describir QUÉ debe ocurrir funcionalmente.

No debe describir HOW técnico salvo que el detalle técnico sea necesario para identificar o validar la regla.

==================================================
DIFERENCIA ENTRE REGLA DE NEGOCIO Y VALIDACIÓN
==================================================

Una regla de negocio define un comportamiento o criterio del negocio.

Una validación verifica que una condición requerida se cumpla.

Ejemplo conceptual:

Regla:
"Los materiales pertenecientes a determinado universo participan del proceso de inventario."

Validación:
"El material debe poseer la característica requerida para poder ser incluido."

No mezclar ambos conceptos.

Una regla puede tener una o varias validaciones asociadas.

==================================================
DIFERENCIA ENTRE REGLA DE NEGOCIO Y CONFIGURACIÓN
==================================================

Una configuración SAP puede implementar o soportar una regla.

Pero:

CONFIGURACIÓN ≠ REGLA

La regla debe documentar el comportamiento funcional.

La configuración debe registrarse como evidencia, mecanismo de implementación o dependencia cuando corresponda.

==================================================
METADATA
==================================================

El archivo debe comenzar obligatoriamente con YAML front matter:

---
rule_id: ""
rule_name: ""
rule_type: ""
module: ""
version: "1.0"
status: "draft"
date: ""
author: ""
---

Luego:

# Regla de Negocio

## Metadata

Utilizar una tabla:

| Campo | Valor |
|---|---|
| Rule ID | |
| Nombre de la regla | |
| Tipo de regla | |
| Módulo | |
| Versión | |
| Estado | |
| Fecha | |
| Autor | |

No inventar valores.

==================================================
RULE_ID
==================================================

Cada regla debe tener un identificador único y estable.

Utilizar:

BR-0001
BR-0002
BR-0003

El rule_id identifica la regla como conocimiento.

No utilizar ticket_id como identificador de la regla.

Una misma regla puede aparecer en múltiples procesos y tickets.

==================================================
RULE_TYPE
==================================================

Registrar el tipo de regla cuando corresponda.

Ejemplos:

- DETERMINATION
- VALIDATION
- RESTRICTION
- CALCULATION
- ELIGIBILITY
- AUTHORIZATION
- SELECTION
- TRANSFORMATION
- ACCOUNTING
- INVENTORY
- PURCHASING
- SALES
- INTEGRATION
- CONTROL
- OTHER

Si no se puede determinar:

"UNKNOWN"

No forzar una clasificación artificial.


==================================================
1. IDENTIFICACIÓN
==================================================

## 1. Identificación

Documentar:

- rule_id;
- nombre;
- tipo;
- módulo principal;
- módulos relacionados;
- origen de la regla;
- estado de conocimiento.

Distinguir cuando corresponda:

- regla estándar SAP;
- regla de negocio interna;
- regla derivada de configuración;
- regla implementada mediante desarrollo;
- regla contractual;
- regla fiscal;
- regla operativa;
- regla inferida.

No asumir que una regla es estándar SAP solamente porque se implemente mediante funcionalidades estándar.


==================================================
2. DESCRIPCIÓN
==================================================

## 2. Descripción

Describir claramente la regla en lenguaje funcional.

Debe poder entenderla un consultor funcional sin necesidad de leer código.

La descripción debe evitar ambigüedades.

Cuando sea posible, utilizar una formulación equivalente a:

"Cuando [condición], debe [comportamiento]."

No introducir ejemplos ficticios.


==================================================
3. OBJETIVO / JUSTIFICACIÓN
==================================================

## 3. Objetivo / Justificación

Explicar por qué existe la regla.

Puede corresponder a:

- necesidad de negocio;
- política interna;
- control operativo;
- requerimiento legal o fiscal;
- configuración SAP;
- integración;
- control contable;
- control de inventario;
- requerimiento funcional.

No especular sobre la motivación.

Si la justificación no está confirmada:

"Justificación pendiente de validar."


==================================================
4. ALCANCE
==================================================

## 4. Alcance

Definir dónde aplica la regla.

Puede incluir:

- módulos;
- procesos;
- sociedades;
- centros;
- almacenes;
- organizaciones;
- tipos de material;
- clases de documento;
- tipos de movimiento;
- usuarios;
- canales;
- sistemas;
- escenarios específicos.

Distinguir:

APLICA

de:

NO APLICA

cuando la información esté confirmada.


==================================================
5. CONDICIÓN DE APLICACIÓN
==================================================

## 5. Condición de aplicación

Documentar exactamente cuándo debe evaluarse la regla.

Utilizar una estructura clara:

### Evento

¿Qué evento inicia la evaluación?

### Condición

¿Qué condiciones deben cumplirse?

### Datos evaluados

¿Qué información se utiliza?

No inventar condiciones.

Si la condición es parcialmente conocida:

"Condición parcial — requiere validación."


==================================================
6. LÓGICA DE LA REGLA
==================================================

## 6. Lógica de la regla

Documentar la lógica funcional de manera estructurada.

Utilizar:

### SI

[condición]

### ENTONCES

[resultado]

### DE LO CONTRARIO

[resultado alternativo]

Cuando existan múltiples condiciones, identificarlas como:

COND-01
COND-02
COND-03

Cuando exista una secuencia de evaluación:

1.
2.
3.

No transformar la regla funcional en pseudocódigo técnico innecesario.


==================================================
7. DATOS INVOLUCRADOS
==================================================

## 7. Datos involucrados

Documentar los datos necesarios para evaluar la regla.

Pueden incluir:

- material;
- centro;
- almacén;
- sociedad;
- proveedor;
- cliente;
- cantidad;
- importe;
- fecha;
- documento;
- estado;
- clase de documento;
- tipo de movimiento;
- característica;
- indicador.

Utilizar una tabla:

| Dato | Descripción | Origen | Uso en la regla | Obligatorio |
|---|---|---|---|---|

No inventar campos técnicos.

Si se conoce un campo SAP, conservar su nombre técnico exacto.


==================================================
8. RESULTADO
==================================================

## 8. Resultado

Documentar qué ocurre cuando la regla se cumple.

Puede incluir:

- selección;
- bloqueo;
- autorización;
- cálculo;
- generación de documento;
- modificación de estado;
- contabilización;
- rechazo;
- derivación;
- envío a otro sistema;
- inclusión/exclusión de un registro.

Separar:

RESULTADO ESPERADO

de:

RESULTADO OBSERVADO

cuando la información provenga de una investigación o caso real.


==================================================
9. COMPORTAMIENTO CUANDO NO SE CUMPLE
==================================================

## 9. Comportamiento cuando no se cumple

Documentar qué ocurre cuando la condición de la regla no se satisface.

Puede ser:

- rechazo;
- exclusión;
- bloqueo;
- mensaje;
- derivación;
- procesamiento alternativo;
- ausencia de acción.

No asumir comportamiento.

Si no está confirmado:

"Comportamiento pendiente de validar."


==================================================
10. EXCEPCIONES
==================================================

## 10. Excepciones

Documentar situaciones donde la regla no se aplica o tiene un comportamiento especial.

Utilizar:

EXC-BR-01
EXC-BR-02

Para cada excepción:

| ID | Condición especial | Comportamiento | Evidencia |
|---|---|---|---|

No inventar excepciones.


==================================================
11. PRIORIDAD Y CONFLICTOS
==================================================

## 11. Prioridad y conflictos

Cuando existan múltiples reglas que puedan aplicarse simultáneamente, documentar:

- prioridad;
- precedencia;
- regla que prevalece;
- condición que determina la precedencia.

Utilizar:

PRIORIDAD-01

Si no se conoce la prioridad:

"Prioridad no confirmada."

No asumir que una regla prevalece sobre otra sin evidencia.


==================================================
12. OBJETOS SAP RELACIONADOS
==================================================

## 12. Objetos SAP relacionados

Relacionar la regla con objetos documentados en:

knowledge/sap-objects/

Pueden incluir:

- transacciones;
- tablas;
- programas;
- clases;
- funciones;
- movimientos;
- Fiori Apps;
- configuraciones;
- servicios;
- interfaces.

Utilizar:

| Object ID | Objeto | Tipo | Relación con la regla |
|---|---|---|---|

No duplicar la documentación completa del objeto.

Si el objeto está identificado pero todavía no documentado:

"Objeto identificado — documentación pendiente."


==================================================
13. PROCESOS RELACIONADOS
==================================================

## 13. Procesos relacionados

Relacionar la regla con procesos documentados en:

knowledge/processes/

Utilizar:

| Process ID | Proceso | Momento de aplicación | Impacto |
|---|---|---|---|

Una misma regla puede aplicar a múltiples procesos.

No crear procesos duplicados.


==================================================
14. CONFIGURACIÓN RELACIONADA
==================================================

## 14. Configuración relacionada

Documentar configuración SAP que soporte o implemente la regla.

Puede incluir:

- customizing;
- parámetros;
- tablas de configuración;
- tipos de movimiento;
- determinación de cuentas;
- clases de valoración;
- estructuras organizativas;
- características;
- condiciones;
- variantes.

Distinguir claramente:

REGLA DE NEGOCIO

de:

CONFIGURACIÓN QUE IMPLEMENTA O SOPORTA LA REGLA

No asumir que una configuración implementa una regla sin evidencia.


==================================================
15. IMPLEMENTACIÓN
==================================================

## 15. Implementación

Documentar cómo está implementada la regla cuando esta información esté confirmada.

Puede ser:

- estándar SAP;
- configuración;
- desarrollo Z;
- combinación de configuración y desarrollo;
- proceso manual;
- integración;
- otro mecanismo.

No describir código detalladamente.

Para información técnica específica, referenciar el objeto SAP correspondiente.


==================================================
16. VALIDACIONES
==================================================

## 16. Validaciones

Documentar validaciones asociadas a la regla.

Utilizar:

VAL-BR-01
VAL-BR-02

Para cada validación:

| ID | Validación | Momento | Resultado esperado | Evidencia |
|---|---|---|---|---|

Distinguir entre:

- regla;
- validación;
- resultado.


==================================================
17. EVIDENCIAS
==================================================

## 17. Evidencias

Registrar las fuentes que sustentan la existencia y comportamiento de la regla.

Utilizar:

EVID-BR-01
EVID-BR-02

Las evidencias pueden provenir de:

- documentación oficial SAP;
- especificaciones funcionales;
- configuración;
- pruebas;
- análisis;
- debug;
- investigaciones;
- tickets;
- documentación interna;
- comportamiento observado en SAP.

Utilizar:

| ID | Fuente | Tipo | Qué demuestra |
|---|---|---|---|

No inventar evidencias.

Una evidencia debe respaldar una afirmación concreta.


==================================================
18. NIVEL DE CERTEZA
==================================================

## 18. Nivel de certeza

Clasificar el estado del conocimiento de la regla.

Utilizar:

- CONFIRMADA
- PARCIAL
- EN VALIDACIÓN
- INFERIDA
- NO CONFIRMADA

Regla:

Una regla INFERIDA no debe presentarse como una regla confirmada.

Una regla observada en un único caso tampoco debe asumirse automáticamente como regla general.


==================================================
19. INFORMACIÓN PENDIENTE
==================================================

## 19. Información pendiente

Registrar aspectos que todavía deben investigarse o validarse.

Utilizar:

PEND-BR-01
PEND-BR-02

Tabla:

| ID | Información pendiente | Motivo | Acción requerida |
|---|---|---|---|

Si no existe información pendiente:

"N/A"


==================================================
20. DOCUMENTACIÓN RELACIONADA
==================================================

## 20. Documentación relacionada

Relacionar la regla con:

- requirements;
- functional specifications;
- functional tests;
- analysis;
- debug;
- investigations;
- procesos;
- objetos SAP;
- relaciones;
- tickets.

Utilizar referencias reales.

No inventar documentos.


==================================================
REGLAS DE NEGOCIO Y TICKETS
==================================================

Una regla es conocimiento permanente.

Un ticket representa un caso concreto.

Por lo tanto:

rule_id = identidad de la regla

ticket_id = caso donde la regla fue utilizada, investigada, modificada o cuestionada

No utilizar ticket_id como sustituto de rule_id.

Una misma regla puede estar relacionada con múltiples tickets.

Si un ticket descubre que una regla previamente documentada era incorrecta, debe actualizarse la regla mediante el mecanismo de versionado correspondiente.


==================================================
REGLAS DE NEGOCIO Y PROCESOS
==================================================

Una regla puede:

- aplicar a un proceso;
- aplicar a varios procesos;
- determinar una etapa;
- controlar una decisión;
- determinar un resultado;
- generar una excepción.

La relación formal debe poder representarse también en:

knowledge/relationships/

No duplicar innecesariamente la información.


==================================================
REGLAS DE NEGOCIO Y OBJETOS SAP
==================================================

Una regla puede estar implementada mediante:

- configuración;
- transacción;
- programa;
- tabla;
- clase;
- función;
- movimiento;
- Fiori;
- integración;
- combinación de objetos.

No confundir:

"El objeto implementa la regla"

con:

"El objeto está relacionado con la regla"

La primera afirmación requiere evidencia de implementación.


==================================================
REGLAS ESTÁNDAR VS REGLAS INTERNAS
==================================================

Distinguir:

SAP_STANDARD

Regla definida por comportamiento estándar documentado de SAP.

BUSINESS

Regla propia del negocio.

CONFIGURATION

Regla derivada o determinada mediante configuración.

CUSTOM

Regla implementada mediante desarrollo personalizado.

FISCAL / LEGAL

Regla derivada de una obligación fiscal o legal, cuando esté debidamente documentada.

INFERRED

Regla inferida a partir de evidencia pero todavía no confirmada.

UNKNOWN

Origen no confirmado.

No clasificar una regla como SAP_STANDARD únicamente porque se observe en un sistema SAP.


==================================================
REGLAS PARA CÁLCULOS
==================================================

Cuando una regla incluya cálculos, documentar explícitamente:

- variables;
- fórmula;
- unidad;
- redondeo;
- condiciones;
- límites;
- resultado esperado.

Utilizar una estructura como:

Variable:
Descripción:

Fórmula:

Unidad:

Redondeo:

Condiciones:

No inventar fórmulas ni valores.


==================================================
REGLAS TEMPORALES
==================================================

Cuando una regla dependa de:

- fecha;
- período;
- vigencia;
- ejercicio;
- horario;
- campaña;
- versión;

documentar explícitamente la condición temporal.

No asumir que una regla es permanente.

Cuando exista fecha de vigencia:

indicarla.

Cuando no esté confirmada:

"Vigencia pendiente de validar."


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

Los valores utilizados como ejemplos no deben representar información sensible real.


==================================================
VERSIONADO
==================================================

Utilizar:

version: "1.0"

Aplicar:

PATCH:
Correcciones editoriales.

MINOR:
Información adicional que no cambia la lógica de la regla.

MAJOR:
Cambio significativo en la lógica, alcance, condición, resultado o interpretación de la regla.

Cuando una regla cambia funcionalmente, conservar la trazabilidad mediante Git.


==================================================
PREPARACIÓN PARA IA
==================================================

La estructura debe permitir que el futuro agente responda preguntas como:

- ¿Qué reglas aplican a este proceso?
- ¿Qué regla aplica a este material?
- ¿Qué condición determina este comportamiento?
- ¿Qué ocurre cuando una condición no se cumple?
- ¿Qué reglas afectan este objeto SAP?
- ¿Qué reglas aplican a este tipo de movimiento?
- ¿Qué configuración implementa esta regla?
- ¿Qué evidencia demuestra esta regla?
- ¿Esta regla es estándar SAP o propia del negocio?
- ¿Qué tickets están relacionados con esta regla?
- ¿Qué reglas entran en conflicto?
- ¿Cuál tiene prioridad?
- ¿Qué parte de la regla todavía necesita validación?

Por esta razón:

- utilizar rule_id estable;
- mantener condiciones explícitas;
- separar regla de implementación;
- mantener evidencia;
- registrar incertidumbre;
- relacionar reglas con procesos y objetos;
- evitar duplicación.


==================================================
REGLAS PARA EL AGENTE
==================================================

El agente que complete esta plantilla debe:

1. Buscar primero si la regla ya existe.
2. Evitar crear reglas duplicadas.
3. Reutilizar rule_id cuando corresponda.
4. No crear una nueva regla solamente porque aparezca en un nuevo ticket.
5. Diferenciar una modificación de una nueva regla.
6. Mantener las relaciones existentes.
7. Agregar nuevas evidencias.
8. Registrar contradicciones.
9. No inventar condiciones.
10. No inventar valores.
11. No inventar fórmulas.
12. No inventar prioridades.
13. No asumir comportamiento estándar.
14. Diferenciar regla de configuración.
15. Diferenciar regla de validación.
16. Registrar información pendiente.
17. Mantener historial mediante Git.
18. No eliminar silenciosamente conocimiento confirmado.


==================================================
ESTRUCTURA DE CONOCIMIENTO
==================================================

La regla debe integrarse con el modelo general:

SAP OBJECTS
    │
    ├── relacionados con
    │
    ▼
PROCESSES
    │
    ├── aplican
    │
    ▼
BUSINESS RULES
    │
    ├── sustentadas por
    │
    ▼
EVIDENCE
    │
    └── relacionadas con
         │
         ▼
      TICKETS

La relación entre estos elementos debe poder documentarse formalmente en:

knowledge/relationships/


==================================================
FORMATO FINAL
==================================================

El archivo final debe ser una plantilla Markdown limpia, profesional y reutilizable.

Debe contener:

1. YAML front matter.
2. Título "# Regla de Negocio".
3. Metadata.
4. Las 20 secciones definidas.
5. Identificadores consistentes.
6. Tablas donde aporten estructura.
7. Comentarios HTML breves para orientar al usuario.
8. Ningún dato ficticio.
9. Ninguna regla de negocio de ejemplo.
10. Ninguna fórmula inventada.
11. Ningún objeto SAP inventado.
12. Ninguna relación inventada.
13. Compatibilidad con los standards existentes.
14. Compatibilidad con templates existentes.
15. Compatibilidad con knowledge/sap-objects/object.md.
16. Compatibilidad con knowledge/processes/process.md.

No agregues secciones adicionales fuera de las definidas.

No generes ejemplos de reglas reales.

No inventes información SAP.

No expliques el proceso de creación.

