# agenteSAP

Agente consultivo para conocimiento y documentación funcional SAP.

## Estado actual

**Baseline funcional avanzada — `main`.**

El agente es read-only respecto de SAP y, por defecto, el consultor no persiste
cambios en Knowledge. La persistencia controlada existe como una capability separada
de Governance y requiere una acción explícita de publicación.

La arquitectura actual es:

```
Usuario
  ↓
CLI / Agent Router
  ↓
Intent Routing determinístico
  ↓
Retrieval
  ├── SAP Standard
  ├── Internal / Custom
  └── Optional MCP evidence
       ├── sap-devs (developer context)
       ├── sap-mcp-server (runtime, disabled)
       └── ABAP MCP (custom runtime, disabled)
  ↓
Evidence Assessment
  ↓
Bounded Reasoning
  ↓
Evidence Traceability
  ↓
Knowledge Intelligence
  ├── Entity Resolution
  ├── Explicit Relationships
  └── bounded multi-hop context
  ↓
LLM Consultant
  ↓
Semantic / structural gates
  ↓
Respuesta trazable
```

## Capabilities

| Capability | Estado |
|---|---|
| `search_knowledge` | ✅ |
| `search_sap_standard` | ✅ |
| `search_unified` | ✅ |
| `get_ticket` | ✅ |
| `get_related_knowledge` | ✅ |
| `analyze` | ✅ |
| `generate_document` | ✅ |
| Evidence assessment | ✅ |
| Evidence traceability | ✅ |
| LLM consultant | ✅ |
| Entity / relationship resolution | ✅ |
| Bounded multi-hop context | ✅ |
| Knowledge governance / PR flow | ✅ |
| Read-only MCP evidence gateway | ✅ (opt-in) |
| QAS runtime contract / discovery | ✅ (disabled by default) |
| Live SAP QAS runtime validation | ⏳ |

## Reglas de seguridad funcional

- SAP Standard e implementación interna son capas de evidencia distintas.
- La coocurrencia no crea relaciones.
- Retrieval no equivale a conclusión.
- Hop no equivale a certainty.
- El LLM no puede elevar certainty ni inventar evidencia.
- El agente no realiza escrituras ni operaciones mutantes en SAP; las lecturas runtime sólo pueden ejecutarse de forma explícita, read-only, sobre QAS y mediante una allowlist validada.
- MCP es opt-in, read-only y utiliza una allowlist explícita de herramientas.
- `sap-devs` se trata como contexto externo/developer context; por sí solo no puede establecer una conclusión interna como confirmada.
- Los proveedores MCP de runtime permanecen deshabilitados hasta validar explícitamente su conexión y contrato de evidencia.
- El agente no afirma haber cambiado SAP, configuración, código o GitHub si no existe
  evidencia de esa acción.
- La publicación de Knowledge es explícita y separada del consultor read-only.

## Knowledge model

```
knowledge/
├── sap-standard/       # SAP Standard reutilizable
├── relationships/      # Relaciones explícitas
├── sap-objects/        # Objetos SAP / Z
└── ...
tickets/                # contexto histórico sanitizado
templates/              # contratos documentales
standards/              # reglas normativas
agent/                  # contratos y documentación del agente
```

## SAP Standard Knowledge

La capa SAP Standard está restringida a documentación oficial curada y mantiene
metadata de fuente, release, clasificación y checksum cuando corresponde.

La ingestión controlada puede dejar contenido como `candidate / under_validation`
antes de su promoción explícita a Knowledge reutilizable.

## CLI

Instalación y ejecución local:

```powershell
git clone https://github.com/araortiz99/agenteSAP.git
cd agenteSAP
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:GITHUB_REF = "main"
```

Consulta determinística:

```powershell
python -m src.agent.cli "Buscá SAP Standard sobre material master" --ref $env:GITHUB_REF
```

Consulta consultiva con LLM:

```powershell
$env:OPENAI_API_KEY = "..."
$env:OPENAI_MODEL = "gpt-5.6"
python -m src.agent.cli "Consultá sobre material master" --ref $env:GITHUB_REF
```

Modo JSON:

```powershell
python -m src.agent.cli "Mostrame el ticket 31426" --ref $env:GITHUB_REF --json
```

La variable `OPENAI_MODEL` es opcional; si se omite, el cliente utiliza
`gpt-5.6`.

## Testing

Desde la raíz:

```powershell
python -m pytest -q
```

Para ejecutar primero una validación rápida:

```powershell
python -m pytest -q tests/test_agent_router.py tests/test_consultant.py
```

La rama debe permanecer verde antes de promover cambios a `main`.

## Alcance actual

El MVP actual prioriza:

1. retrieval determinístico y trazable;
2. separación Standard / Custom;
3. evidencia y reasoning acotado;
4. contexto multi-hop limitado;
5. consultoría LLM sobre evidencia acotada;
6. governance para propuestas de Knowledge;
7. MCP read-only como fuente complementaria de evidencia, sin promoción automática a Knowledge.

No se considera todavía parte de esta baseline:

- ejecución mutante contra SAP;
- escritura en SAP;
- retrieval semántico/vectorial;
- memoria conversacional persistente;
- conexión directa a un sistema SAP productivo.

## Source / Evidence Selection

Antes de sintetizar una conclusión, AgenteSAP aplica una política determinística para
identificar qué capa de evidencia es pertinente a la pregunta:

- consultas genéricas SAP → SAP Standard + Internal;
- comparación Standard/Custom → ambas capas;
- preguntas sobre implementación → Internal;
- preguntas sobre estado/configuración actual → Runtime;
- la selección de una fuente es una necesidad de evidencia, no evidencia por sí misma.

Si la capa esperada no está disponible, se registra como gap. La ausencia de una
fuente no se interpreta como prueba de que el dato no exista.

## MCP Provider Strategy

La selección de evidencia y la selección de proveedor MCP son capas separadas:

- `runtime` identifica una necesidad de observación del sistema, pero no habilita por sí sola una conexión.
- `sap-devs` puede aportar contexto de desarrollador como evidencia externa/suplementaria, pero no satisface una necesidad `runtime`.
- `sap-mcp-server` y `abap_ai` están registrados como proveedores potenciales de runtime, pero permanecen en estado **fail-closed** hasta disponer de un contrato explícito de herramientas read-only.
- La estrategia de proveedor no ejecuta herramientas ni eleva certainty; únicamente determina elegibilidad y readiness.
- Una pregunta de runtime sin un proveedor read-only listo debe conservar el gap de runtime en lugar de degradar silenciosamente a contexto externo.

## QAS Runtime Read-only Contract

La primera etapa de runtime está deliberadamente limitada a **QAS + mcp_readonly**.
El proveedor sap_mcp_server sólo puede activarse cuando se cumplen simultáneamente estas condiciones:

- AGENTESAP_SAP_RUNTIME_ENABLED=true;
- AGENTESAP_SAP_RUNTIME_LANDSCAPE=QAS;
- AGENTESAP_SAP_RUNTIME_SCOPE=mcp_readonly;
- existe una allowlist explícita de herramientas de lectura;
- el nombre concreto de la herramienta fue verificado contra el catálogo del binario instalado.

El repositorio no fija un nombre de herramienta inventado: sap-mcp-server distribuye su catálogo de herramientas dentro del binario y documenta que la capacidad incluye lectura de tablas y ADT SQL/Open SQL/DDIC. La configuración de conexión y sus secretos permanecen fuera de Git; el servidor oficial indica que connections.json es local y que la autenticación se realiza mediante credenciales OAuth2 del backend.

El contrato de AgenteSAP agrega una barrera adicional: aunque exista una conexión, un proveedor runtime no se considera listo si no está en QAS, no usa mcp_readonly o no tiene una allowlist explícita. La ausencia de configuración no se convierte en una falsa observación runtime.

Ejemplo no secreto: config/sap-mcp-qas.example.env.

### Descubrimiento seguro del catálogo QAS

Antes de autorizar una herramienta runtime concreta, AgenteSAP permite un modo discovery_only que sólo ejecuta la operación de protocolo MCP para listar las herramientas disponibles. No ejecuta ninguna herramienta SAP y no preautoriza ninguna herramienta runtime.

Con una conexión QAS válida y scope mcp_readonly, se puede ejecutar:

    python -m src.sap.runtime_cli discover-qas --pretty

El resultado debe utilizarse para identificar el nombre y schema exactos de la herramienta de lectura que luego será incorporada a AGENTESAP_SAP_RUNTIME_READ_TOOLS. La configuración sigue deshabilitada por defecto.

Para validar operativamente una allowlist ya configurada, sin ejecutar ninguna herramienta SAP:

    python -m src.sap.runtime_cli readiness-qas --pretty --verify-catalog

Este probe ejecuta únicamente MCP `tools/list` a través de la validación del catálogo. Sólo informa `runtime_ready=true` cuando las herramientas configuradas están anunciadas y cada una declara `readOnlyHint=true` sin `destructiveHint=true`.

## Runtime read-only actual

La baseline ya contiene el contrato técnico para lecturas QAS opt-in. La ejecución efectiva depende de una conexión `sap-mcp-server` disponible, scope `mcp_readonly` y una herramienta concreta anunciada por `tools/list` con `readOnlyHint=true`. Sin esa conexión y catálogo verificable, el estado correcto permanece `pending` y el agente no inventa observaciones.

## Próximo roadmap

La secuencia de avance queda definida por calidad de evidencia antes que por complejidad de infraestructura:

1. **SAP Help Knowledge Foundation (en esta rama)**: metadata, provenance, chunking estructural, source audit y retrieval Standard.
2. **Validación y benchmark SAP MM**: Material Master, Inventory Management, Goods Movements, Movement Types, Purchasing, GR e Invoice Verification.
3. **SAP runtime read-only**: habilitar progresivamente `sap-mcp-server` con allowlists y contratos de provenance por sistema/landscape/objeto.
4. **ABAP custom MCP**: incorporar capacidades específicas sólo cuando exista un caso funcional y un contrato de lectura claramente definido.

Embeddings/vector DB quedan fuera de esta etapa hasta que la cobertura y calidad del conocimiento estructurado justifiquen su incorporación.


## Consultant Regression Benchmark

Además de la suite automatizada, el proyecto mantiene `benchmarks/consultant-regression.md` con diez casos para validar el comportamiento consultivo del agente: evidencia, certeza, separación Standard/Custom, conflictos, multi-hop y límites de ejecución. Debe revisarse cuando cambien routing, retrieval, evidence, reasoning, Consultant o generación documental.
