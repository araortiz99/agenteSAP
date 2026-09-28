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

### Gate semántico real
El benchmark ejecutable `benchmarks/mvp-4-2-semantic-gate.py` valida:

1. estructura obligatoria de la respuesta;
2. citas EVD-* pertenecientes a la trazabilidad;
3. tratamiento explícito del conflicto K1/K4;
4. preservación de `certainty`;
5. separación SAP Standard vs implementación interna/custom;
6. explicitación de información faltante;
7. referencia TKT-*.

Además ejecuta cuatro casos negativos sintéticos que **deben ser rechazados**:

- `partial_as_confirmed`: presenta evidencia `partial` como confirmada.
- `conflict_omitted`: omite la discrepancia K1/K4.
- `unknown_evidence`: introduce un EVD-* inexistente.
- `standard_custom_mixed`: presenta un objeto/proceso custom como SAP Standard.

Los casos negativos no modifican la evidencia real; son mutaciones en memoria del
`ConsultationResult` para probar el comportamiento del Gate.

### Estabilidad
La ejecución canónica acepta el parámetro `--runs N` para repetir la consulta
real con el proveedor LLM configurado. El criterio de estabilidad es:

- todas las ejecuciones deben pasar los checks semánticos;
- los cuatro negativos deben continuar siendo rechazados.

Ejemplo:

```powershell
$env:PYTHONPATH="."
.\.venv\Scripts\python.exe benchmarks\mvp-4-2-semantic-gate.py --runs 3
```

## Baseline semántico esperado

La respuesta canónica debe mantener:

- `Reasoning status: conflict`;
- discrepancia K1/K4 como no resuelta;
- evidencia parcial como parcial;
- separación de SAP Standard e implementación interna/custom;
- información faltante explícita;
- referencias EVD-* válidas;
- referencia TKT-*.

La redacción exacta del LLM **no es el resultado esperado**. El benchmark valida
propiedades semánticas y de trazabilidad, no una respuesta textual exacta.

## Resultado

El pipeline técnico y el Gate semántico deben considerarse aprobados solamente
cuando:

1. la consulta canónica pasa todos los checks en las ejecuciones solicitadas;
2. los cuatro casos negativos son rechazados por el check correspondiente;
3. no se altera la procedencia ni la certeza de la evidencia para conseguir el PASS.

## Criterio para MVP 5

No avanzar a MVP 5 por una única respuesta correcta. Primero debe existir:

- un baseline semántico persistido;
- casos negativos reproducibles;
- evidencia de estabilidad en múltiples ejecuciones;
- separación entre validación determinística y comportamiento probabilístico del LLM.

El siguiente MVP puede entonces centrarse en nuevas capacidades sobre este contrato
ya validado, sin reinterpretar la evidencia existente.
