---
process_id: "PROC-0001"
process_name: "Generación XML SNC K1"
process_type: "custom"
module: "MM"
knowledge_type: "custom"
knowledge_scope: "process"
version: "1.0"
status: "candidate"
date: "2026-09-27"
author: "agenteSAP"
---

# Process

## 1. Identificación
PROC-0001 — Generación XML SNC K1

## 2. Objetivo
Representar únicamente el flujo documentado por la fuente para el contexto del ticket 31426.

## 3. Alcance
Generación de XML SNC K1 cuando existen posiciones de pedido marcadas para borrado.

## 4. Flujo documentado
1. Existen posiciones del pedido.
2. Se genera XML SNC K1.
3. Debe controlarse EKPO-LOEKZ antes de la generación.

## 5. Decisiones y validaciones
La fuente registra la necesidad de excluir/gestionar correctamente posiciones marcadas para borrado.

## 6. Objetos relacionados
- OBJ-0001 — ZMM_IMX_0004
- EKPO-LOEKZ

## 7. Evidencias y fuentes
- SRC-31426-KB-20260918

## 8. Estado
candidate / partial.

## 9. Información pendiente
- flujo completo;
- punto exacto de generación;
- lógica ABAP;
- estructura XML;
- comportamiento esperado por posición;
- resultado QA.
