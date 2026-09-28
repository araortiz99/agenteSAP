# Knowledge Lifecycle Standard

## 1. Objetivo

Definir el ciclo de vida del conocimiento reutilizable de agenteSAP y los controles necesarios para incorporar, modificar, revisar, validar y publicar conocimiento sin perder trazabilidad.

El estándar complementa:
- standards/documentation-standard.md
- standards/versioning-standard.md
- standards/security-standard.md
- standards/knowledge-classification-standard.md

## 2. Principio fundamental

El agente puede proponer conocimiento, pero la reutilización organizacional requiere una etapa explícita de validación.

```
DOCUMENTACIÓN
    ↓
DISCOVERY
    ↓
CANDIDATE
    ↓
IN_REVIEW
    ↓
APPROVED / VALIDATED
    ↓
REUSABLE KNOWLEDGE
```

La publicación en Git no implica aprobación funcional.

## 3. Áreas publicables

La persistencia automatizada del agente está limitada inicialmente a:
- knowledge/
- knowledge/relationships/

No se permite escritura automatizada en:
- standards/
- templates/
- agent/
- tickets/
- .github/

Los tickets representan contexto histórico y no deben ser reescritos por el flujo de Knowledge Governance.

## 4. Human-in-the-loop

Todo cambio persistente de Knowledge debe pasar por Pull Request.

El agente puede:
- proponer;
- validar estructura;
- validar clasificación;
- validar seguridad;
- conservar trazabilidad;
- crear el PR.

El agente no puede:
- hacer merge automático;
- aprobar su propio cambio;
- declarar validado un conocimiento sin evidencia explícita;
- eliminar historial;
- sobrescribir silenciosamente una versión aprobada.

## 5. Creación

Antes de crear Knowledge:
1. buscar documentación equivalente;
2. comprobar entidades relacionadas;
3. determinar knowledge_type;
4. determinar knowledge_scope;
5. identificar fuentes;
6. identificar ticket cuando exista;
7. validar metadata;
8. ejecutar security gate;
9. asignar versión inicial;
10. generar propuesta.

La ausencia de un resultado no prueba inexistencia.

## 6. Actualización

Antes de modificar Knowledge:
1. recuperar la versión actual;
2. conservar su SHA;
3. determinar el tipo de cambio;
4. incrementar la versión lógica cuando corresponda;
5. conservar trazabilidad;
6. verificar referencias y relaciones dependientes;
7. ejecutar security gate;
8. proponer PR.

Nunca modificar directamente una rama protegida.

## 7. Versionado

La versión lógica se rige por standards/versioning-standard.md.

- PATCH: corrección sin cambio funcional;
- MINOR: ampliación sin cambio funcional principal;
- MAJOR: cambio funcional relevante.

El agente no aumenta la versión arbitrariamente.

## 8. Relaciones

Una nueva relación solo puede persistirse cuando existe evidencia documental explícita.

Toda relación debe conservar:
- source;
- target;
- relation_type;
- certainty;
- status;
- evidence_source_id cuando exista;
- path que la respalda.

Coocurrencia != relación.

## 9. Seguridad

Antes de publicar:
- rechazar secretos;
- rechazar claves privadas;
- rechazar tokens;
- rechazar API keys;
- minimizar datos productivos;
- conservar solo información necesaria para utilidad funcional.

La sanitización automática no debe alterar evidencia sin revisión humana. Un posible secreto bloquea la publicación hasta su corrección.

## 10. Pull Request

Todo cambio persistente debe incluir:
- objetivo;
- ticket relacionado cuando exista;
- paths modificados;
- versión anterior y nueva cuando aplique;
- tipo de cambio;
- fuentes principales;
- impacto conocido;
- validaciones ejecutadas.

El PR es una unidad de revisión, no confirmación funcional.

## 11. Branching

La rama debe derivar de una base_ref explícita, ser distinta de ella y nunca escribir directamente en main/master.

Ejemplos:
- docs/ticket-31426-knowledge
- feat/knowledge-snc-k1
- fix/knowledge-zmm-imx-0004

## 12. No promoción automática

La existencia de un documento bajo knowledge/ no significa que esté confirmado, aprobado, vigente o universalizado.

certainty y status conservan su valor explícito.

El agente puede proponer draft o in_review. No puede autodeclarar approved o validated sin evidencia explícita.

## 13. Integridad

La publicación debe ser reproducible a partir de:
- repository ref;
- path;
- contenido;
- metadata;
- versión;
- fuentes;
- ticket;
- commit;
- Pull Request.

## 14. Regla final

```
SEARCH
→ CLASSIFY
→ VALIDATE
→ SECURITY CHECK
→ VERSION
→ PROPOSE
→ REVIEW
→ MERGE
→ REUSE
```

Nunca:
```
GENERATE
→ WRITE DIRECTLY TO MAIN
→ ASSUME VALIDATED
```
