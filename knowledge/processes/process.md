
==================================================
1. OBJETIVO
==================================================

Documentar procesos funcionales SAP como secuencias reutilizables.

Un proceso debe representar:

inicio
→ actividades
→ decisiones
→ validaciones
→ resultado.

==================================================
2. METADATA
==================================================

Utilizar:

---
process_id: ""
process_name: ""
process_type: ""
module: ""
knowledge_type: ""
knowledge_scope: ""
version: "1.0"
status: "draft"
date: ""
author: ""
---

==================================================
3. PROCESS_ID
==================================================

Formato:

PROC-0001

Debe ser estable.

==================================================
4. PROCESS_TYPE
==================================================

Utilizar:

standard
configured
custom
mixed
unknown

Explicar cada uno.

==================================================
5. KNOWLEDGE_TYPE
==================================================

Utilizar:

standard
custom
mixed
unknown

Distinguirlo de process_type.

==================================================
6. KNOWLEDGE_SCOPE
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
7. ESTRUCTURA
==================================================

Crear:

# Process

## Metadata

## 1. Identificación

## 2. Objetivo

## 3. Alcance

## 4. Inicio y fin del proceso

## 5. Actores

## 6. Precondiciones

## 7. Flujo del proceso

## 8. Decisiones y validaciones

## 9. Documentos SAP

## 10. Objetos SAP relacionados

## 11. Reglas de negocio

## 12. Datos y objetos de información

## 13. Integraciones

## 14. Estados del proceso

## 15. Excepciones

## 16. Controles

## 17. Resultados

## 18. Evidencias

## 19. Fuentes

## 20. Relaciones

## 21. Información pendiente

## 22. Documentación relacionada

==================================================
8. STANDARD VS CUSTOM
==================================================

Explicar explícitamente:

Un proceso puede ser mixed.

Ejemplo conceptual:

SAP Standard
+
Configuración
+
Z Development
+
Integración.

No clasificar todo el proceso como custom únicamente porque contiene un desarrollo Z.

==================================================
9. RELACIÓN CON OBJECTS
==================================================

Referenciar object_id.

No copiar toda la documentación del objeto.

==================================================
10. IA
==================================================

El agente debe poder separar:

SAP Standard
Configuración
Custom
Integración
Reglas locales
Información no confirmada

==================================================
11. DUPLICACIÓN
==================================================

Buscar procesos existentes antes de crear uno nuevo.

No crear dos procesos para la misma secuencia funcional.
