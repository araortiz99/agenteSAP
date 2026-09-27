Actúa como arquitecto de información y especialista en diseño de agentes de conocimiento para SAP.

Necesito generar el archivo:

agent/generation.md

Este archivo debe definir formalmente el mecanismo mediante el cual el agente SAP genera documentos funcionales a partir de una solicitud del usuario.

IMPORTANTE:

- Este archivo NO debe contener documentos funcionales concretos.
- No debe contener ejemplos extensos de incidentes reales.
- No debe inventar información SAP.
- No debe reemplazar a promptMaestro.
- No debe reemplazar standards/documentation-standard.md.
- No debe reemplazar los templates.
- Debe definir el proceso operativo que conecta:
  
  usuario → tipo documental → template → contexto → knowledge → sources → generación → validación → documento.

La arquitectura existente del repositorio es:

agenteSAP/
├── agent/
│   └── agent.md
├── knowledge/
│   ├── business-rules/
│   ├── processes/
│   ├── relationships/
│   ├── sap-objects/
│   └── sources/
├── standards/
│   ├── documentation-standard.md
│   ├── knowledge-classification-standard.md
│   ├── security-standard.md
│   └── versioning-standard.md
├── templates/
│   ├── analysis.md
│   ├── functional-specification.md
│   ├── functional-tests.md
│   ├── investigation.md
│   └── requirement.md
├── tickets/
│   ├── index.md
│   └── ticket.md
└── promptMaestro

Los templates existentes representan la especificación de:
- qué debe contener cada documento;
- cómo debe construirse;
- qué reglas debe seguir el agente para generarlo.

El documento generado será una instancia concreta y no debe confundirse con el template.

==================================================
OBJETIVO DEL ARCHIVO
==================================================

Definir un Generation Contract para que el agente pueda recibir solicitudes como:

- "Generá el análisis del ticket 31426."
- "Creá la especificación funcional para este requerimiento."
- "Documentá el debug realizado."
- "Generá las pruebas funcionales."
- "Actualizá el análisis existente."
- "Convertí esta investigación en documentación funcional."

y determinar de forma controlada:

1. qué documento debe generar;
2. qué template debe utilizar;
3. qué información debe recuperar;
4. qué información puede utilizar;
5. qué información debe marcar como desconocida;
6. cómo debe construir el documento;
7. cómo debe validarlo;
8. cómo debe versionarlo;
9. cómo debe mantener trazabilidad;
10. cuándo una información descubierta puede convertirse en Knowledge reutilizable.

==================================================
PRINCIPIOS OBLIGATORIOS
==================================================

El mecanismo de generación debe cumplir:

1. No inventar información.
2. No transformar inferencias en hechos.
3. Mantener separación entre:
   - documentación;
   - conocimiento reutilizable;
   - fuentes;
   - evidencia;
   - contexto de ticket.
4. Respetar la clasificación:
   - knowledge_type;
   - knowledge_scope;
   - certainty;
   - SAP object origin;
   - implementation_type;
   - source origin;
   - source type.
5. Mantener ticket_id como identificador transversal cuando corresponda.
6. Mantener trazabilidad hacia las fuentes utilizadas.
7. No duplicar información que ya existe como Knowledge.
8. Reutilizar Knowledge existente en lugar de copiarlo innecesariamente.
9. No promover automáticamente cualquier información documentada a Knowledge reusable.
10. Distinguir claramente información confirmada, parcial, pendiente, inferida y no confirmada.
11. Respetar security-standard.md.
12. Respetar documentation-standard.md.
13. Respetar knowledge-classification-standard.md.
14. Respetar versioning-standard.md.
15. Utilizar el template correspondiente antes de generar un documento.
16. Si existe un documento previo, actualizarlo o versionarlo en lugar de crear duplicados.
17. El agente es consultivo y documental. No ejecuta cambios en SAP.

==================================================
ESTRUCTURA OBLIGATORIA DE generation.md
==================================================

Generá el documento con las siguientes secciones:

# Generation Contract

## 1. Purpose

Explicar la finalidad del mecanismo de generación documental.

## 2. Scope

Definir qué tipos de documentos cubre y qué queda fuera.

## 3. Generation Lifecycle

Definir formalmente el flujo:

REQUEST
→ DOCUMENT TYPE IDENTIFICATION
→ TEMPLATE SELECTION
→ TICKET RESOLUTION
→ CONTEXT RETRIEVAL
→ KNOWLEDGE RETRIEVAL
→ SOURCE RETRIEVAL
→ EVIDENCE ANALYSIS
→ DOCUMENT GENERATION
→ VALIDATION
→ VERSIONING
→ TRACEABILITY
→ OUTPUT
→ KNOWLEDGE PROMOTION EVALUATION

Explicar cada etapa.

## 4. Document Type Identification

Definir cómo el agente determina el tipo documental solicitado.

Debe contemplar como mínimo:

- REQUIREMENT
- ANALYSIS
- DEBUG
- INVESTIGATION
- FUNCTIONAL_SPECIFICATION
- FUNCTIONAL_TESTS

Si la intención no es suficientemente clara, el agente debe pedir aclaración en lugar de elegir arbitrariamente.

## 5. Template Selection

Definir cómo se selecciona:

templates/<document_type>.md

Debe existir una correspondencia controlada entre document_type y template.

El agente nunca debe generar un documento funcional ignorando el template correspondiente.

## 6. Standard Selection

Definir qué standards deben consultarse antes de generar.

Como mínimo:

- documentation-standard.md
- knowledge-classification-standard.md
- versioning-standard.md
- security-standard.md

Explicar cuándo cada uno es obligatorio.

## 7. Ticket Resolution

Definir cómo identificar el ticket asociado.

Prioridad:

1. ticket_id explícitamente proporcionado;
2. ticket_id encontrado en contexto;
3. ticket_id identificado mediante documentos relacionados;
4. si realmente no existe, utilizar el mecanismo definido para documentos sin ticket.

No inventar ticket_id.

## 8. Context Retrieval

Definir cómo recuperar contexto del ticket.

Debe contemplar:

- ticket;
- documentos existentes;
- cronología;
- decisiones;
- solución;
- validaciones;
- pendientes;
- documentos relacionados.

El contexto del ticket debe considerarse contexto histórico y no necesariamente verdad universal.

## 9. Knowledge Retrieval

Definir cómo recuperar conocimiento reusable relacionado.

Debe contemplar:

- SAP Objects;
- Processes;
- Business Rules;
- Relationships;
- Sources.

El agente debe buscar primero Knowledge existente antes de crear información redundante.

Debe diferenciar:

- conocimiento aplicable directamente;
- conocimiento relacionado;
- conocimiento potencialmente aplicable;
- conocimiento contradictorio.

## 10. Source Retrieval

Definir cómo recuperar y utilizar Sources.

Las fuentes deben clasificarse según:

- origin;
- source_type;
- reliability;
- certainty.

Definir prioridad de evidencia.

Como regla general:

direct evidence
>
official SAP documentation
>
confirmed configuration
>
confirmed code
>
functional test
>
internal documentation
>
analysis
>
inference

No presentar una inferencia como hecho confirmado.

## 11. Evidence Handling

Definir cómo el agente debe manejar:

- evidencia directa;
- evidencia documental;
- evidencia técnica;
- evidencia de pruebas;
- evidencia de debug;
- evidencia parcial;
- ausencia de evidencia.

Cuando no exista evidencia suficiente, debe indicarlo explícitamente.

## 12. Information Gaps

Definir el comportamiento ante información faltante.

El agente debe:

- identificar qué falta;
- distinguir dato desconocido de dato no aplicable;
- marcar información pendiente;
- solicitar información cuando sea indispensable;
- continuar con la generación cuando sea posible;
- no completar campos críticos mediante suposiciones.

Utilizar estados claros como:

- confirmed;
- partial;
- under_validation;
- inferred;
- not_confirmed.

## 13. Document Generation

Definir cómo construir el documento final.

El agente debe:

1. cargar el template;
2. interpretar sus instrucciones;
3. recuperar contexto;
4. recuperar Knowledge;
5. recuperar Sources;
6. estructurar la información;
7. clasificar hechos;
8. completar metadata;
9. generar el contenido;
10. registrar pendientes.

La estructura del documento generado debe respetar el template.

## 14. Fact and Inference Separation

Definir reglas para separar:

- hecho confirmado;
- información proporcionada por el usuario;
- evidencia;
- análisis;
- hipótesis;
- inferencia;
- pendiente de validación.

Nunca convertir una hipótesis en una afirmación factual.

## 15. Validation

Definir una validación previa a la entrega.

Como mínimo:

### Structural validation
- estructura correcta;
- secciones requeridas;
- metadata completa.

### Content validation
- coherencia;
- ausencia de contradicciones;
- información suficiente.

### Evidence validation
- trazabilidad;
- fuentes identificables;
- incertidumbre correctamente indicada.

### Classification validation
- knowledge_type;
- knowledge_scope;
- certainty;
- SAP object classification;
- source classification.

### Security validation
- ausencia de credenciales;
- ausencia de secretos;
- ausencia de información sensible innecesaria.

### Version validation
- versión correcta;
- historial consistente;
- actualización en lugar de duplicación.

## 16. Versioning

Definir cómo se determina la versión del documento.

Diferenciar:

- versión documental;
- historial Git;
- cambio menor;
- cambio estructural;
- corrección;
- nueva información;
- modificación funcional.

Respetar versioning-standard.md.

## 17. Traceability

Todo documento generado debe poder responder:

- ¿qué ticket originó el documento?
- ¿qué información fue utilizada?
- ¿qué Knowledge fue consultado?
- ¿qué Sources fueron utilizados?
- ¿qué documentos relacionados existen?
- ¿qué información quedó pendiente?

La trazabilidad debe ser explícita.

## 18. Existing Document Handling

Definir qué ocurre si ya existe un documento del mismo tipo para el mismo ticket.

El agente debe:

1. buscar el documento existente;
2. determinar si corresponde actualizarlo;
3. identificar cambios;
4. incrementar versión cuando corresponda;
5. preservar trazabilidad;
6. evitar documentos duplicados.

## 19. Knowledge Promotion

Definir el proceso mediante el cual una información descubierta durante la documentación puede convertirse en Knowledge reusable.

Debe existir una separación explícita:

DOCUMENTATION
→ DISCOVERY
→ CANDIDATE KNOWLEDGE
→ VALIDATION
→ REUSABLE KNOWLEDGE

La generación de un documento NO implica automáticamente la creación de Knowledge.

Para promover información a Knowledge debe existir evidencia suficiente y clasificación adecuada.

## 20. Conflict Handling

Definir qué ocurre cuando:

- dos Sources contradicen;
- un documento contradice Knowledge;
- un ticket histórico contradice una configuración actual;
- existe información antigua y nueva.

El agente no debe ocultar conflictos.

Debe preservar:

- fuente;
- fecha;
- contexto;
- certeza;
- estado.

## 21. Output Contract

Definir qué debe contener una salida generada.

Como mínimo:

- metadata;
- document_type;
- ticket_id;
- version;
- status;
- date;
- author;
- knowledge classification;
- content;
- sources/evidence;
- related knowledge;
- pending information.

## 22. Human Review

Definir cuándo el documento puede considerarse:

- draft;
- in_review;
- approved;
- validated;
- implemented;
- obsolete.

El agente no debe asumir aprobación humana si esta no fue indicada.

## 23. Agent Rules

Cerrar con reglas operativas resumidas:

- no inventar;
- no duplicar;
- no ocultar incertidumbre;
- no mezclar estándar y custom;
- no mezclar ticket context con reusable knowledge;
- mantener trazabilidad;
- respetar templates;
- respetar standards;
- versionar;
- preservar historial;
- solicitar aclaración cuando sea indispensable.

## 24. Generation Checklist

Crear una checklist final que el agente pueda utilizar antes de entregar cualquier documento.

Debe ser concreta y verificable.

==================================================
FORMATO
==================================================

Usar Markdown limpio.

Usar tablas solamente cuando realmente aporten claridad.

Utilizar YAML únicamente para metadata o estructuras donde sea necesario.

No agregar contenido inventado.

No crear todavía ejemplos reales de tickets.

El resultado debe ser una especificación normativa y operativa del mecanismo de generación documental del agente SAP.
