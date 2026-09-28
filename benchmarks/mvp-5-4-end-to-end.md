# MVP 5.4 — End-to-End Knowledge Consultant

## Objetivo

Validar el flujo completo:

QUERY → ENTITY RESOLUTION → RELATIONSHIPS → MULTI-HOP → KNOWLEDGE CONTEXT → EVIDENCE → LLM → VALIDATED RESPONSE

El caso canónico es el ticket 31426.

## Caso canónico 31426

La representación disponible documenta:

- ticket 31426;
- ZMM_IMX_0004 como objeto relacionado;
- proceso de generación XML SNC K1;
- EKPO-LOEKZ como dato relevante;
- relación ticket → objeto con certainty confirmed;
- relación ticket → proceso con certainty partial y status candidate;
- fuente interna consolidada como evidence de apoyo;
- discrepancia documentada porque la misma fuente también utiliza 31426 para un escenario K4;
- causa raíz, solución definitiva y evidencia QA como información pendiente.

## Invariantes E2E

- **E2E-01 Entity:** ZMM_IMX_0004 debe resolverse como SAP_OBJECT.
- **E2E-02 Ticket:** debe existir contexto TKT-* para 31426.
- **E2E-03 Relationship:** debe recuperarse 31426 → ZMM_IMX_0004.
- **E2E-04 Partial preservation:** 31426 → PROC-0001 conserva partial/candidate.
- **E2E-05 Conflict preservation:** K1/K4 se conserva como conflicto pendiente de análisis.
- **E2E-06 Standard/Custom:** ZMM_IMX_0004 no puede presentarse como SAP Standard.
- **E2E-07 Missing information:** no se afirma como confirmado causa raíz, solución definitiva ni QA.
- **E2E-08 Citation integrity:** toda cita EVD-* debe existir en TraceabilityReport.
- **E2E-09 Ticket integrity:** con ticket context, la respuesta debe incluir TKT-*.
- **E2E-10 Structure:** la respuesta respeta el contrato de MVP 4.2.
- **E2E-11 Read-only:** no se declara ejecución SAP ni modificación del repositorio.

## Negative cases

1. EVD inexistente → rechazo.
2. TKT-* omitido → rechazo.
3. Sección obligatoria omitida → rechazo.
4. ZMM_IMX_0004 atribuido a SAP Standard → rechazo semántico.
5. partial/candidate convertido a confirmed → rechazo semántico.
6. conflicto K1/K4 omitido → rechazo semántico.

## Criterio de cierre

Todos los invariantes E2E y negativos deben pasar y la suite completa de regresión debe permanecer verde.

El benchmark no requiere una llamada real al proveedor LLM para validar el contrato. La llamada real permanece cubierta por el semantic gate de MVP 4.2; 5.4 valida que el contexto enriquecido llega al LLM y que su salida sigue sometida a los mismos gates.
