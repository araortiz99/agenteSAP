# MVP 5.5 — Operational Knowledge Consultant

## Objetivo

Convertir el Knowledge Consultant validado en MVP 5.4 en una interfaz operativa estable mediante CLI.

Flujo:

CLI → ROUTER → CONSULTANT → KNOWLEDGE INTELLIGENCE → EVIDENCE / TRACEABILITY → LLM → VALIDATED RESPONSE

## Capacidades

- consulta natural en español;
- ticket extraído desde la consulta o suministrado explícitamente;
- repository ref configurable;
- máximo de evidencia configurable;
- salida humana;
- salida JSON estructurada;
- plan de ejecución visible en JSON.

## Parámetros

```text
python -m src.agent.cli "<consulta>"
python -m src.agent.cli "<consulta>" --ticket 31426
python -m src.agent.cli "<consulta>" --ref feature/agent-mvp-search
python -m src.agent.cli "<consulta>" --max-results 12
python -m src.agent.cli "<consulta>" --json
```

`--ticket` sobrescribe el ticket detectado desde lenguaje natural.

`--max-results` debe ser mayor que cero.

## Contrato JSON

La salida JSON conserva request, plan.intent, plan.ticket_id, plan.capabilities y result. En consultas consultivas también conserva evidencia y traceability.

El JSON no reemplaza la respuesta consultiva; expone el mismo resultado estructurado para integración futura.

## Seguridad

5.5 continúa siendo read-only.

El CLI no ejecuta SAP, modifica SAP, modifica GitHub, escribe Knowledge automáticamente, altera provenance ni resuelve conflictos automáticamente.

## Gates

### CLI Gate
Una consulta válida llega al consultor correcto.

### Ticket Gate
Un ticket explícito prevalece sobre el ticket extraído.

### Parameter Gate
`--max-results <= 0` se rechaza.

### JSON Gate
La salida `--json` debe ser serializable y contener el plan.

### E2E Gate
Una consulta sobre 31426 conserva las garantías de MVP 5.4.

### Regression Gate
Toda la suite existente permanece verde.

## Caso canónico

`Consultá el ticket 31426: explicame qué está confirmado sobre ZMM_IMX_0004, SNC K1 y la discrepancia K1/K4.`

Debe conservar ZMM_IMX_0004, SNC K1, K1/K4, relaciones, partial/candidate, conflicto, TKT-*, EVD-*, Standard vs Custom e información no confirmada.

## Fuera de alcance

- memoria conversacional;
- sesiones persistentes;
- vector DB;
- embeddings;
- ejecución SAP;
- escritura automática;
- interfaz web;
- agente autónomo.

## Criterio de cierre

MVP 5.5 se cierra cuando los CLI Gates, E2E Gate y Regression Gate estén verdes.
