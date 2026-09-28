# agenteSAP

Agente consultivo para conocimiento y documentación funcional SAP.

## Estado actual

**Baseline funcional avanzada — rama `feature/agent-mvp-search`.**

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
  └── Internal / Custom
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

## Reglas de seguridad funcional

- SAP Standard e implementación interna son capas de evidencia distintas.
- La coocurrencia no crea relaciones.
- Retrieval no equivale a conclusión.
- Hop no equivale a certainty.
- El LLM no puede elevar certainty ni inventar evidencia.
- El agente no ejecuta SAP.
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
$env:GITHUB_REF = "feature/agent-mvp-search"
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
6. governance para propuestas de Knowledge.

No se considera todavía parte de esta baseline:

- ejecución contra SAP;
- escritura en SAP;
- retrieval semántico/vectorial;
- memoria conversacional persistente;
- conexión directa a un sistema SAP productivo.

## Próximo MVP

Antes de introducir embeddings o una vector DB, la siguiente etapa recomendada es
**MVP 7 — SAP MM Knowledge Foundation**: ampliar conocimiento funcional curado de MM,
objetos, procesos, reglas, tablas, movimientos, integración MM-FI e incidentes
sanitizados, manteniendo la arquitectura determinística y trazable.
