Este archivo será el ESTÁNDAR MAESTRO DE CLASIFICACIÓN DEL KNOWLEDGE del repositorio `agenteSAP`.

==================================================
1. CONTEXTO
==================================================

El repositorio `agenteSAP` tiene como objetivo construir una base de conocimiento estructurada para un futuro agente de IA especializado en consultoría funcional SAP.

La arquitectura actual contiene:

standards/
templates/
knowledge/
tickets/
agent/

El Knowledge Base contiene conocimiento reutilizable sobre:

- objetos SAP;
- procesos;
- reglas de negocio;
- relaciones;
- fuentes.

El agente debe poder distinguir entre:

- conocimiento SAP estándar;
- conocimiento específico de la organización;
- conocimiento mixto;
- conocimiento cuyo origen todavía no fue confirmado.

Este estándar debe centralizar las taxonomías utilizadas por el resto del repositorio.

==================================================
2. OBJETIVO
==================================================

Definir los vocabularios controlados utilizados para clasificar:

- documentos;
- conocimiento;
- objetos SAP;
- procesos;
- reglas de negocio;
- relaciones;
- fuentes;
- alcance;
- nivel de certeza.

Este archivo será la única fuente normativa para estas clasificaciones.

Los demás archivos deben referenciar este estándar y no crear vocabularios alternativos incompatibles.

==================================================
3. PRINCIPIO FUNDAMENTAL
==================================================

La clasificación no debe basarse en intuición.

Debe basarse en evidencia disponible.

Cuando no exista evidencia suficiente:

utilizar:

unknown

Es preferible utilizar:

unknown

antes que inventar una clasificación.

==================================================
4. KNOWLEDGE_TYPE
==================================================

Definir exclusivamente los siguientes valores:

standard
custom
mixed
unknown

--------------------------------------------------
4.1 STANDARD
--------------------------------------------------

Representa conocimiento que describe comportamiento, funcionalidad, proceso, regla o característica proporcionada por SAP y respaldada por evidencia suficiente.

No debe utilizarse simplemente porque:

- el proceso ocurre dentro de SAP;
- el objeto tiene apariencia estándar;
- la transacción existe;
- el comportamiento parece conocido.

--------------------------------------------------
4.2 CUSTOM
--------------------------------------------------

Representa conocimiento específico de la organización.

Puede corresponder a:

- desarrollos Z/Y;
- integraciones propias;
- reglas internas;
- configuraciones específicas;
- extensiones;
- procesos propios;
- comportamiento implementado localmente.

--------------------------------------------------
4.3 MIXED
--------------------------------------------------

Representa conocimiento que combina de forma relevante:

- SAP Standard;
- configuración local;
- desarrollos custom;
- integraciones;
- reglas internas.

Ejemplo conceptual:

Un proceso puede utilizar una transacción SAP estándar, una configuración local y un desarrollo Z.

El proceso puede clasificarse como:

knowledge_type: mixed

--------------------------------------------------
4.4 UNKNOWN
--------------------------------------------------

Debe utilizarse cuando no existe evidencia suficiente para determinar si el conocimiento es:

- standard;
- custom;
- mixed.

Nunca reemplazar unknown por una suposición.

==================================================
5. KNOWLEDGE_SCOPE
==================================================

Definir exclusivamente:

global
organization
country
company
plant
process
project
ticket
unknown

--------------------------------------------------
5.1 GLOBAL
--------------------------------------------------

Conocimiento aplicable de manera general y no limitado a una organización específica.

--------------------------------------------------
5.2 ORGANIZATION
--------------------------------------------------

Conocimiento aplicable a una organización determinada.

--------------------------------------------------
5.3 COUNTRY
--------------------------------------------------

Conocimiento condicionado por un país.

Puede incluir:

- legislación;
- localización SAP;
- requisitos fiscales;
- procesos específicos del país.

--------------------------------------------------
5.4 COMPANY
--------------------------------------------------

Conocimiento aplicable a una sociedad, compañía o entidad empresarial específica.

--------------------------------------------------
5.5 PLANT
--------------------------------------------------

Conocimiento aplicable a un centro, planta o ubicación operativa específica.

--------------------------------------------------
5.6 PROCESS
--------------------------------------------------

Conocimiento cuyo alcance está limitado a un proceso determinado.

--------------------------------------------------
5.7 PROJECT
--------------------------------------------------

Conocimiento creado o válido dentro de un proyecto específico.

--------------------------------------------------
5.8 TICKET
--------------------------------------------------

Conocimiento estrictamente relacionado con un caso o ticket determinado y que todavía no debe considerarse conocimiento transversal.

--------------------------------------------------
5.9 UNKNOWN
--------------------------------------------------

El alcance todavía no está determinado.

==================================================
6. SAP OBJECT ORIGIN
==================================================

Para SAP Objects definir:

origin:

standard
custom
unknown

--------------------------------------------------
STANDARD
--------------------------------------------------

Objeto proporcionado por SAP.

--------------------------------------------------
CUSTOM
--------------------------------------------------

Objeto desarrollado específicamente por la organización.

--------------------------------------------------
UNKNOWN
--------------------------------------------------

No existe evidencia suficiente para determinar el origen.

No asumir que un objeto es estándar solamente por su nombre.

No asumir que un objeto es custom solamente porque participa en un proceso custom.

==================================================
7. SAP OBJECT IMPLEMENTATION_TYPE
==================================================

Definir:

standard
configuration
enhancement
z_development
integration
unknown

--------------------------------------------------
STANDARD
--------------------------------------------------

Funcionalidad SAP estándar sin evidencia de extensión o implementación específica.

--------------------------------------------------
CONFIGURATION
--------------------------------------------------

Comportamiento determinado o condicionado mediante configuración SAP.

--------------------------------------------------
ENHANCEMENT
--------------------------------------------------

Extensión de funcionalidad estándar mediante:

- BAdI;
- User Exit;
- Enhancement;
- mecanismo equivalente.

--------------------------------------------------
Z_DEVELOPMENT
--------------------------------------------------

Desarrollo personalizado identificado mediante evidencia.

--------------------------------------------------
INTEGRATION
--------------------------------------------------

Implementación cuya función principal consiste en integrar SAP con otro sistema.

--------------------------------------------------
UNKNOWN
--------------------------------------------------

No existe evidencia suficiente.

==================================================
8. SOURCE ORIGIN
==================================================

Para Sources definir:

internal
sap
external
system
unknown

==================================================
9. SOURCE TYPE
==================================================

Definir:

repository_file
sap_documentation
sap_system
configuration
abap_code
debug
ticket
analysis
investigation
functional_test
screenshot
log
query
external_documentation
other
unknown

==================================================
10. KNOWLEDGE CERTAINTY
==================================================

Definir:

confirmed
partial
under_validation
inferred
not_confirmed

--------------------------------------------------
CONFIRMED
--------------------------------------------------

Existe evidencia suficiente para sostener la afirmación.

--------------------------------------------------
PARTIAL
--------------------------------------------------

Existe evidencia, pero no cubre completamente el conocimiento.

--------------------------------------------------
UNDER_VALIDATION
--------------------------------------------------

La información está siendo validada.

--------------------------------------------------
INFERRED
--------------------------------------------------

La información es una inferencia basada en evidencia indirecta.

--------------------------------------------------
NOT_CONFIRMED
--------------------------------------------------

No existe evidencia suficiente para considerar la información confirmada.

==================================================
11. REGLAS DE CLASIFICACIÓN
==================================================

Aplicar obligatoriamente:

1. No inventar clasificaciones.
2. No utilizar el nombre de una transacción como única evidencia.
3. No utilizar el prefijo Z/Y como única evidencia absoluta.
4. No confundir configuración con desarrollo custom.
5. No confundir objeto estándar con proceso estándar.
6. Un proceso puede ser mixed.
7. Un documento puede ser mixed.
8. Un ticket puede ser mixed.
9. Un objeto estándar puede participar en una implementación custom.
10. Un objeto custom puede utilizar funcionalidad estándar.
11. Una relación puede ser custom aunque uno de los objetos sea estándar.
12. Un conocimiento local no debe generalizarse como conocimiento SAP estándar.
13. Utilizar unknown cuando no haya evidencia suficiente.
14. Mantener la trazabilidad hacia la evidencia.
15. No cambiar una clasificación confirmada sin justificar el cambio.

==================================================
12. PRIORIDAD DE EVIDENCIA
==================================================

Definir la siguiente jerarquía conceptual:

EVIDENCIA DIRECTA
>
DOCUMENTACIÓN SAP OFICIAL
>
CONFIGURACIÓN CONFIRMADA
>
CÓDIGO CONFIRMADO
>
PRUEBA FUNCIONAL
>
DOCUMENTACIÓN INTERNA
>
ANÁLISIS
>
INFERENCIA

La jerarquía no significa que una fuente inferior sea inválida.

Significa que debe evaluarse de acuerdo con su naturaleza y contexto.

==================================================
13. NO GENERALIZACIÓN
==================================================

El agente nunca debe transformar:

comportamiento observado en una implementación local

en:

comportamiento estándar SAP.

Ejemplo conceptual:

Un proceso puede utilizar:

SAP Standard
+
Configuración local
+
Desarrollo Z
+
Integración externa.

El proceso no debe describirse simplemente como:

"Proceso SAP Standard"

sin identificar los componentes custom.

==================================================
14. USO POR EL AGENTE
==================================================

El agente debe consultar este estándar antes de clasificar conocimiento.

Debe utilizar las clasificaciones para:

- filtrar resultados;
- comparar conocimiento;
- identificar alcance;
- separar standard de custom;
- detectar conocimiento mixto;
- identificar información no confirmada;
- evitar generalizaciones.

==================================================
15. COMPATIBILIDAD
==================================================

Este estándar debe ser utilizado por:

- standards/documentation-standard.md
- templates/requirement.md
- templates/functional-specification.md
- templates/functional-tests.md
- templates/analysis.md
- templates/debug.md
- templates/investigation.md
- knowledge/sap-objects/object.md
- knowledge/processes/process.md
- knowledge/business-rules/business-rules.md
- knowledge/relationships/relationships.md
- knowledge/sources/source.md
- tickets/ticket.md
- agent/agent.md
- promptMaestro

==================================================
16. REGLA FINAL
==================================================

La clasificación debe ayudar al agente a responder:

¿Qué es?
¿De dónde proviene?
¿Dónde aplica?
¿Qué tan confirmado está?
¿Es SAP Standard o implementación Custom?

Nunca debe utilizarse la clasificación para inventar conocimiento.

PRINCIPIO:

CLASIFICAR → CONTEXTUALIZAR → EVIDENCIAR → VALIDAR
