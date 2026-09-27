Quiero que crees el archivo:

knowledge/sap-objects/object.md

Este archivo será la plantilla maestra para documentar OBJETOS SAP dentro del repositorio agenteSAP.

==================================================
CONTEXTO
==================================================

El repositorio agenteSAP está construyendo una base de conocimiento estructurada para un futuro agente de IA especializado en consultoría funcional SAP.

Las fases anteriores establecieron:

FASE 1 — STANDARDS
- standards/documentation-standard.md
- standards/versioning-standard.md
- standards/security-standard.md

FASE 2 — TEMPLATES
- templates/requirement.md
- templates/functional-specification.md
- templates/functional-tests.md
- templates/analysis.md
- templates/debug.md
- templates/investigation.md

La FASE 3 — KNOWLEDGE comienza a construir conocimiento SAP reutilizable.

La carpeta actual es:

knowledge/sap-objects/

El archivo object.md será la plantilla base para documentar cualquier objeto SAP identificado de forma real y verificable.

==================================================
OBJETIVO
==================================================

Crear una estructura estándar para registrar conocimiento sobre objetos SAP.

La plantilla debe permitir documentar objetos como:

- Transacciones
- Tablas
- Vistas
- CDS Views
- Programas
- Reportes
- Clases
- Métodos
- Function Modules
- BAPIs
- BADIs
- User Exits
- Enhancements
- Estructuras
- Dominios
- Elementos de datos
- Objetos de customizing
- Tipos de movimiento
- Apps Fiori
- Roles
- Catálogos
- Servicios
- Interfaces
- Jobs
- Formularios
- SmartForms
- Adobe Forms
- Objetos Z/Y
- Otros objetos SAP verificables

La plantilla debe ser suficientemente genérica para soportar estos tipos sin obligar a incluir información que no aplique.

==================================================
PRINCIPIO FUNDAMENTAL
==================================================

La documentación de un objeto SAP debe representar CONOCIMIENTO CONFIRMADO.

No debe utilizarse esta plantilla para registrar suposiciones.

Regla:

OBJETO IDENTIFICADO
→ DATOS CONFIRMADOS
→ PROPÓSITO
→ RELACIONES
→ USO
→ EVIDENCIA
→ DOCUMENTACIÓN RELACIONADA

Nunca:

"Probablemente existe..."
"Debería utilizar..."
"Seguramente actualiza..."

Si algo no está confirmado:

"NO CONFIRMADO"

o:

"PENDIENTE DE VALIDAR"

==================================================
METADATA
==================================================

El archivo debe comenzar obligatoriamente con YAML front matter:

---
object_id: ""
object_type: ""
object_name: ""
technical_name: ""
module: ""
version: "1.0"
status: "draft"
date: ""
author: ""
---

Luego:

# Objeto SAP

## Metadata

Utilizar una tabla:

| Campo | Valor |
|---|---|
| Object ID | |
| Tipo de objeto | |
| Nombre funcional | |
| Nombre técnico | |
| Módulo | |
| Versión | |
| Estado | |
| Fecha | |
| Autor | |

No inventar valores.

==================================================
OBJECT_ID
==================================================

Cada objeto debe poseer un identificador único dentro de la base de conocimiento.

Utilizar:

OBJ-0001
OBJ-0002
OBJ-0003

El identificador debe permanecer estable aunque cambie la documentación del objeto.

No utilizar el ticket_id como identificador del objeto.

Un mismo objeto puede estar relacionado con múltiples tickets.

==================================================
OBJECT_TYPE
==================================================

Registrar explícitamente el tipo de objeto.

Ejemplos:

- TRANSACTION
- TABLE
- VIEW
- CDS_VIEW
- PROGRAM
- CLASS
- METHOD
- FUNCTION_MODULE
- BAPI
- BADI
- USER_EXIT
- ENHANCEMENT
- STRUCTURE
- DOMAIN
- DATA_ELEMENT
- MOVEMENT_TYPE
- FIORI_APP
- ROLE
- CATALOG
- SERVICE
- INTERFACE
- JOB
- FORM
- SMARTFORM
- ADOBE_FORM
- CUSTOMIZING
- OTHER

Si el tipo no está confirmado:

"UNKNOWN"

No crear categorías innecesarias si el estándar SAP o el sistema no permiten confirmar el tipo.


==================================================
1. IDENTIFICACIÓN
==================================================

## 1. Identificación

Documentar:

- nombre funcional;
- nombre técnico;
- tipo de objeto;
- sistema cuando sea relevante;
- componente SAP cuando sea relevante;
- namespace cuando corresponda;
- objeto estándar o personalizado.

Utilizar:

ESTÁNDAR SAP
Z
Y
OTRO

No asumir que un objeto es estándar únicamente por su nombre.

Para objetos Z/Y, indicar que corresponde a desarrollo personalizado cuando haya evidencia.

==================================================
2. DESCRIPCIÓN
==================================================

## 2. Descripción

Explicar brevemente qué es el objeto.

La descripción debe responder:

¿Qué es?

Evitar explicaciones especulativas.

Separar:

- descripción confirmada;
- interpretación funcional.

==================================================
3. PROPÓSITO
==================================================

## 3. Propósito

Documentar para qué existe o se utiliza el objeto.

Responder:

¿Para qué sirve?

Cuando el propósito no esté confirmado:

"Propósito pendiente de validar."


==================================================
4. COMPORTAMIENTO
==================================================

## 4. Comportamiento

Documentar el comportamiento conocido del objeto.

Cuando corresponda:

- entradas;
- procesamiento;
- validaciones;
- salidas;
- actualizaciones;
- errores;
- dependencias.

No convertir esta sección en código técnico detallado salvo que sea necesario para comprender el objeto.

Distinguir claramente:

COMPORTAMIENTO CONFIRMADO

de:

COMPORTAMIENTO INFERIDO


==================================================
5. DATOS
==================================================

## 5. Datos

Documentar los datos relevantes relacionados con el objeto.

Cuando aplique:

- tablas;
- campos;
- estructuras;
- parámetros;
- documentos;
- claves;
- relaciones.

Utilizar tablas cuando sea útil.

Ejemplo de estructura:

| Elemento | Tipo | Descripción | Confirmación |
|---|---|---|---|

No inventar campos ni relaciones.


==================================================
6. RELACIONES CON OTROS OBJETOS
==================================================

## 6. Relaciones con otros objetos

Esta sección es crítica para la futura base de conocimiento.

Registrar relaciones confirmadas entre el objeto y otros objetos SAP.

Ejemplos:

- utiliza;
- llama;
- actualiza;
- lee;
- genera;
- depende de;
- es ejecutado por;
- pertenece a;
- integra con;
- precede;
- sucede después de.

Utilizar:

| ID | Objeto origen | Relación | Objeto destino | Evidencia |
|---|---|---|---|---|

Cuando otro objeto esté documentado en la base de conocimiento, utilizar su `object_id`.

Ejemplo conceptual:

OBJ-0001 → actualiza → OBJ-0020

No inventar relaciones.

==================================================
7. PROCESOS RELACIONADOS
==================================================

## 7. Procesos relacionados

Registrar los procesos SAP o procesos de negocio en los que participa el objeto.

Por ejemplo:

- inventario;
- compras;
- recepción;
- facturación;
- movimientos de mercancía;
- notas de crédito;
- devoluciones;
- contabilización.

No asumir que un objeto pertenece a un proceso únicamente por su módulo.

La relación debe estar sustentada por evidencia.


==================================================
8. MÓDULO SAP
==================================================

## 8. Módulo SAP

Registrar el módulo o componente funcional/técnico relacionado.

Ejemplos:

- MM
- FI
- SD
- WM
- EWM
- PP
- CO
- QM
- PM
- HCM
- BASIS
- ABAP
- Fiori/UI5

Un objeto puede estar relacionado con más de un módulo.

No limitar artificialmente la clasificación cuando exista integración entre módulos.


==================================================
9. CONFIGURACIÓN RELACIONADA
==================================================

## 9. Configuración relacionada

Registrar customizing o parámetros que afecten el comportamiento del objeto.

Cuando corresponda:

- tablas de customizing;
- transacciones de configuración;
- clases de valoración;
- tipos de movimiento;
- determinación de cuentas;
- organizaciones;
- centros;
- sociedades;
- parámetros;
- variantes.

Distinguir entre:

CONFIGURACIÓN CONFIRMADA

y:

CONFIGURACIÓN PENDIENTE DE VALIDAR.


==================================================
10. INTEGRACIONES
==================================================

## 10. Integraciones

Documentar integraciones con:

- otros módulos SAP;
- sistemas externos;
- APIs;
- middleware;
- EDI;
- servicios;
- interfaces;
- jobs;
- archivos.

Para cada integración:

| Sistema / Objeto | Tipo | Dirección | Descripción | Evidencia |
|---|---|---|---|---|

No inventar sistemas ni interfaces.


==================================================
11. USO FUNCIONAL
==================================================

## 11. Uso funcional

Explicar cómo utiliza el objeto un usuario o proceso funcional.

Debe responder:

- ¿Quién lo utiliza?
- ¿En qué contexto?
- ¿En qué proceso?
- ¿Cuándo se utiliza?
- ¿Qué resultado funcional produce?

Cuando no se conozca:

"Información pendiente de validar."


==================================================
12. USO TÉCNICO
==================================================

## 12. Uso técnico

Documentar información técnica relevante cuando esté confirmada.

Puede incluir:

- programas que lo utilizan;
- funciones;
- clases;
- métodos;
- estructuras;
- tablas;
- APIs;
- servicios;
- jobs.

No convertir esta sección en documentación completa de desarrollo.

Para documentación detallada de código debe existir documentación técnica específica.


==================================================
13. REGLAS DE NEGOCIO RELACIONADAS
==================================================

## 13. Reglas de negocio relacionadas

Registrar reglas de negocio conocidas que estén asociadas al objeto.

Utilizar identificadores:

RN-OBJ-01
RN-OBJ-02

Cada regla debe indicar su fuente o evidencia.

No inventar reglas de negocio.


==================================================
14. EVIDENCIAS
==================================================

## 14. Evidencias

Registrar las evidencias que sustentan la documentación.

Utilizar:

EVID-OBJ-01
EVID-OBJ-02

Las evidencias pueden provenir de:

- sistema SAP;
- documentación oficial;
- código;
- configuración;
- pruebas;
- debug;
- tickets;
- investigaciones;
- análisis;
- documentación interna.

Utilizar una tabla:

| ID | Tipo | Referencia | Qué demuestra |
|---|---|---|---|

No almacenar secretos ni información sensible.


==================================================
15. DOCUMENTACIÓN RELACIONADA
==================================================

## 15. Documentación relacionada

Relacionar el objeto con:

- requirements;
- functional specifications;
- functional tests;
- analysis;
- debug;
- investigation;
- tickets;
- otros objetos SAP.

Cuando exista ticket_id, conservarlo como referencia transversal.

No convertir ticket_id en sustituto de object_id.


==================================================
16. ESTADO DEL CONOCIMIENTO
==================================================

## 16. Estado del conocimiento

Indicar el nivel de certeza del conocimiento documentado.

Utilizar:

- CONFIRMADO
- PARCIAL
- EN VALIDACIÓN
- NO CONFIRMADO

También puede indicarse el alcance:

- FUNCIONAL
- TÉCNICO
- CONFIGURACIÓN
- INTEGRACIÓN

No utilizar "CONFIRMADO" cuando solamente exista una hipótesis.


==================================================
17. INFORMACIÓN PENDIENTE
==================================================

## 17. Información pendiente

Registrar información que todavía debe investigarse o validarse.

Utilizar:

PEND-OBJ-01
PEND-OBJ-02

Para cada elemento:

| ID | Información pendiente | Motivo | Acción requerida |
|---|---|---|---|

Si no existe información pendiente:

"N/A"


==================================================
REGLAS DE OBJETOS SAP
==================================================

La plantilla debe aplicar estas reglas:

1. Nunca inventar objetos SAP.
2. Nunca inventar nombres técnicos.
3. Nunca inventar relaciones.
4. Nunca inventar tablas o campos.
5. Nunca asumir que un objeto Z tiene comportamiento estándar SAP.
6. Diferenciar estándar SAP de desarrollo personalizado.
7. Mantener exactamente los nombres técnicos confirmados.
8. Registrar incertidumbre explícitamente.
9. Mantener evidencia para afirmaciones relevantes.
10. Permitir múltiples módulos por objeto.
11. Permitir múltiples procesos relacionados.
12. Permitir múltiples relaciones entre objetos.


==================================================
OBJETOS ESTÁNDAR VS OBJETOS PERSONALIZADOS
==================================================

La documentación debe distinguir:

STANDARD

Objeto entregado por SAP.

CUSTOM

Objeto desarrollado o configurado por la organización.

UNKNOWN

No se pudo confirmar su origen.

Nunca clasificar como STANDARD solamente porque el nombre parezca estándar.

Para objetos Z o Y, clasificarlos como personalizados cuando el origen esté confirmado.


==================================================
RELACIONES ENTRE OBJETOS
==================================================

Las relaciones deben ser tratadas como conocimiento independiente.

Ejemplo conceptual:

OBJ-0010
Tipo: TRANSACTION
Nombre: [objeto]

RELACIÓN:

OBJ-0010
→ ejecuta →
OBJ-0020

Esta relación debe poder ser utilizada posteriormente por el agente para responder preguntas como:

- ¿Qué objetos intervienen en este proceso?
- ¿Qué programa ejecuta esta transacción?
- ¿Qué tablas utiliza este desarrollo?
- ¿Qué objetos están relacionados con este movimiento?
- ¿Qué integraciones existen?
- ¿Qué documentos dependen de este objeto?

No crear relaciones sin evidencia.


==================================================
TICKET_ID
==================================================

El conocimiento de un objeto puede originarse a partir de múltiples tickets.

Por lo tanto:

object_id = identidad del objeto

ticket_id = contexto donde fue investigado, utilizado o documentado

No mezclar ambos conceptos.

Si un objeto aparece en varios tickets, registrar las relaciones correspondientes en documentación relacionada o referencias.


==================================================
SEGURIDAD
==================================================

La plantilla debe cumplir:

standards/security-standard.md

Nunca almacenar:

- contraseñas;
- tokens;
- API keys;
- credenciales;
- claves privadas;
- secretos;
- información personal innecesaria.

Las evidencias deben sanitizarse.

Los nombres técnicos SAP pueden conservarse cuando sean necesarios para el conocimiento funcional o técnico.


==================================================
VERSIONADO
==================================================

Utilizar:

version: "1.0"

Aplicar:

PATCH:
Correcciones editoriales.

MINOR:
Información adicional que no modifica sustancialmente el conocimiento existente.

MAJOR:
Cambio significativo en la descripción, comportamiento, relaciones o clasificación del objeto.

No sobrescribir silenciosamente información anterior.


==================================================
PREPARACIÓN PARA IA
==================================================

La estructura debe estar optimizada para recuperación de conocimiento por un agente de IA.

El agente debe poder responder posteriormente preguntas como:

- ¿Qué es este objeto?
- ¿Para qué sirve?
- ¿A qué módulo pertenece?
- ¿Qué procesos utiliza?
- ¿Qué tablas están relacionadas?
- ¿Qué programas o funciones intervienen?
- ¿Qué objetos lo llaman?
- ¿Qué objetos actualiza?
- ¿Qué configuración afecta su comportamiento?
- ¿Qué integraciones tiene?
- ¿Qué documentación existe sobre él?
- ¿Qué información todavía no está confirmada?

Por esta razón:

- utilizar nombres técnicos exactos;
- mantener identificadores estables;
- evitar texto ambiguo;
- registrar relaciones explícitas;
- separar hechos de inferencias;
- mantener evidencias;
- evitar información duplicada innecesariamente.


==================================================
REGLAS PARA EL AGENTE QUE COMPLETE LA PLANTILLA
==================================================

El agente debe:

1. Buscar primero si el objeto ya existe en la base de conocimiento.
2. Evitar crear duplicados.
3. Reutilizar el object_id existente.
4. Actualizar el objeto existente cuando corresponda.
5. No crear un nuevo objeto solamente porque aparece en otro ticket.
6. Mantener las relaciones existentes.
7. Agregar nuevas evidencias cuando estén disponibles.
8. Marcar contradicciones.
9. No eliminar conocimiento confirmado sin justificación.
10. Mantener historial mediante Git.
11. No inventar información faltante.
12. Registrar explícitamente lo que requiere validación.


==================================================
FORMATO FINAL
==================================================

El archivo final debe ser una plantilla Markdown limpia y reutilizable.

Debe contener:

1. YAML front matter.
2. Título "# Objeto SAP".
3. Metadata.
4. Las 17 secciones definidas.
5. Tablas donde aporten estructura.
6. Identificadores consistentes.
7. Comentarios HTML breves para orientar al usuario.
8. Ningún dato ficticio.
9. Ningún objeto SAP inventado.
10. Ninguna relación inventada.
11. Compatibilidad con los standards existentes.
12. Compatibilidad con los templates existentes.

No agregues secciones adicionales fuera de las definidas.

No generes objetos SAP de ejemplo.

No expliques el proceso de creación.

Entrega únicamente el contenido final que debe guardarse en:

knowledge/sap-objects/object.md
