# Knowledge Graph — SAP Help Extension

## Entidades

La extracción es conservadora. Sólo se crean entidades cuando el documento proporciona evidencia suficiente.

Tipos iniciales:

- transaction;
- table;
- CDS view;
- BAdI;
- enhancement;
- class;
- function module;
- API;
- Fiori app;
- business object;
- movement type;
- document type;
- configuration object;
- authorization object;
- process;
- module;
- product;
- component.

## Relaciones

Cada relación requiere:

- source;
- target;
- predicate;
- evidence;
- confidence;
- provenance.

Ejemplos:

- SAP Help document → documents → Movement Type;
- SAP Help document → explains → Inventory Management;
- SAP Help document → references → MIGO.

La coocurrencia de términos no crea una relación.

## Standard ↔ Internal

Una relación entre una entidad SAP_STANDARD y una entidad INTERNAL representa una comparación o vínculo documentado, no equivalencia.

Ejemplo:

`SAP_HELP(Movement Type 551) --standard_behavior--> STANDARD_ENTITY`

`ZMM_IM_0002 --uses--> Movement Type 551`

La conclusión de que ambos comportamientos son equivalentes requiere análisis funcional.
