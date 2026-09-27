Actúa como arquitecto de repositorios de conocimiento y especialista en agentes de IA.

Genera desde cero:

.github/copilot-instructions.md

Estas instrucciones deben gobernar el trabajo realizado sobre el repositorio `agenteSAP`.

==================================================
1. PROPÓSITO DEL REPOSITORIO
==================================================

`agenteSAP` es una base de conocimiento estructurada para un agente de consultoría funcional SAP.

El repositorio debe priorizar:

- trazabilidad;
- evidencia;
- reutilización;
- consistencia;
- seguridad;
- separación Standard/Custom.

==================================================
2. ESTRUCTURA
==================================================

standards/
=
reglas.

templates/
=
estructuras.

knowledge/
=
Knowledge reusable.

tickets/
=
contexto histórico.

agent/
=
comportamiento.

==================================================
3. CLASIFICACIÓN
==================================================

Consultar:

standards/knowledge-classification-standard.md

Antes de crear o modificar conocimiento.

==================================================
4. DOCUMENT METADATA
==================================================

Los documentos deben utilizar:

ticket_id
document_type
knowledge_type
knowledge_scope
version
status
date
author

==================================================
5. KNOWLEDGE_TYPE
==================================================

Valores permitidos:

standard
custom
mixed
unknown

==================================================
6. KNOWLEDGE_SCOPE
==================================================

Valores:

global
organization
country
company
plant
process
project
ticket
unknown

==================================================
7. SAP OBJECT
==================================================

Utilizar:

origin

y:

implementation_type.

origin:

standard
custom
unknown

implementation_type:

standard
configuration
enhancement
z_development
integration
unknown

==================================================
8. REGLAS
==================================================

No inferir Standard/Custom solamente por:

- nombre;
- módulo;
- transacción;
- prefijo;
- apariencia.

Z/Y es indicio, no evidencia absoluta.

==================================================
9. MIXED
==================================================

Utilizar:

mixed

cuando una pieza de conocimiento combine de manera relevante:

SAP Standard
+
Configuración
+
Custom
+
Integración.

==================================================
10. UNKNOWN
==================================================

Utilizar:

unknown

cuando no exista evidencia suficiente.

Nunca rellenar unknown con una suposición.

==================================================
11. SOURCE
==================================================

Utilizar:

source_id

cuando exista una fuente documentada.

Las fuentes deben permitir rastrear el origen de las afirmaciones.

==================================================
12. RELATIONSHIPS
==================================================

No crear relaciones por simple co-ocurrencia.

Una relación debe tener:

source
relation
target

y evidencia cuando corresponda.

==================================================
13. DUPLICACIÓN
==================================================

Antes de crear:

- Object;
- Process;
- Business Rule;
- Relationship;
- Source;

buscar si ya existe.

No crear duplicados.

==================================================
14. SEGURIDAD
==================================================

No almacenar:

- passwords;
- tokens;
- API keys;
- credenciales;
- secretos;
- claves privadas.

Sanitizar información productiva innecesaria.

==================================================
15. RETRIEVAL
==================================================

El agente debe recuperar conocimiento leyendo directorios y archivos relevantes.

No asumir que promptMaestro contiene conocimiento SAP.

==================================================
16. STANDARD VS CUSTOM
==================================================

Siempre diferenciar:

SAP Standard
Configuración
Enhancement
Z Development
Integration
Unknown

==================================================
17. CAMBIOS
==================================================

Al modificar conocimiento:

- preservar trazabilidad;
- incrementar versión cuando corresponda;
- no eliminar información confirmada sin justificación;
- mantener referencias;
- revisar relaciones afectadas.

==================================================
18. REGLA FINAL
==================================================

NO INVENTAR.

NO DUPLICAR.

NO GENERALIZAR.

NO CONFUNDIR STANDARD CON CUSTOM.

NO CONFUNDIR CONFIGURACIÓN CON DESARROLLO.

NO CREAR RELACIONES SIN EVIDENCIA.

NO CONVERTIR INFERENCIAS EN HECHOS.

MANTENER TRAZABILIDAD.

MANTENER SEGURIDAD.

Entrega únicamente el contenido completo final de:

.github/copilot-instructions.md
