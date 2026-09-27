Este archivo será la plantilla maestra para documentar cualquier SAP Object.

==================================================
1. OBJETIVO
==================================================

Documentar objetos SAP de forma:

- estructurada;
- reutilizable;
- trazable;
- diferenciando SAP Standard de Custom;
- utilizable por agentes de IA.

==================================================
2. METADATA
==================================================

Utilizar:

---
object_id: ""
object_type: ""
object_name: ""
technical_name: ""
module: ""
origin: ""
implementation_type: ""
knowledge_type: ""
knowledge_scope: ""
version: "1.0"
status: "draft"
date: ""
author: ""
---

==================================================
3. IDENTIFICADOR
==================================================

Utilizar:

OBJ-0001
OBJ-0002
...

El object_id debe ser estable.

No cambiarlo cuando el objeto sea actualizado.

==================================================
4. ORIGIN
==================================================

Valores:

standard
custom
unknown

Definir:

standard = proporcionado por SAP.

custom = desarrollado específicamente por la organización.

unknown = no confirmado.

==================================================
5. IMPLEMENTATION_TYPE
==================================================

Valores:

standard
configuration
enhancement
z_development
integration
unknown

Explicar cada valor.

==================================================
6. DIFERENCIA
==================================================

Explicar:

origin

responde:

"¿De dónde proviene el objeto?"

implementation_type

responde:

"¿Cómo está implementado o qué tipo de implementación representa?"

Ejemplo conceptual:

origin: standard
implementation_type: configuration

Es válido.

==================================================
7. KNOWLEDGE_TYPE
==================================================

Valores:

standard
custom
mixed
unknown

Aclarar que:

knowledge_type

clasifica el conocimiento documentado sobre el objeto.

No necesariamente debe coincidir con:

origin.

Un objeto estándar puede tener documentación sobre una implementación local.

==================================================
8. KNOWLEDGE_SCOPE
==================================================

Valores:

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
9. ESTRUCTURA
==================================================

Crear:

# SAP Object

## Metadata

## 1. Identificación

## 2. Tipo de objeto

## 3. Descripción

## 4. Propósito

## 5. Comportamiento

## 6. Datos involucrados

## 7. Relaciones con otros objetos

## 8. Procesos relacionados

## 9. Módulo SAP

## 10. Clasificación Standard / Custom

## 11. Configuración relacionada

## 12. Integraciones

## 13. Uso funcional

## 14. Uso técnico

## 15. Reglas de negocio relacionadas

## 16. Evidencias

## 17. Fuentes

## 18. Estado del conocimiento

## 19. Información pendiente

## 20. Documentación relacionada

==================================================
10. REGLAS
==================================================

No inventar objetos.

No inventar nombres técnicos.

No asumir Standard por uso.

No asumir Custom solamente por prefijo.

Z/Y puede ser indicio, no prueba absoluta.

No confundir configuración con desarrollo.

No confundir objeto Standard con proceso Standard.

==================================================
11. IA
==================================================

El agente debe poder determinar:

- qué objeto es;
- qué tipo tiene;
- si es Standard o Custom;
- cómo está implementado;
- dónde aplica;
- qué procesos utiliza;
- qué reglas aplica;
- qué objetos relacionados existen;
- qué evidencia respalda la información.

==================================================
12. DUPLICADOS
==================================================

Antes de crear un objeto:

buscar por:

- technical_name;
- object_name;
- object_id.

No crear duplicados.
