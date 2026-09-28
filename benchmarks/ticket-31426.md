# Benchmark funcional — Ticket 31426

## Objetivo

Validar el flujo completo del consultor SAP sobre un ticket real/sanitizado
incorporado a la Knowledge Base.

## Consulta canónica

> Consultá el ticket 31426 y explicame qué está confirmado, qué corresponde
> a nuestra implementación y qué información falta.

## Gate de aceptación

### Recuperación
- [x] Se identifica ticket_id 31426.
- [x] Se recupera tickets/31426/.
- [x] Se recuperan relaciones explícitas.
- [x] Se recuperan entidades relacionadas cuando forman parte del resultado.

### Evidencia
- [x] Las evidencias tienen IDs determinísticos EVD-*.
- [x] La certeza se conserva.
- [x] El ticket candidato no se convierte automáticamente en evidencia SAP Standard.
- [x] Las citas del LLM se validan contra la trazabilidad.

### Ticket
- [x] El contexto recibe referencias TKT-*.
- [x] Las relaciones del ticket se incorporan al contexto.
- [x] Las relaciones no se infieren por co-ocurrencia.

### Control de incertidumbre
- [x] No se afirma causa raíz sin evidencia.
- [x] No se afirma solución definitiva sin evidencia.
- [x] La discrepancia documental K1/K4 queda pendiente.
- [x] No se confunde el ticket histórico con comportamiento SAP Standard.

### CI
- [x] GitHub Actions: job `test` — success.
- [x] Último baseline: 72 tests pasaron antes del último ajuste del test.
- [x] El ajuste posterior valida pertenencia de citas al conjunto de trazabilidad.

## Resultado

El pipeline técnico del benchmark cumple el contrato de trazabilidad.

La validación de la **respuesta semántica de un LLM real** queda separada de
esta prueba determinística y requiere credenciales/runtime del proveedor.

## Criterio para MVP 4.2

No avanzar a MVP 4.2 únicamente por tener el pipeline verde. Primero se debe
ejecutar una consulta con un proveedor LLM real y revisar manualmente:

1. exactitud factual;
2. preservación de certainty;
3. uso correcto de EVD-*;
4. tratamiento de la discrepancia K1/K4;
5. separación Standard/Custom;
6. identificación explícita de información faltante.

Si esos seis puntos pasan, MVP 4.2 puede centrarse en la experiencia de
consulta del consultor SAP, sin introducir todavía memoria conversacional ni
RAG semántico.
