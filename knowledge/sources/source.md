==================================================
1. OBJETIVO
==================================================

Definir una entidad Source que permita responder:

¿De dónde proviene esta información?

Una Source puede respaldar:

- documentos;
- objetos;
- procesos;
- reglas;
- relaciones;
- análisis;
- conclusiones.

==================================================
2. METADATA
==================================================

Utilizar:

---
source_id: ""
source_type: ""
source_name: ""
origin: ""
knowledge_type: ""
knowledge_scope: ""
version: "1.0"
status: "active"
date: ""
author: ""
---

==================================================
3. SOURCE_ID
==================================================

Formato:

SRC-0001

Debe ser estable.

==================================================
4. SOURCE_TYPE
==================================================

Utilizar:

repository_file
sap_documentation
sap_system
configuration
abap_code
debug
ticket
analysis
investigation
functional_test
screenshot
log
query
external_documentation
other
unknown

==================================================
5. ORIGIN
==================================================

Utilizar:

internal
sap
external
system
unknown

==================================================
6. KNOWLEDGE_TYPE
==================================================

Utilizar:

standard
custom
mixed
unknown

==================================================
7. KNOWLEDGE_SCOPE
==================================================

Utilizar:

global
organization
country
company
plant
process
project
ticket
unknown

==================================================
8. RELIABILITY
==================================================

Utilizar:

authoritative
confirmed
supporting
contextual
unknown

==================================================
9. ESTRUCTURA
==================================================

Crear:

# Source

## Metadata

## 1. Identificación

## 2. Tipo de fuente

## 3. Origen

## 4. Ubicación / Referencia

## 5. Fecha

## 6. Versión

## 7. Información proporcionada

## 8. Elementos de conocimiento respaldados

## 9. Evidencia derivada

## 10. Nivel de confiabilidad

## 11. Alcance

## 12. Limitaciones

## 13. Documentación relacionada

## 14. Información pendiente de validar

==================================================
10. REGLAS
==================================================

Una fuente no representa automáticamente la verdad.

Evaluar:

SOURCE
+
CONTEXT
+
EVIDENCE
+
VALIDATION

No considerar automáticamente:

ticket = verdad SAP.

No considerar:

código aislado = explicación funcional completa.

No considerar:

captura = comportamiento general.

No inventar URLs.

No almacenar secretos.

==================================================
11. IA
==================================================

El agente debe poder recorrer:

KNOWLEDGE
→ SOURCE
→ EVIDENCE

y:

DOCUMENT
→ SOURCE
→ KNOWLEDGE

Debe poder explicar el origen de afirmaciones relevantes.

Entrega únicamente el contenido completo final.
