Actúa como arquitecto de conocimiento, consultor funcional SAP senior y especialista en gestión documental, versionado de conocimiento y control de cambios mediante Git.

Tu tarea es generar el archivo:

standards/versioning-standard.md

Este archivo será el ESTÁNDAR MAESTRO DE VERSIONADO del repositorio `agenteSAP`.

IMPORTANTE:

- No debes crear templates.
- No debes crear otros estándares.
- No debes modificar otros archivos.
- Debes generar únicamente el contenido completo de:
  standards/versioning-standard.md

El estándar debe complementar `standards/documentation-standard.md`.

No debes duplicar innecesariamente las reglas de documentación ya definidas allí.

Su propósito específico es establecer cómo se crean, modifican, versionan, relacionan, revisan, reemplazan y conservan las distintas versiones de la documentación y conocimiento del repositorio.

==================================================
1. CONTEXTO
==================================================

El repositorio `agenteSAP` es una base de conocimiento destinada a soportar un futuro agente de IA especializado en consultoría funcional SAP.

El repositorio contendrá documentación como:

- requerimientos;
- especificaciones funcionales;
- pruebas funcionales;
- análisis;
- debug;
- investigaciones;
- conocimiento sobre objetos SAP;
- procesos;
- reglas de negocio;
- relaciones entre conocimiento.

La documentación debe evolucionar de forma controlada.

El versionado debe permitir responder:

- qué información existía anteriormente;
- qué cambió;
- cuándo cambió;
- quién realizó el cambio;
- por qué cambió;
- qué versión está vigente;
- qué versión fue implementada;
- qué versión fue validada;
- qué documentación quedó obsoleta;
- qué conocimiento histórico debe conservarse.

==================================================
2. OBJETIVO
==================================================

Definir reglas uniformes para el versionado de:

- documentos;
- conocimiento;
- especificaciones;
- análisis;
- pruebas;
- reglas;
- relaciones;
- estructuras documentales cuando corresponda.

El estándar debe garantizar:

- trazabilidad;
- reproducibilidad;
- historial;
- integridad;
- claridad;
- consistencia;
- compatibilidad con Git;
- recuperación histórica;
- identificación inequívoca de versiones.

==================================================
3. PRINCIPIO FUNDAMENTAL
==================================================

Toda modificación relevante debe poder explicarse.

La cadena de control debe ser:

CAMBIO
↓
MOTIVO
↓
VERSIÓN
↓
EVIDENCIA
↓
REVISIÓN
↓
ESTADO
↓
HISTORIAL

Nunca debe existir un cambio funcional importante cuyo origen o motivo no pueda identificarse.

==================================================
4. VERSIONADO DOCUMENTAL
==================================================

Todos los documentos que estén sujetos a evolución deben utilizar un campo:

```yaml
version:

Formato inicial recomendado:

MAJOR.MINOR

Ejemplo:

version: "1.0"

El versionado debe ser incremental y explícito.

==================================================
5. TIPOS DE CAMBIO

Los cambios deben clasificarse como:

PATCH

Cambios menores que no modifican el significado funcional del documento.

Ejemplos:

corrección ortográfica;
corrección gramatical;
mejora de redacción;
aclaración textual;
corrección de formato;
corrección de referencia documental.

Ejemplo:

1.0 → 1.0.1
MINOR

Cambios que agregan información o amplían el documento sin modificar su significado funcional principal.

Ejemplos:

agregar una validación;
agregar un escenario;
agregar una evidencia;
agregar una sección;
documentar una nueva dependencia;
agregar información funcional relevante.

Ejemplo:

1.0 → 1.1
MAJOR

Cambios que modifican sustancialmente el contenido funcional o el significado de la solución.

Ejemplos:

cambio de requerimiento;
cambio de comportamiento esperado;
cambio de solución funcional;
cambio importante de reglas de negocio;
cambio de alcance;
cambio de proceso;
cambio que invalida pruebas anteriores;
cambio que requiere una nueva validación funcional.

Ejemplo:

1.1 → 2.0

Cuando exista duda entre dos niveles, debe evaluarse el impacto funcional.

==================================================
6. REGLA DE IMPACTO

El nivel de versión debe determinarse por el impacto real del cambio y no únicamente por la cantidad de texto modificada.

Un cambio de una sola línea puede requerir MAJOR si modifica una regla de negocio crítica.

Una modificación extensa puede ser PATCH si solamente reorganiza o corrige documentación sin modificar su significado.

==================================================
7. VERSIONES DE DOCUMENTOS FUNCIONALES

Los documentos funcionales deben mantener coherencia entre:

requerimiento;
especificación funcional;
pruebas;
análisis;
debug;
implementación.

Ejemplo:

REQUERIMIENTO
v1.0
↓
ESPECIFICACIÓN
v1.0
↓
IMPLEMENTACIÓN
↓
PRUEBAS
v1.0

Si la especificación cambia significativamente:

ESPECIFICACIÓN
v2.0

debe evaluarse si:

el requerimiento también cambió;
las pruebas anteriores siguen siendo válidas;
la implementación debe cambiar;
debe generarse una nueva versión de pruebas.
==================================================
8. VERSIONADO DE PRUEBAS

Las pruebas deben identificar qué versión funcional validan.

Ejemplo:

version: "2.0"

y:

Versión funcional validada: 2.0

Nunca debe considerarse automáticamente que una prueba de una versión anterior valida una nueva versión funcional.

Debe evaluarse si corresponde:

mantener la prueba;
actualizarla;
ejecutar regresión;
crear nuevos casos.
==================================================
9. CAMBIOS DE ESTADO

El versionado debe distinguir entre:

modificación documental;
modificación funcional;
modificación técnica;
cambio de estado.

Un cambio de estado no necesariamente implica cambio de versión.

Ejemplo:

draft → in_review

puede no modificar el contenido.

Por otro lado:

draft v1.0
→ cambio funcional
→ v2.0

sí requiere una nueva versión.

==================================================
10. DOCUMENTOS OBSOLETOS

Cuando un documento deje de representar el comportamiento vigente:

no debe eliminarse automáticamente;
debe conservarse cuando tenga valor histórico;
debe marcarse como obsolete;
debe existir una referencia hacia la documentación vigente cuando corresponda.

Ejemplo:

Documento v1.0
status: obsolete

Reemplazado por:
Documento v2.0
==================================================
11. HISTORIAL DE CAMBIOS

Cuando un documento tenga cambios relevantes, debe poder identificarse:

versión;
fecha;
autor;
motivo;
descripción;
impacto.

Formato recomendado:

## Historial de cambios

| Versión | Fecha | Autor | Tipo | Descripción |
|---|---|---|---|---|
| 1.0 | 2026-09-01 | Analista Funcional | Inicial | Creación |
| 1.1 | 2026-09-03 | Analista Funcional | Minor | Se agrega validación |
| 2.0 | 2026-09-10 | Analista Funcional | Major | Cambio de solución |

El historial debe mantenerse claro y conciso.

==================================================
12. GIT COMO CONTROL DE VERSIONES

Git será el mecanismo principal de control de cambios del repositorio.

Debe utilizarse para preservar:

commits;
diferencias;
historial;
autores;
fechas;
ramas;
merges;
evolución documental.

El versionado documental y Git cumplen funciones diferentes.

Git registra cambios técnicos en archivos.

El campo version representa la versión lógica del conocimiento/documento.

Ambos mecanismos deben coexistir.

==================================================
13. COMMITS

Los commits relacionados con documentación deben ser descriptivos.

Formato recomendado:

<tipo>: <descripción>

Tipos sugeridos:

docs
fix
feat
refactor
test
chore

Ejemplos:

docs: update SNC functional analysis
docs: add functional specification for ticket 33007
fix: correct business rule reference
feat: add inventory process documentation
test: update functional test cases

No utilizar mensajes genéricos como:

update
cambios
fix
prueba
final
nuevo

cuando no permitan comprender qué cambió.

==================================================
14. RELACIÓN ENTRE COMMIT Y DOCUMENTO

Cuando sea relevante, el commit debe permitir identificar:

ticket;
documento;
cambio realizado.

Ejemplo:

docs(33007): update SNC functional specification

Esto facilita la trazabilidad entre:

TICKET
↓
DOCUMENTO
↓
VERSIÓN
↓
COMMIT

==================================================
15. BRANCHES

Las ramas deben utilizarse cuando el cambio requiera trabajo aislado o revisión.

Ejemplos:

feature/
fix/
docs/

Ejemplo:

docs/ticket-33007

o:

feature/ticket-33007

La estrategia exacta de branching podrá evolucionar posteriormente.

No crear ramas innecesarias para cambios triviales.

==================================================
16. PULL REQUESTS

Los cambios relevantes deben revisarse mediante Pull Request cuando el flujo del repositorio lo requiera.

Un Pull Request debería indicar:

objetivo;
ticket relacionado;
documentos afectados;
tipo de cambio;
impacto;
pruebas realizadas cuando correspondan.

No aprobar cambios relevantes sin revisar su impacto documental.

==================================================
17. COMPATIBILIDAD

Antes de incrementar una versión se debe evaluar el impacto sobre:

documentos relacionados;
requerimientos;
especificaciones;
pruebas;
reglas de negocio;
procesos;
objetos SAP;
relaciones;
conocimiento reutilizable.

Una modificación en una regla puede afectar múltiples documentos.

No asumir que un documento es independiente solamente porque está almacenado en un archivo separado.

==================================================
18. CAMBIOS QUE INVALIDAN DOCUMENTACIÓN

Debe considerarse que un cambio puede invalidar:

pruebas;
análisis;
conclusiones;
reglas;
referencias;
documentación relacionada.

Cuando esto ocurra:

identificar los documentos afectados;
evaluar si requieren nueva versión;
actualizar relaciones;
conservar la trazabilidad histórica;
documentar el impacto.
==================================================
19. VERSIONADO DEL CONOCIMIENTO

No todo conocimiento debe versionarse de la misma manera.

Debe diferenciarse entre:

Documento

Tiene versiones explícitas.

Regla de negocio

Debe registrar su vigencia y origen cuando corresponda.

Objeto SAP

Debe documentarse su estado y relación con versiones funcionales.

Proceso

Puede evolucionar y debe mantener trazabilidad histórica.

Relación

Debe modificarse cuando cambien las relaciones entre entidades.

El objetivo es preservar la evolución del conocimiento, no solamente de los archivos.

==================================================
20. CAMBIOS RETROACTIVOS

No modificar documentación histórica para hacerla coincidir con el comportamiento actual.

Si se descubre que una documentación anterior era incorrecta:

conservar la versión histórica;
crear una nueva versión;
explicar la corrección;
identificar la evidencia que provocó el cambio.

Ejemplo:

v1.0:
Se documentó comportamiento A.

v2.0:
Se determina mediante evidencia que el comportamiento real es B.

Motivo:
Debug / prueba / análisis.
==================================================
21. VERSIONADO Y EVIDENCIA

Los cambios importantes deben tener una justificación.

Cuando sea posible, registrar:

ticket;
análisis;
debug;
prueba;
fuente;
evidencia;
decisión funcional.

No cambiar una regla crítica sin registrar por qué cambió.

==================================================
22. REGLA DE NO SOBRESCRITURA SILENCIOSA

Nunca modificar una versión aprobada o validada sin dejar trazabilidad.

Una nueva versión debe preservar la existencia lógica de la anterior.

La historia debe poder reconstruirse mediante:

Git;
historial de cambios;
referencias documentales;
estados.
==================================================
23. CONTROL DE VERSIONES EN DOCUMENTACIÓN GENERADA POR IA

Cuando un agente de IA genere o modifique documentación debe:

identificar la versión actual;
identificar el cambio solicitado;
evaluar impacto;
proponer el incremento de versión;
preservar el historial;
indicar documentos relacionados afectados;
no inventar cambios;
no modificar versiones históricas;
respetar el estándar de documentación;
mantener trazabilidad.

La IA no debe incrementar versiones arbitrariamente.

==================================================
24. REGLAS DE COMPATIBILIDAD

Antes de finalizar una nueva versión verificar:

metadata;
estructura documental;
referencias;
ticket;
relaciones;
pruebas;
reglas;
objetos SAP;
procesos;
estado;
historial.
==================================================
25. CHECKLIST

Antes de aceptar una nueva versión:

Identificación
¿Existe versión anterior?
¿Se identificó el documento?
¿Se identificó el ticket?
¿Se identificó el autor?
¿Se registró la fecha?
Cambio
¿Qué cambió?
¿Por qué cambió?
¿El cambio es PATCH, MINOR o MAJOR?
¿Cuál es el impacto?
Trazabilidad
¿Existe evidencia?
¿Existe commit?
¿Existe ticket relacionado?
¿Se actualizaron documentos dependientes?
Calidad
¿Las referencias siguen siendo válidas?
¿Las pruebas siguen siendo aplicables?
¿Las reglas siguen siendo correctas?
¿Existe documentación obsoleta que deba marcarse?
==================================================
26. PRINCIPIO FINAL

El versionado no debe utilizarse únicamente para saber que un archivo cambió.

Debe permitir comprender la evolución del conocimiento.

La cadena final es:

CAMBIO
↓
MOTIVO
↓
EVIDENCIA
↓
VERSIÓN
↓
VALIDACIÓN
↓
HISTORIAL
↓
CONOCIMIENTO VIGENTE

El objetivo es que agenteSAP pueda reconstruir cómo evolucionó una decisión funcional y qué información era válida en cada momento.

==================================================
27. INSTRUCCIÓN FINAL

Genera únicamente:

standards/versioning-standard.md

El archivo debe:

estar completamente escrito en Markdown;
ser autocontenido;
complementar standards/documentation-standard.md;
ser normativo;
ser claro para consultores funcionales SAP;
ser interpretable por agentes de IA;
ser compatible con Git/GitHub;
no inventar información;
no crear otros archivos;
no incluir explicaciones externas a este estándar.
