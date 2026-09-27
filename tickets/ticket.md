

Este archivo será la plantilla maestra para representar un ticket.

==================================================
1. OBJETIVO
==================================================

Un ticket representa:

- contexto;
- problema;
- necesidad;
- historial;
- evidencia;
- decisiones;
- resultado.

Un ticket NO es la única fuente de verdad del Knowledge Base.

==================================================
2. METADATA
==================================================

---
ticket_id: ""
ticket_type: ""
title: ""
module: ""
priority: ""
status: ""
knowledge_type: ""
knowledge_scope: ""
version: "1.0"
date_opened: ""
date_updated: ""
date_closed: ""
author: ""
---

==================================================
3. TICKET_TYPE
==================================================

Valores:

INCIDENT
REQUIREMENT
IMPROVEMENT
CONSULTATION
PROBLEM
CHANGE
INVESTIGATION
OTHER

==================================================
4. KNOWLEDGE_TYPE
==================================================

standard
custom
mixed
unknown

==================================================
5. KNOWLEDGE_SCOPE
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
6. ESTRUCTURA
==================================================

# Ticket

## Metadata

## 1. Identificación del caso

## 2. Resumen

## 3. Antecedente

## 4. Problema / Necesidad

## 5. Alcance

## 6. Impacto

## 7. Documentación del ticket

## 8. Knowledge relacionado

## 9. Objetos descubiertos

## 10. Procesos descubiertos

## 11. Reglas descubiertas

## 12. Relaciones descubiertas

## 13. Fuentes

## 14. Evidencias

## 15. Cronología

## 16. Decisiones

## 17. Conclusión

## 18. Solución / Acción realizada

## 19. Resultado de validación

## 20. Información pendiente

## 21. Documentación relacionada

==================================================
7. DISCOVERED KNOWLEDGE
==================================================

Permitir referencias mediante:

object_id
process_id
rule_id
relationship_id
source_id

No duplicar el contenido de las entidades.

==================================================
8. PROMOCIÓN
==================================================

Un ticket puede descubrir Knowledge.

Pero:

ticket

NO significa:

Knowledge confirmado.

Distinguir:

observación
hipótesis
candidato
confirmado.

==================================================
9. IA
==================================================

El agente debe poder navegar:

ticket
→ documentos
→ objetos
→ procesos
→ reglas
→ relaciones
→ fuentes
→ evidencias.

==================================================
10. REGLA
==================================================

No utilizar ticket histórico como evidencia automática de comportamiento SAP Standard.

No generalizar un incidente aislado.

Entrega únicamente el contenido completo final.
