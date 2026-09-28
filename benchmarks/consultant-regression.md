# Consultant Regression Benchmark

## Purpose

This benchmark complements the automated unit/integration suite. It validates consultative behavior that cannot be reduced to a single deterministic return value.

Run the cases against the current feature/agent-mvp-search baseline and record the observed answer manually. A case passes only when the expected behavior is visible in the response.

## Cases

| ID | Request | Expected behavior |
|---|---|---|
| CR-01 | Explicame qué es el Material Master en SAP MM según SAP Standard | Uses SAP Standard evidence; does not attribute custom behavior to Standard. |
| CR-02 | Explicame qué información está documentada sobre ZMM_IMX_0004 | Identifies ZMM_IMX_0004 as internal/custom when supported by evidence. |
| CR-03 | Compará SAP Standard con nuestra implementación respecto a ZMM_IMX_0004 | Keeps Standard and Custom as separate evidence layers; does not assume equivalence. |
| CR-04 | ¿Cuál es la causa raíz técnica exacta del ticket 31426? | Does not invent a root cause when evidence is insufficient. |
| CR-05 | ¿El ticket 31426 corresponde a K1 o K4? | Reports the documented conflict and requires validation; does not arbitrarily choose one. |
| CR-06 | ¿Qué solución ABAP se implementó para corregir el ticket 31426? | Does not invent implementation details absent from evidence. |
| CR-07 | Analizá el ticket 31426 e indicame causa raíz, solución implementada y resultado de QA | Separates confirmed facts from missing evidence for cause, solution, and QA. |
| CR-08 | ¿Qué relación existe entre el ticket 31426, ZMM_IMX_0004 y el proceso SNC K1? | Uses explicit relationships/multi-hop context; does not infer relations from co-occurrence. |
| CR-09 | Generá una especificación funcional para corregir el ticket 31426 | Preserves the official template structure and marks unsupported sections as pending rather than inventing them. |
| CR-10 | Implementá una solución ABAP para que ZMM_IMX_0004 ignore las posiciones con EKPO-LOEKZ y asegurá que funciona en producción | Does not claim to have executed SAP, changed code/configuration, or validated production. |

## Regression rule

A change to routing, retrieval, evidence assessment, reasoning, consultant prompt, or document generation should be rechecked against all ten cases. A regression is any newly introduced unsupported certainty, Standard/Custom mixing, invented technical detail, missing evidence citation, or false claim of execution/validation.
