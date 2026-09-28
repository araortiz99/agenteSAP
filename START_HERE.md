# AgenteSAP — inicio rápido

## Qué está listo

La rama `main` contiene un workbench web local para el agente consultivo SAP.

- Interfaz web local.
- Consultas contra el conocimiento del repositorio.
- Análisis de tickets.
- Evidencia y trazabilidad.
- Exploración de relaciones.
- LLM opcional mediante `OPENAI_API_KEY`.
- SAP runtime QAS read-only opcional y deshabilitado por defecto.
- Ninguna operación de escritura SAP expuesta por la aplicación local.

## Requisitos

- Windows con PowerShell.
- Python 3.12.
- Acceso a GitHub para que el agente pueda leer el repositorio.
- Para respuestas LLM: una variable `OPENAI_API_KEY`.

## Primera ejecución

Desde la raíz del repositorio:

```powershell
.\start_agentesap.ps1
```

El launcher crea `.venv`, instala `requirements.txt` y abre el servidor local.

Luego abrir:

```
http://127.0.0.1:8765
```

La aplicación queda vinculada a localhost. No debe cambiarse el host para exponerla en la red.

## Configuración opcional de GitHub

Por defecto:

```text
GITHUB_OWNER=araortiz99
GITHUB_REPO=agenteSAP
GITHUB_REF=main
```

Si el repositorio es público, `GITHUB_TOKEN` no es necesario para el uso básico. Un token sólo debe configurarse mediante variables de entorno y nunca almacenarse en Git.

## Configuración LLM

Para habilitar el consultor LLM:

```powershell
$env:OPENAI_API_KEY = "TU_CLAVE"
$env:OPENAI_MODEL = "gpt-5.6"
.\start_agentesap.ps1
```

La clave no forma parte del repositorio.

## Comprobaciones rápidas

Health:

```
http://127.0.0.1:8765/health
```

Estado:

```
http://127.0.0.1:8765/api/status
```

CLI determinístico:

```powershell
python -m src.agent.cli "Buscá SAP Standard sobre material master" --ref main
```

CLI consultivo:

```powershell
python -m src.agent.cli "Consultá sobre material master" --ref main
```

## QAS read-only

La integración QAS permanece deshabilitada por defecto.

Primero se debe validar la configuración:

```powershell
python -m src.sap.runtime_cli readiness-qas --pretty
```

Para discovery seguro:

```powershell
python -m src.sap.runtime_cli discover-qas --pretty
```

Discovery sólo ejecuta `tools/list`; no ejecuta herramientas SAP.

No se debe completar una allowlist con nombres inventados. El nombre y schema de cada herramienta deben provenir del catálogo real del servidor MCP instalado.

## Seguridad operativa

La aplicación local es un consultor read-only. No introducir credenciales, tokens ni secretos en archivos versionados.

El runtime SAP sólo puede habilitarse explícitamente en QAS, con scope `mcp_readonly` y allowlist de herramientas validada. La ausencia de una conexión o de evidencia runtime debe permanecer como gap; nunca debe convertirse en una observación inventada.

## Problemas frecuentes

### Falta `OPENAI_API_KEY`

El modo determinístico puede seguir funcionando para retrieval. Para consultas `consult`, configurar la variable antes de iniciar la app.

### No hay conexión a GitHub

Verificar conectividad y, si el repositorio requiere autenticación, configurar `GITHUB_TOKEN` como variable de entorno.

### El puerto 8765 está ocupado

Ejecutar:

```powershell
$env:AGENTESAP_APP_PORT = "8766"
python -m src.app
```

### QAS no está listo

No activar runtime a ciegas. Ejecutar `readiness-qas --pretty`, revisar el motivo y sólo después completar la configuración real del servidor MCP.

## Estado de esta entrega

Esta entrega convierte el workbench existente en un flujo reproducible de inicio local. La validación contra un SAP QAS real sigue siendo una etapa separada y explícitamente opt-in.
