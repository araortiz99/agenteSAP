Actúa como arquitecto de información y especialista en recuperación de conocimiento para agentes de IA.


==================================================
1. OBJETIVO
==================================================

Este archivo será el índice maestro de tickets.

No contiene el detalle completo de los tickets.

Su función es:

DISCOVERY
+
NAVIGATION
+
INDEXACIÓN.

==================================================
2. METADATA
==================================================

---
document_type: "ticket-index"
version: "1.0"
status: "active"
date: ""
author: ""
---

==================================================
3. CATÁLOGO
==================================================

Crear una tabla:

| Ticket ID | Título | Tipo | Módulo | Prioridad | Estado | Knowledge Type | Knowledge Scope | Fecha apertura | Fecha actualización | Ticket |

No inventar tickets.

==================================================
4. ORGANIZACIÓN
==================================================

Crear secciones para navegación:

## Todos los tickets

## Por tipo

## Por módulo

## Por estado

## Por Knowledge Type

## Por Knowledge Scope

## Documentación asociada

## Knowledge descubierto

==================================================
5. REGLA
==================================================

El índice no contiene:

- análisis;
- debug;
- reglas;
- objetos;
- soluciones completas.

Solo referencias.

==================================================
6. NAVEGACIÓN
==================================================

Cuando exista:

tickets/<ticket_id>/ticket.md

utilizar esa ruta.

==================================================
7. IA
==================================================

El agente puede utilizar el índice para:

- localizar tickets;
- identificar contexto;
- encontrar documentación relacionada;
- descubrir Knowledge candidato.

Luego debe abrir el ticket correspondiente.

==================================================
8. DUPLICADOS
==================================================

Cada ticket_id debe aparecer una sola vez.

No crear entradas separadas para:

- requirement;
- analysis;
- debug;
- investigation;
- functional specification;
- tests.

Todos pertenecen al mismo ticket.

Entrega únicamente el contenido completo final
