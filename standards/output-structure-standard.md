Actúa como arquitecto de repositorios de conocimiento y especialista en gestión documental para agentes de IA orientados a SAP.


Este archivo debe definir de forma normativa dónde y cómo se almacenan los documentos generados por el agente SAP.

==================================================
OBJETIVO PRINCIPAL
==================================================

La regla fundamental del repositorio es:

Todo documento generado asociado a un ticket debe almacenarse dentro de:

tickets/<ticket_id>/

El ticket_id es el identificador transversal del caso.

Por lo tanto, la estructura física principal será:

tickets/
└── <ticket_id>/
    ├── ticket.md
    ├── requirement.md
    ├── analysis.md
    ├── debug.md
    ├── investigation.md
    ├── functional-specification.md
    └── functional-tests.md

Los documentos son opcionales según las necesidades del ticket.

No todos los tickets deben contener todos los tipos documentales.

==================================================
ARQUITECTURA EXISTENTE
==================================================

El repositorio contiene:

tickets/
├── index.md
└── ticket.md

templates/
├── analysis.md
├── functional-specification.md
├── functional-tests.md
├── investigation.md
└── requirement.md

knowledge/
├── business-rules/
├── processes/
├── relationships/
├── sap-objects/
└── sources/

standards/
├── documentation-standard.md
├── knowledge-classification-standard.md
├── security-standard.md
└── versioning-standard.md

agent/
├── agent.md
└── generation.md

promptMaestro

El archivo output-structure-standard.md debe complementar estos documentos y no reemplazarlos.

==================================================
RESPONSABILIDAD DE ESTE STANDARD
==================================================

Este archivo debe definir exclusivamente:

1. dónde se almacenan los documentos;
2. cómo se estructura cada ticket;
3. cómo se nombran los archivos;
4. qué documentos puede contener un ticket;
5. cómo se relacionan los documentos con ticket_id;
6. cómo se actualizan los documentos existentes;
7. cómo se manejan las versiones;
8. cómo se mantiene la trazabilidad;
9. cómo se actualiza tickets/index.md;
10. cómo se referencian Knowledge y Sources.

No debe definir nuevamente:

- el contenido de cada documento;
- la estructura interna de requirement.md;
- la estructura interna de analysis.md;
- la estructura interna de debug.md;
- las reglas generales de documentación;
- las reglas generales de clasificación;
- las reglas generales de versionado.

Estas responsabilidades pertenecen respectivamente a:

templates/
standards/documentation-standard.md
standards/knowledge-classification-standard.md
standards/versioning-standard.md

==================================================
ESTRUCTURA FÍSICA OBLIGATORIA
==================================================

La estructura de tickets debe ser:

tickets/
├── index.md
├── <ticket_id>/
│   ├── ticket.md
│   ├── requirement.md
│   ├── analysis.md
│   ├── debug.md
│   ├── investigation.md
│   ├── functional-specification.md
│   └── functional-tests.md

Reglas:

1. Cada ticket debe tener su propio directorio.

2. El nombre del directorio debe ser exactamente el ticket_id.

3. ticket.md representa el contexto principal del ticket.

4. Los demás documentos representan documentación especializada asociada al ticket.

5. Los documentos especializados son opcionales.

6. El agente solamente debe crear un documento cuando exista una necesidad documental correspondiente.

7. No deben crearse archivos vacíos para completar la estructura.

8. No deben crearse documentos duplicados.

9. No deben almacenarse documentos de tickets fuera de su directorio correspondiente.

==================================================
NOMENCLATURA DE ARCHIVOS
==================================================

Utilizar nombres de archivo determinísticos en lowercase-kebab-case.

Definir la correspondencia:

requirement
→ requirement.md

analysis
→ analysis.md

debug
→ debug.md

investigation
→ investigation.md

functional-specification
→ functional-specification.md

functional-tests
→ functional-tests.md

ticket
→ ticket.md

La nomenclatura debe mantenerse estable.

No utilizar nombres dinámicos como:

analysis-v2.md
analysis-final.md
analysis-final-final.md
nuevo-analysis.md

La versión pertenece a la metadata del documento y al historial Git, no al nombre del archivo.

==================================================
DOCUMENTOS POR TICKET
==================================================

Un ticket puede contener uno o varios de los siguientes documentos:

- ticket.md
- requirement.md
- analysis.md
- debug.md
- investigation.md
- functional-specification.md
- functional-tests.md

Definir que:

ticket.md
= contexto principal del ticket.

requirement.md
= requerimiento funcional identificado.

analysis.md
= análisis funcional o técnico realizado.

debug.md
= documentación de una actividad de debug.

investigation.md
= investigación realizada para comprender un problema o comportamiento.

functional-specification.md
= especificación funcional de una solución.

functional-tests.md
= pruebas funcionales y resultados.

Un documento no debe utilizarse para almacenar información que corresponde naturalmente a otro tipo documental.

==================================================
GENERACIÓN DE DOCUMENTOS
==================================================

Cuando el agente recibe una solicitud de generación documental:

1. identificar el ticket_id;
2. localizar tickets/<ticket_id>/;
3. identificar document_type;
4. seleccionar el template correspondiente;
5. verificar si ya existe el documento;
6. recuperar contexto y Knowledge;
7. generar o actualizar el documento;
8. validar el documento;
9. guardar el documento en tickets/<ticket_id>/;
10. actualizar tickets/index.md cuando corresponda.

La ubicación física del documento debe ser determinística.

Ejemplo:

ticket_id = 31426
document_type = analysis

Salida:

tickets/31426/analysis.md

==================================================
ACTUALIZACIÓN DE DOCUMENTOS
==================================================

Si el documento correspondiente ya existe:

NO crear otro archivo.

El agente debe:

1. localizar el documento;
2. analizar su contenido actual;
3. identificar nueva información;
4. determinar el impacto del cambio;
5. actualizar el documento;
6. incrementar la versión según versioning-standard.md;
7. mantener la trazabilidad.

La existencia de un nuevo análisis no implica automáticamente crear:

analysis-2.md
analysis-v2.md
analysis-new.md

==================================================
VERSIONADO
==================================================

Las versiones documentales no deben formar parte del nombre físico del archivo.

Ejemplo correcto:

tickets/31426/analysis.md

con metadata:

version: "1.1"

No utilizar:

tickets/31426/analysis-v1.1.md

El historial de cambios debe mantenerse mediante:

1. metadata del documento;
2. historial definido por versioning-standard.md;
3. historial Git.

El standard debe evitar duplicación innecesaria de archivos.

==================================================
TICKET.MD
==================================================

Cada ticket debe utilizar:

tickets/<ticket_id>/ticket.md

Este documento representa el contexto general del ticket.

Debe contener o referenciar:

- identificación del ticket;
- título;
- tipo;
- módulo;
- prioridad;
- estado;
- fechas;
- clasificación;
- contexto;
- documentación relacionada;
- Knowledge relacionado;
- Sources;
- estado actual;
- conclusión o solución cuando corresponda.

No debe duplicar completamente el contenido de:

analysis.md
debug.md
functional-specification.md
functional-tests.md

Debe funcionar como punto de entrada del caso.

==================================================
TICKETS/INDEX.MD
==================================================

tickets/index.md funciona como índice general de tickets.

No debe contener el contenido completo de cada ticket.

Debe permitir localizar rápidamente:

- ticket_id;
- título;
- tipo;
- módulo;
- prioridad;
- estado;
- knowledge_type;
- knowledge_scope;
- fecha de apertura;
- fecha de actualización;
- fecha de cierre;
- ruta.

La ruta debe apuntar al directorio:

tickets/<ticket_id>/

El índice debe actualizarse cuando se cree o modifique un ticket de acuerdo con las reglas establecidas.

==================================================
RELACIÓN CON KNOWLEDGE
==================================================

Los documentos almacenados en:

tickets/<ticket_id>/

pueden referenciar Knowledge reusable ubicado en:

knowledge/sap-objects/
knowledge/processes/
knowledge/business-rules/
knowledge/relationships/
knowledge/sources/

El ticket NO debe copiar el contenido completo de Knowledge.

Debe utilizar referencias estables.

Ejemplo conceptual:

analysis.md
→ SAP Object: ZMM_IMX_0004
→ Process: SNC Logístico
→ Business Rule: ...
→ Source: ...

La documentación del ticket conserva el contexto específico del caso.

Knowledge conserva conocimiento reusable.

==================================================
RELACIÓN CON SOURCES
==================================================

Los documentos pueden utilizar Sources para respaldar información.

Las referencias deben permitir identificar:

- qué Source fue utilizada;
- qué información aporta;
- qué documento utiliza esa Source;
- cuándo fue utilizada cuando corresponda.

No duplicar innecesariamente el contenido de la Source.

==================================================
SEPARACIÓN ENTRE DOCUMENTACIÓN Y KNOWLEDGE
==================================================

Debe mantenerse estrictamente la separación:

tickets/
=
documentación contextual e histórica.

knowledge/
=
conocimiento reusable.

Un hecho descubierto durante un ticket no se convierte automáticamente en Knowledge reusable.

El flujo es:

DOCUMENTACIÓN
→ DESCUBRIMIENTO
→ CANDIDATE KNOWLEDGE
→ VALIDACIÓN
→ KNOWLEDGE REUSABLE

Las reglas de promoción se encuentran en agent/generation.md.

==================================================
DOCUMENTOS SIN TICKET
==================================================

No crear dentro de tickets documentos que no estén asociados a un ticket.

Si una información constituye conocimiento reusable y no pertenece a un ticket específico, debe evaluarse su incorporación en:

knowledge/

según el tipo de Knowledge correspondiente.

No crear una estructura paralela de documentos fuera de tickets/ salvo que exista una decisión arquitectónica explícita posterior.

==================================================
REFERENCIAS
==================================================

Las referencias internas deben utilizar identificadores estables.

Cuando exista un identificador formal, utilizarlo en lugar de depender exclusivamente del nombre o texto libre.

Las referencias pueden incluir:

- ticket_id;
- document_id si posteriormente se define;
- SAP Object;
- Process;
- Business Rule;
- Relationship;
- Source.

No introducir document_id como requisito obligatorio si no está definido formalmente por la arquitectura vigente.

==================================================
DOCUMENT_ID
==================================================

No crear document_id como requisito de almacenamiento físico en esta etapa.

El documento se identifica mínimamente mediante:

ticket_id + document_type

Ejemplo:

31426 + analysis

→ tickets/31426/analysis.md

Si en una fase posterior el modelo de Knowledge Graph requiere un identificador formal para DOCUMENT, document_id podrá incorporarse mediante una modificación arquitectónica explícita.

==================================================
DOCUMENTOS MÚLTIPLES DEL MISMO TIPO
==================================================

Por defecto, un ticket tendrá como máximo un documento activo por tipo documental.

Ejemplo:

tickets/31426/analysis.md

Si el análisis cambia:

→ actualizar y versionar analysis.md.

No crear múltiples análisis independientes salvo que exista una razón documental explícita.

Si realmente existen documentos conceptualmente distintos, deben evaluarse como documentos relacionados y no como duplicados del mismo tipo.

==================================================
ELIMINACIÓN Y OBSOLESCENCIA
==================================================

No eliminar documentos únicamente porque fueron reemplazados.

La preservación histórica debe priorizarse.

Cuando un documento deje de ser aplicable:

- utilizar el estado correspondiente;
- registrar su obsolescencia;
- mantener el historial Git;
- conservar trazabilidad.

La eliminación física debe ser excepcional y estar sujeta a las reglas de documentación y seguridad.

==================================================
VALIDACIÓN DE SALIDA
==================================================

Antes de considerar generado un documento, verificar:

[ ] Existe ticket_id válido.
[ ] Existe tickets/<ticket_id>/.
[ ] El document_type es válido.
[ ] El nombre del archivo es correcto.
[ ] El documento utiliza el template correspondiente.
[ ] No existe un documento duplicado.
[ ] La metadata es válida.
[ ] La versión es correcta.
[ ] Las referencias son trazables.
[ ] Knowledge no fue duplicado.
[ ] Sources están correctamente referenciadas.
[ ] No existen secretos o información sensible.
[ ] El documento cumple documentation-standard.md.
[ ] El documento cumple knowledge-classification-standard.md.
[ ] El documento cumple versioning-standard.md.

==================================================
ESTRUCTURA FINAL DEL STANDARD
==================================================

El archivo generado debe contener únicamente las siguientes secciones:

# Output Structure Standard

## 1. Purpose

## 2. Scope

## 3. Repository Output Model

## 4. Ticket Directory Structure

## 5. Document Types

## 6. File Naming Convention

## 7. Ticket.md

## 8. Document Generation Output

## 9. Document Update and Versioning

## 10. Ticket Index

## 11. Knowledge References

## 12. Source References

## 13. Separation Between Documentation and Knowledge

## 14. Multiple Documents

## 15. Obsolescence and Preservation

## 16. Output Validation

## 17. Final Rules

==================================================
REGLAS FINALES
==================================================

El resultado debe ser simple, determinístico y operativo.

La regla principal debe quedar inequívocamente establecida:

DOCUMENT GENERATED FOR TICKET
→ tickets/<ticket_id>/<document_type>.md

No generar una arquitectura alternativa.

No crear estructuras paralelas innecesarias.

No duplicar contenido de Knowledge.

No utilizar versiones en los nombres de archivo.

No crear archivos duplicados por cada interacción.

No inventar entidades.

No introducir document_id como requisito obligatorio en esta etapa.

El objetivo del standard es que cualquier agente o persona pueda determinar exactamente dónde debe quedar almacenado un documento generado.
