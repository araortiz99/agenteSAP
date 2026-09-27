==================================================
1. OBJETIVO
==================================================

Documentar relaciones explícitas entre entidades del Knowledge Base.

Modelo:

SOURCE
→ RELATION
→ TARGET

==================================================
2. METADATA
==================================================

Utilizar:

---
relationship_id: ""
source_id: ""
source_type: ""
relation_type: ""
target_id: ""
target_type: ""
knowledge_type: ""
knowledge_scope: ""
version: "1.0"
status: "draft"
date: ""
author: ""
---

==================================================
3. RELATIONSHIP_ID
==================================================

Formato:

REL-0001

Debe ser estable.

==================================================
4. ENTIDADES
==================================================

Entidades principales:

TICKET
DOCUMENT
SAP_OBJECT
PROCESS
BUSINESS_RULE
RELATIONSHIP
SOURCE

No introducir todavía SYSTEM o ACTOR como entidades principales.

==================================================
5. RELATION TYPES
==================================================

Utilizar el vocabulario existente:

contiene
forma_parte_de
subproceso_de
depende_de
requiere
ejecuta
llama
lee
consulta
actualiza
genera
transforma
alimenta
consume
participa_en
utiliza
aplica
determina
valida
afecta
bloquea
autoriza
precede
sucede_a
integra_con
implementa
implementada_mediante
documenta
evidencia
relacionado_con
deriva_de
reemplaza

==================================================
6. KNOWLEDGE_TYPE
==================================================

standard
custom
mixed
unknown

La clasificación describe la relación documentada, no necesariamente los objetos.

==================================================
7. KNOWLEDGE_SCOPE
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
8. ESTRUCTURA
==================================================

Crear:

# Relationship

## Metadata

## 1. Elemento origen

## 2. Tipo de relación

## 3. Elemento destino

## 4. Descripción

## 5. Dirección

## 6. Condición de aplicación

## 7. Momento del proceso

## 8. Evidencia

## 9. Fuente

## 10. Nivel de certeza

## 11. Alcance

## 12. Vigencia

## 13. Impacto

## 14. Relaciones inversas

## 15. Conflictos o contradicciones

## 16. Información pendiente

## 17. Documentación relacionada

==================================================
9. REGLA FUNDAMENTAL
==================================================

No crear relaciones por co-ocurrencia.

Que dos objetos aparezcan juntos en:

- un ticket;
- un documento;
- una consulta;

no significa automáticamente que exista una relación.

Debe existir evidencia.

==================================================
10. IA
==================================================

El agente puede utilizar relaciones para recorrer el Knowledge Base.

Debe poder navegar:

objeto
→ proceso
→ regla
→ objeto

o:

ticket
→ documento
→ objeto
→ proceso.

No crear automáticamente relaciones inversas cuando no tengan significado semántico.

Entrega únicamente el contenido completo final.
