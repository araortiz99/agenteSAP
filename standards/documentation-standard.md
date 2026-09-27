Actúa como arquitecto de conocimiento, consultor funcional SAP senior y especialista en diseño de bases de conocimiento para agentes de IA.

Debes actualizar:

standards/documentation-standard.md

OBJETIVO DEL CAMBIO

Incorporar al estándar documental una clasificación transversal que permita al agente distinguir:

1. conocimiento SAP estándar;
2. conocimiento SAP custom;
3. conocimiento mixto;
4. conocimiento cuyo origen todavía no está confirmado.

IMPORTANTE

No elimines ninguna regla funcional existente.

No cambies los tipos oficiales de documentación.

No reemplaces ticket_id.

No conviertas knowledge_type en sustituto de document_type.

--------------------------------------------------
1. NUEVA METADATA OBLIGATORIA
--------------------------------------------------

Todo documento de conocimiento o documentación funcional debe incorporar:

knowledge_type:
knowledge_scope:

La metadata base debe quedar conceptualmente:

---
ticket_id: ""
document_type: ""
knowledge_type: ""
knowledge_scope: ""
version: "1.0"
status: "draft"
date: ""
author: ""
---

Cuando un documento no esté asociado a ticket:

ticket_id: "N/A"

--------------------------------------------------
2. KNOWLEDGE_TYPE
--------------------------------------------------

Definir exclusivamente:

standard
custom
mixed
unknown

STANDARD

Utilizar cuando el contenido documentado representa comportamiento, proceso, regla o funcionalidad SAP estándar y existe evidencia suficiente.

CUSTOM

Utilizar cuando el contenido representa comportamiento específico de una organización, desarrollo Z/Y, integración propia, configuración particular o implementación específica.

MIXED

Utilizar cuando el documento contiene conocimiento estándar y custom de manera relevante.

UNKNOWN

Utilizar cuando no existe evidencia suficiente para determinar el origen.

--------------------------------------------------
3. REGLAS DE CLASIFICACIÓN
--------------------------------------------------

El agente debe:

- no clasificar como STANDARD solamente porque el objeto se utiliza dentro de SAP;
- no clasificar como CUSTOM solamente porque el comportamiento observado sea diferente;
- no convertir un nombre técnico en evidencia suficiente;
- utilizar evidencia disponible;
- conservar UNKNOWN cuando no pueda determinar el origen;
- utilizar MIXED cuando el documento combine conocimiento estándar y custom.

Los nombres Z o Y pueden utilizarse como indicio de desarrollo personalizado, pero no deben considerarse por sí solos evidencia definitiva.

--------------------------------------------------
4. KNOWLEDGE_SCOPE
--------------------------------------------------

Definir:

global
organization
country
company
plant
process
project
ticket
unknown

Explicar el significado de cada valor.

knowledge_scope determina el ámbito de aplicación del conocimiento.

No utilizar knowledge_scope para indicar si algo es estándar o custom.

Ejemplo:

knowledge_type: custom
knowledge_scope: company

--------------------------------------------------
5. STANDARD VS CUSTOM
--------------------------------------------------

Incorporar una sección normativa que establezca:

SAP STANDARD
=
funcionalidad o comportamiento proporcionado por SAP.

SAP CUSTOM
=
desarrollo, configuración, extensión, integración o comportamiento específico de la organización.

El agente debe distinguir entre:

- objeto SAP estándar;
- configuración de SAP estándar;
- desarrollo Z/Y;
- enhancement;
- integración;
- comportamiento específico de la organización.

--------------------------------------------------
6. REGLA DE NO GENERALIZACIÓN
--------------------------------------------------

Nunca convertir:

comportamiento observado localmente

en:

comportamiento estándar SAP.

Ejemplo conceptual:

MIGO es estándar SAP.

Un comportamiento observado en MIGO dentro de PY44 no debe atribuirse automáticamente a SAP estándar.

Debe distinguirse:

SAP STANDARD
+
CONFIGURACIÓN LOCAL
+
CUSTOM
+
EVIDENCIA.

--------------------------------------------------
7. DOCUMENTOS MIXTOS
--------------------------------------------------

Definir explícitamente que un documento puede ser:

knowledge_type: mixed

cuando describa simultáneamente:

- funcionalidad SAP estándar;
- configuración local;
- desarrollos Z;
- integraciones;
- reglas propias.

--------------------------------------------------
8. COMPATIBILIDAD
--------------------------------------------------

La clasificación debe ser compatible con:

- requirement;
- functional-specification;
- functional-test;
- analysis;
- debug;
- investigation;
- ticket;
- SAP Object;
- Process;
- Business Rule;
- Relationship;
- Source.

No inventar nuevos tipos de documentos.

--------------------------------------------------
9. IA
--------------------------------------------------

El agente debe utilizar knowledge_type y knowledge_scope durante la recuperación.

Debe poder responder separando:

SAP STANDARD

de:

CUSTOM

y:

IMPLEMENTACIÓN LOCAL.

No mezclar ambos como una única fuente de verdad.

Mantener trazabilidad hacia las fuentes.

No inventar clasificaciones.

Entrega únicamente el contenido completo actualizado de:

standards/documentation-standard.md
