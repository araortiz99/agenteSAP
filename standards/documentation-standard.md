Actúa como arquitecto de documentación, consultor funcional SAP senior y arquitecto de conocimiento para agentes de IA.

Genera desde cero:

standards/documentation-standard.md

Este será el estándar maestro de documentación de agenteSAP.

Debe ser autocontenido y definir cómo se documenta conocimiento, requerimientos, análisis, debug, investigación, pruebas y especificaciones.

Debe utilizar como autoridad de clasificación:

standards/knowledge-classification-standard.md

==================================================
1. OBJETIVO
==================================================

Definir un estándar único para crear documentación:

- consistente;
- trazable;
- reutilizable;
- versionable;
- comprensible por humanos;
- recuperable por agentes de IA.

==================================================
2. PRINCIPIO TRANSVERSAL
==================================================

Todo documento debe distinguir:

document_type

de:

knowledge_type

de:

knowledge_scope.

Definir:

document_type = tipo documental.

knowledge_type = naturaleza del conocimiento.

knowledge_scope = ámbito de aplicación.

==================================================
3. METADATA OBLIGATORIA
==================================================

Todo documento debe contemplar:

---
ticket_id: ""
document_type: ""
knowledge_type: ""
knowledge_scope: ""
version: "1.0"
status: "draft"
date: ""
author: ""
---

Si no existe ticket:

ticket_id: "N/A"

==================================================
4. DOCUMENT TYPES
==================================================

Definir como documentación oficial:

- requirement
- functional-specification
- functional-test

Definir como actividades de consultoría:

- analysis
- debug
- investigation

Definir:

ticket

como entidad de contexto y trazabilidad.

==================================================
5. KNOWLEDGE_TYPE
==================================================

Utilizar únicamente:

- standard
- custom
- mixed
- unknown

La definición completa debe referenciar:

standards/knowledge-classification-standard.md

==================================================
6. KNOWLEDGE_SCOPE
==================================================

Utilizar:

- global
- organization
- country
- company
- plant
- process
- project
- ticket
- unknown

==================================================
7. STATUS DOCUMENTAL
==================================================

Definir:

- draft
- in_review
- approved
- implemented
- validated
- obsolete

Aclarar que status documental no equivale al lifecycle del Knowledge.

==================================================
8. CICLO DOCUMENTAL
==================================================

Definir:

Need
↓
Requirement
↓
Functional Specification
↓
Implementation
↓
Functional Tests
↓
Validation

Analysis, Debug e Investigation pueden aparecer transversalmente.

==================================================
9. CLASIFICACIÓN DE HECHOS
==================================================

Todo análisis relevante debe distinguir:

HECHO
HIPÓTESIS
INFORMACIÓN FALTANTE
CONCLUSIÓN

==================================================
10. STANDARD VS CUSTOM
==================================================

Definir reglas:

- nunca atribuir comportamiento local a SAP Standard sin evidencia;
- distinguir configuración;
- distinguir enhancement;
- distinguir desarrollo Z/Y;
- distinguir integración;
- utilizar mixed cuando corresponda;
- utilizar unknown cuando no pueda determinarse.

==================================================
11. TICKET_ID
==================================================

ticket_id es el identificador transversal que permite conectar:

- requerimiento;
- especificación;
- análisis;
- debug;
- investigación;
- pruebas;
- decisiones;
- evidencias.

No utilizar ticket_id como sustituto de los IDs de Knowledge.

==================================================
12. DOCUMENTACIÓN RELACIONADA
==================================================

Cada documento debe permitir referencias a:

- otros documentos;
- tickets;
- objetos;
- procesos;
- reglas;
- relaciones;
- fuentes.

==================================================
13. REGLA DE NO DUPLICACIÓN
==================================================

Antes de crear documentación:

buscar si existe documentación equivalente.

No duplicar conocimiento.

Actualizar cuando corresponda.

==================================================
14. VERSIONADO
==================================================

Distinguir:

document version

de:

Git history.

Utilizar MAJOR.MINOR.PATCH:

PATCH:
correcciones editoriales.

MINOR:
información adicional sin cambio funcional.

MAJOR:
cambio funcional relevante.

==================================================
15. SEGURIDAD
==================================================

No almacenar:

- passwords;
- tokens;
- API keys;
- credenciales;
- claves privadas;
- secretos.

Sanitizar:

- screenshots;
- logs;
- dumps;
- datos productivos;
- información personal innecesaria.

==================================================
16. REGLAS PARA IA
==================================================

El agente debe:

- buscar antes de crear;
- leer metadata;
- respetar knowledge_type;
- respetar knowledge_scope;
- mantener incertidumbre;
- conservar trazabilidad;
- no inventar;
- no generalizar.

==================================================
17. QUALITY CHECKLIST
==================================================

Incluir checklist para validar:

- metadata;
- clasificación;
- ticket_id;
- evidencia;
- fuentes;
- trazabilidad;
- seguridad;
- versionado;
- documentación relacionada;
- información pendiente.

