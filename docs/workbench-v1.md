# AgenteSAP Workbench v1

The local web application is a presentation layer over the existing read-only agent.

## Available now

- natural-language consultation;
- optional ticket/incident ID;
- local browser history using `localStorage`;
- plan visibility;
- evidence citation IDs;
- uncited supporting evidence IDs;
- responsive layout for desktop and mobile browsers.

## Data boundary

Browser history is stored only in the local browser profile. It is not written to GitHub or SAP.

The server receives the request and optional ticket ID, then delegates to `run_agent()`.

No SAP write endpoint is exposed.

## Suggested workflow

1. Start with a broad functional question.
2. Add a ticket number when investigating an incident.
3. Inspect the answer and citation IDs.
4. Expand "Plan y trazabilidad" when you need to understand what the agent used.
5. Use the CLI or future document views for formal deliverables.

## Next UI increments

- dedicated Ticket workspace;
- evidence cards with source layer and certainty;
- Standard vs Internal/Custom comparison view;
- relationship graph;
- document generation actions;
- QAS runtime status/readiness panel;
- optional server-side authenticated persistence.


## Ticket workspace action

The **Analizar ticket** action pre-fills a structured investigation request. It does not invent ticket facts; the agent still relies on retrieved evidence and reports gaps.

The intended analysis sections are:

- hechos confirmados;
- evidencia disponible;
- hipótesis;
- gaps de información;
- objetos SAP relacionados;
- próximos pasos.
