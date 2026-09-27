Actúa como arquitecto de conocimiento SAP.

Actualiza:

knowledge/sap-objects/object.md

Mantén toda la estructura existente y agrega una clasificación técnica formal para diferenciar SAP Standard de SAP Custom.

--------------------------------------------------
1. NUEVA METADATA
--------------------------------------------------

El YAML debe incorporar:

origin:
implementation_type:

La estructura debe quedar:

---
object_id: ""
object_type: ""
object_name: ""
technical_name: ""
module: ""
origin: ""
implementation_type: ""
version: "1.0"
status: "draft"
date: ""
author: ""
---

--------------------------------------------------
2. ORIGIN
--------------------------------------------------

Valores permitidos:

standard
custom
unknown

STANDARD

Objeto proporcionado por SAP.

CUSTOM

Objeto desarrollado o implementado específicamente por la organización.

UNKNOWN

No existe evidencia suficiente.

--------------------------------------------------
3. IMPLEMENTATION_TYPE
--------------------------------------------------

Valores permitidos:

standard
configuration
enhancement
z_development
integration
unknown

STANDARD

Funcionalidad SAP estándar sin evidencia de modificación específica.

CONFIGURATION

Comportamiento producido o condicionado mediante configuración SAP.

ENHANCEMENT

Extensión de funcionalidad estándar mediante enhancement, BAdI, exit u mecanismo equivalente.

Z_DEVELOPMENT

Desarrollo propio identificado mediante evidencia.

INTEGRATION

Objeto o componente cuya función principal es integrar SAP con otro sistema.

UNKNOWN

No existe evidencia suficiente.

--------------------------------------------------
4. REGLAS
--------------------------------------------------

No asumir que todo objeto Z/Y es custom únicamente por el prefijo.

Puede utilizarse como indicio.

La clasificación definitiva debe basarse en evidencia.

Nunca clasificar como STANDARD un objeto cuyo origen custom esté confirmado.

Nunca clasificar como CUSTOM un objeto estándar solamente porque haya sido configurado localmente.

Distinguir:

ORIGEN DEL OBJETO

de:

FORMA EN QUE ESTÁ IMPLEMENTADO.

--------------------------------------------------
5. EJEMPLOS CONCEPTUALES
--------------------------------------------------

MIGO:

origin: standard
implementation_type: standard

Una configuración estándar que afecta MIGO:

origin: standard
implementation_type: configuration

ZMM_IM_0002:

origin: custom
implementation_type: z_development

Una integración:

origin: custom
implementation_type: integration

No crear objetos reales adicionales.

--------------------------------------------------
6. KNOWLEDGE_SCOPE
--------------------------------------------------

Agregar:

knowledge_scope:

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

Explicar que indica el ámbito donde aplica el conocimiento documentado del objeto.

--------------------------------------------------
7. IA
--------------------------------------------------

El agente debe utilizar origin e implementation_type antes de afirmar que un comportamiento es SAP estándar.

Debe responder separando:

OBJETO STANDARD

OBJETO CUSTOM

CONFIGURACIÓN

ENHANCEMENT

DESARROLLO Z

INTEGRACIÓN

No inferir relaciones o comportamientos sin evidencia.

Entrega únicamente el contenido actualizado de:

knowledge/sap-objects/object.md
