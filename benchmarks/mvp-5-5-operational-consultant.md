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


## Performance hardening — 5.5

La primera ejecución E2E real del caso 31426 mostró que el flujo funcional es correcto, pero el tiempo de respuesta puede ser elevado por múltiples lecturas repetidas del repositorio GitHub.

Se incorpora una optimización de transporte sin alterar la semántica del agente:

- caché en memoria por `ref + path` durante una ejecución;
- caché del árbol por `ref`;
- lectura concurrente acotada de archivos del repositorio;
- deduplicación de paths antes de solicitar contenido;
- sin memoria persistente ni cambios en provenance.

La optimización fue validada nuevamente sobre el caso canónico 31426. El tiempo observado por ejecución local bajó de aproximadamente 5 minutos a aproximadamente 20 segundos, sin cambios funcionales en la respuesta.


## Resultado de performance

Caso: ticket 31426, consulta canónica.

- baseline observado: ~5 minutos;
- resultado después del hardening: ~20 segundos;
- reducción observada: aproximadamente 93 % del tiempo total;
- validación funcional: respuesta conservó TKT-*, EVD-*, partial/candidate, conflicto K1/K4 y separación Standard/Custom.

La medición corresponde a una ejecución local y no constituye un SLA productivo.

## Estado de cierre

**CLOSED / APPROVED** — 5.5 queda cerrado funcional y operacionalmente.
