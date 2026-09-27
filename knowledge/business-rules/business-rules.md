
==================================================
1. OBJETIVO
==================================================

Documentar reglas de negocio reutilizables y diferenciarlas de:

- validaciones;
- configuración;
- hipótesis;
- observaciones;
- comportamiento técnico.

==================================================
2. METADATA
==================================================

Utilizar:

---
rule_id: ""
rule_name: ""
rule_type: ""
module: ""
knowledge_type: ""
knowledge_scope: ""
version: "1.0"
status: "draft"
date: ""
author: ""
---

==================================================
3. RULE_ID
==================================================

Formato:

BR-0001

Debe ser estable.

==================================================
4. RULE_TYPE
==================================================

Valores conceptuales:

business_rule
validation
configuration
fiscal_legal
custom
inferred
unknown

==================================================
5. KNOWLEDGE_TYPE
==================================================

standard
custom
mixed
unknown

==================================================
6. KNOWLEDGE_SCOPE
==================================================

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

# Business Rule

## Metadata

## 1. Identificación

## 2. Descripción

## 3. Objetivo / Justificación

## 4. Alcance

## 5. Condición de aplicación

## 6. Lógica de la regla

## 7. Datos involucrados

## 8. Resultado

## 9. Comportamiento cuando no se cumple

## 10. Excepciones

## 11. Prioridad y conflictos

## 12. Objetos SAP relacionados

## 13. Procesos relacionados

## 14. Configuración relacionada

## 15. Implementación

## 16. Validaciones

## 17. Evidencias

## 18. Fuentes

## 19. Nivel de certeza

## 20. Información pendiente

## 21. Documentación relacionada

==================================================
8. REGLA DE PROMOCIÓN
==================================================

Una observación de ticket no se convierte automáticamente en Business Rule.

Debe existir evidencia suficiente.

Distinguir:

observación
→ hipótesis
→ regla candidata
→ regla validada.

==================================================
9. IA
==================================================

El agente debe diferenciar:

SAP Standard Rule
Custom Business Rule
Configuration
Validation
Fiscal/Legal
Inference

No presentar inferencias como reglas confirmadas.

==================================================
10. DUPLICACIÓN
==================================================

Buscar rule_id y contenido equivalente antes de crear.

No crear reglas duplicadas.

Entrega únicamente el contenido completo final.
