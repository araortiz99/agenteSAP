---
ticket_id: "31426"
ticket_type: "INCIDENT"
title: "Error de XML SNC K1 con posiciones de pedido marcadas para borrado"
module: "MM"
priority: "High"
status: "candidate"
knowledge_type: "custom"
knowledge_scope: "ticket"
version: "1.0"
date_opened: "2026-08-20"
date_updated: "2026-09-27"
date_closed: ""
author: "agenteSAP"
---

# Ticket

## 1. Identificación del caso
- Ticket: 31426
- Módulo: MM
- Objeto: ZMM_IMX_0004
- Escenario: SNC K1
- Campo relevante: EKPO-LOEKZ
- Estado de esta representación: candidate

## 2. Resumen
La fuente interna consultada registra un error en la generación del XML de SNC K1 cuando existen posiciones del pedido marcadas para borrado.

## 3. Problema / Necesidad
Controlar el tratamiento de posiciones de pedido marcadas para borrado antes de la generación del XML K1.

## 4. Alcance
- ZMM_IMX_0004
- generación XML SNC K1
- posiciones de pedido con EKPO-LOEKZ

No se agrega comportamiento técnico no documentado por la fuente.

## 5. Impacto
No cuantificado en la fuente utilizada.

## 6. Documentación del ticket
Esta instancia fue construida desde una fuente interna consolidada, no desde la ficha original del sistema de tickets.

## 7. Knowledge relacionado
- OBJ-0001 — ZMM_IMX_0004
- PROC-0001 — Generación XML SNC K1
- SRC-31426-KB-20260918

## 8. Objetos descubiertos
- ZMM_IMX_0004
- EKPO-LOEKZ

## 9. Procesos descubiertos
- Generación XML SNC K1

## 10. Reglas descubiertas
La fuente registra la necesidad de controlar EKPO-LOEKZ y excluir/gestionar correctamente las posiciones marcadas para borrado antes de generar XML K1.

## 11. Relaciones descubiertas
- REL-31426-001
- REL-31426-002

## 12. Evidencias
- EVD-T31426-001: la fuente registra el error de XML SNC K1 con posiciones marcadas para borrado. certainty: partial.
- EVD-T31426-002: EKPO-LOEKZ es el campo relevante. certainty: partial.
- EVD-T31426-003: existe una regla documentada para controlar EKPO-LOEKZ antes del XML K1. certainty: partial.

## 13. Cronología
- 2026-08-20: fecha previamente registrada para el incidente.
- 2026-09-27: creación de esta representación candidata.

## 14. Conclusión
La evidencia disponible permite documentar como contexto candidato la asociación de 31426 con ZMM_IMX_0004 y XML SNC K1 relacionado con posiciones marcadas para borrado.

No permite afirmar causa raíz ni solución definitiva.

## 15. Solución / Acción realizada
No documentada en la fuente utilizada.

## 16. Resultado de validación
Pendiente de validar contra el ticket original y evidencia QA.

## 17. Información pendiente
- registro original del ticket;
- causa raíz técnica;
- solución implementada;
- evidencia QA;
- resultado de prueba;
- estado real de cierre;
- relación con transportes;
- aclaración de la discrepancia documental que también utiliza 31426 para un escenario K4.

## 18. Documentación relacionada
- knowledge/sources/src-31426-kb-20260918.md
- knowledge/sap-objects/zmm-imx-0004.md
- knowledge/processes/snc-k1-xml-generation.md
