# MVP 6 — Knowledge Governance & Controlled Persistence

## Objetivo

Agregar una frontera explícita entre el agente consultivo read-only y la persistencia controlada de Knowledge.

Flujo:

CONSULT
  ↓
PROPOSE
  ↓
CLASSIFY
  ↓
SECURITY / VERSION / DUPLICATE GATES
  ↓
CHANGE BRANCH
  ↓
COMMIT
  ↓
PULL REQUEST
  ↓
HUMAN REVIEW
  ↓
MERGE
  ↓
REUSABLE KNOWLEDGE

## Principios

- El agente nunca modifica SAP.
- El agente nunca escribe directamente en main.
- El agente no hace merge.
- El agente no se autoaprueba.
- La publicación está limitada inicialmente a knowledge/.
- Tickets y estándares quedan fuera de la escritura automatizada.
- Provenance y certainty no pueden degradarse ni alterarse silenciosamente.
- Un PR no equivale a aprobación funcional.

## Capabilities

- validar una propuesta de Knowledge;
- detectar secretos conocidos;
- validar metadata;
- comparar versión propuesta contra versión existente;
- impedir paths fuera de knowledge/;
- crear branch;
- persistir un único archivo Markdown;
- crear Pull Request;
- ejecutar dry-run sin escribir.

## Gates

### Scope Gate
Solo knowledge/**/*.md es publicable.

### Metadata Gate
Metadata obligatoria y valores controlados.

### Security Gate
Bloquea patrones conocidos de secretos.

### Version Gate
Una actualización requiere una versión lógica superior.

### Branch Gate
La rama de cambio debe ser diferente de la base y no puede ser main/master.

### Duplicate Gate
Una creación no puede apuntar a un path existente.

### PR Gate
Toda escritura genera Pull Request y nunca merge automático.

### Human Review Gate
approved/validated no pueden ser declarados por el agente sin evidencia explícita.

### Read-only SAP Gate
No existe capability de escritura SAP.

## Caso canónico

Proponer Knowledge relacionado con ticket 31426, por ejemplo:
knowledge/sap-objects/zmm-imx-0004.md

El flujo debe rechazar una escritura directa en main y permitir un dry-run de la propuesta.

## Negativos

- path standards/...;
- path tickets/...;
- branch main;
- branch igual a base;
- metadata incompleta;
- versión nueva <= existente;
- secreto detectado;
- creación sobre path existente;
- merge automático.

## Criterio de cierre

- unit tests verdes;
- gates negativos cubiertos;
- dry-run funcional;
- writer separado del cliente read-only;
- PR creado solamente bajo --publish;
- ningún merge automático;
- documentación del lifecycle completa.
