Actúa como consultor funcional SAP senior, arquitecto de conocimiento y especialista en análisis de incidentes, problemas funcionales y documentación de razonamiento para sistemas empresariales y agentes de IA.

Tu tarea es generar ÚNICAMENTE el archivo:

templates/analysis.md

Este archivo será el TEMPLATE OFICIAL para documentos de tipo:

document_type: analysis

del repositorio `agenteSAP`.

==================================================
1. ESTÁNDARES OBLIGATORIOS
==================================================

El template debe cumplir y ser compatible con:

- standards/documentation-standard.md
- standards/versioning-standard.md
- standards/security-standard.md

Estos documentos son normativos.

No debes redefinir sus reglas ni contradecirlas.

La responsabilidad de este archivo es únicamente definir la estructura práctica para documentar análisis funcionales SAP.

Diferencia de responsabilidades:

documentation-standard.md
→ Define las reglas generales de documentación.

versioning-standard.md
→ Define cómo evolucionan y se versionan los documentos.

security-standard.md
→ Define cómo se protege y sanitiza la información.

templates/analysis.md
→ Define la estructura que debe utilizar un análisis funcional.

==================================================
2. OBJETIVO
==================================================

El template debe permitir documentar de manera estructurada el razonamiento realizado durante un análisis funcional.

Debe permitir reconstruir:

- qué se intentaba analizar;
- cuál era el contexto;
- qué información estaba disponible;
- qué hechos fueron identificados;
- qué evidencia fue encontrada;
- qué análisis se realizó;
- qué hipótesis surgieron;
- qué información faltaba;
- qué impactos fueron identificados;
- qué dependencias existen;
- qué conclusión se obtuvo;
- qué próximos pasos quedaron definidos.

El análisis debe preservar el razonamiento y no solamente el resultado final.

==================================================
3. PRINCIPIO FUNDAMENTAL
==================================================

El análisis debe seguir la cadena:

PREGUNTA
↓
CONTEXTO
↓
INFORMACIÓN DISPONIBLE
↓
HECHOS
↓
EVIDENCIA
↓
ANÁLISIS
↓
HIPÓTESIS
↓
VALIDACIÓN
↓
CONCLUSIÓN
↓
PRÓXIMOS PASOS

El agente NO debe saltar directamente de:

"se reportó un problema"

a:

"la causa es X"

sin documentar la evidencia y el razonamiento que sustentan esa conclusión.

==================================================
4. PROPÓSITO DEL ANÁLISIS
==================================================

Un análisis puede utilizarse para:

- investigar un incidente;
- comprender un comportamiento SAP;
- analizar datos;
- estudiar un proceso;
- evaluar una inconsistencia;
- identificar impactos;
- determinar una posible causa;
- preparar una especificación funcional;
- evaluar una solución;
- analizar documentación existente;
- preparar una sesión de debug;
- interpretar resultados de debug;
- analizar un desarrollo Z;
- investigar una integración.

El template debe ser suficientemente flexible para todos estos escenarios sin inventar información.

==================================================
5. METADATA
==================================================

El documento generado mediante este template debe comenzar exactamente con:

---
ticket_id: ""
document_type: "analysis"
version: "1.0"
status: "draft"
date: ""
author: ""
---

Estos campos son obligatorios según:

standards/documentation-standard.md

Si no existe un ticket:

ticket_id: "N/A"

No inventar valores.

==================================================
6. ESTRUCTURA OBLIGATORIA
==================================================

Después del Front Matter, utilizar exactamente:

# Análisis

## Metadata

## 1. Objetivo del análisis

## 2. Contexto

## 3. Información disponible

## 4. Hechos identificados

## 5. Evidencias

## 6. Análisis funcional

## 7. Hipótesis

## 8. Información faltante

## 9. Impactos identificados

## 10. Dependencias

## 11. Conclusión

## 12. Próximos pasos

## 13. Documentación relacionada

No agregar secciones adicionales salvo que el estándar de documentación sea posteriormente modificado.

==================================================
7. METADATA VISIBLE
==================================================

La sección:

## Metadata

debe representar de forma legible el Front Matter.

Utilizar:

| Campo | Valor |
|---|---|
| Ticket ID | |
| Tipo de documento | analysis |
| Versión | 1.0 |
| Estado | draft |
| Fecha | |
| Autor | |

La metadata visible y el Front Matter deben permanecer consistentes.

==================================================
8. OBJETIVO DEL ANÁLISIS
==================================================

## 1. Objetivo del análisis

Debe describir qué pregunta o problema intenta resolver el análisis.

Debe ser concreto.

Ejemplos conceptuales:

- Determinar por qué una funcionalidad no genera el resultado esperado.
- Analizar el comportamiento de un documento SAP.
- Identificar el origen de una inconsistencia.
- Evaluar el impacto funcional de un cambio.

No definir una conclusión antes de realizar el análisis.

Utilizar:

<!-- Indicar qué se busca determinar o comprender mediante este análisis. -->

==================================================
9. CONTEXTO
==================================================

## 2. Contexto

Debe describir las circunstancias que originaron el análisis.

Puede incluir:

- ticket;
- incidente;
- proceso;
- usuario;
- área;
- ambiente;
- funcionalidad;
- documentos involucrados;
- antecedentes;
- cambios recientes.

Debe responder:

"¿Por qué este análisis es necesario?"

Utilizar:

<!-- Describir el contexto que originó el análisis y los antecedentes relevantes. -->

==================================================
10. INFORMACIÓN DISPONIBLE
==================================================

## 3. Información disponible

Debe registrar qué información estaba disponible al comenzar el análisis.

Puede incluir:

- descripción del usuario;
- documentos SAP;
- consultas;
- resultados de reportes;
- screenshots;
- logs;
- código;
- configuraciones;
- documentación;
- resultados previos;
- datos maestros;
- documentos relacionados.

Utilizar:

### Información recibida

-

### Documentos analizados

-

### Datos disponibles

-

### Fuentes disponibles

-

No asumir que toda información recibida constituye un hecho confirmado.

==================================================
11. HECHOS IDENTIFICADOS
==================================================

## 4. Hechos identificados

Debe registrar únicamente información confirmada.

Cada hecho debe ser concreto y, cuando sea posible, trazable a una evidencia.

Utilizar:

### HECHO-01

Descripción:

Fuente / evidencia:

### HECHO-02

Descripción:

Fuente / evidencia:

No incluir interpretaciones en esta sección.

Un hecho debe responder:

"¿Qué sabemos que ocurrió o existe?"

==================================================
12. EVIDENCIAS
==================================================

## 5. Evidencias

Debe documentar la evidencia utilizada para sustentar el análisis.

Puede incluir:

- resultado de una consulta;
- documento SAP;
- resultado de debug;
- código;
- tabla;
- log;
- screenshot;
- configuración;
- documentación oficial;
- prueba funcional;
- comportamiento reproducido.

Utilizar:

### EVID-01

Tipo:

Fuente:

Descripción:

Referencia:

### EVID-02

Tipo:

Fuente:

Descripción:

Referencia:

La evidencia debe permitir comprender de dónde surge cada conclusión relevante.

No inventar evidencias.

==================================================
13. ANÁLISIS FUNCIONAL
==================================================

## 6. Análisis funcional

Esta es la sección principal del razonamiento.

Debe explicar cómo se interpretó la información disponible.

Debe poder responder:

- ¿Qué comportamiento se observó?
- ¿Cómo debería comportarse?
- ¿Cuál es la diferencia?
- ¿Qué elementos intervienen?
- ¿Qué relaciones se identificaron?
- ¿Qué reglas pueden estar involucradas?
- ¿Qué escenarios fueron considerados?
- ¿Qué información respalda cada interpretación?

Utilizar una estructura clara.

### Observación

Descripción:

### Análisis

Descripción:

### Relación identificada

Descripción:

### Interpretación

Descripción:

No presentar una interpretación como causa confirmada si todavía es una hipótesis.

==================================================
14. HIPÓTESIS
==================================================

## 7. Hipótesis

Debe registrar explicaciones posibles que todavía no fueron confirmadas.

Cada hipótesis debe tener un identificador.

Utilizar:

### HIP-01

**Hipótesis:**

**Evidencia que la sustenta:**

**Evidencia que la contradice:**

**Validación requerida:**

**Estado:**
- Pendiente
- Confirmada
- Descartada

### HIP-02

**Hipótesis:**

**Evidencia que la sustenta:**

**Evidencia que la contradice:**

**Validación requerida:**

**Estado:**
- Pendiente
- Confirmada
- Descartada

No marcar una hipótesis como confirmada sin evidencia suficiente.

==================================================
15. INFORMACIÓN FALTANTE
==================================================

## 8. Información faltante

Debe registrar la información necesaria para completar o confirmar el análisis.

Utilizar:

### INFO-01

Información faltante:

¿Por qué es necesaria?

¿Cómo obtenerla?

### INFO-02

Información faltante:

¿Por qué es necesaria?

¿Cómo obtenerla?

Ejemplos de información faltante pueden ser:

- resultado de debug;
- documento SAP;
- configuración;
- dato maestro;
- resultado de prueba;
- log;
- confirmación funcional;
- comportamiento en otro ambiente.

No inventar información faltante.

==================================================
16. IMPACTOS IDENTIFICADOS
==================================================

## 9. Impactos identificados

Debe documentar los impactos detectados durante el análisis.

Considerar:

- proceso;
- subproceso;
- usuarios;
- áreas;
- documentos;
- datos;
- integraciones;
- reportes;
- procesos posteriores;
- objetos SAP;
- reglas de negocio.

Utilizar:

### Procesos afectados

-

### Usuarios / áreas afectadas

-

### Datos / documentos afectados

-

### Integraciones afectadas

-

### Procesos posteriores

-

### Otros impactos

-

Diferenciar:

IMPACTO CONFIRMADO

de

IMPACTO POTENCIAL.

==================================================
17. DEPENDENCIAS
==================================================

## 10. Dependencias

Debe registrar elementos de los que depende el análisis o su validación.

Puede incluir:

- disponibilidad de ambientes;
- acceso a datos;
- disponibilidad de usuarios;
- desarrollos;
- configuraciones;
- interfaces;
- documentos;
- equipos técnicos;
- otros análisis.

Utilizar:

### DEP-01

**Dependencia:**

**Descripción:**

**Impacto:**

### DEP-02

**Dependencia:**

**Descripción:**

**Impacto:**

No inventar dependencias.

==================================================
18. CONCLUSIÓN
==================================================

## 11. Conclusión

Debe presentar el resultado del análisis.

La conclusión debe responder la pregunta planteada en:

## 1. Objetivo del análisis

Debe distinguir:

### Conclusión confirmada

-

### Conclusión inferida

-

### Conclusión pendiente

-

Una conclusión confirmada debe estar respaldada por evidencia suficiente.

Una conclusión inferida debe indicar que se trata de una inferencia.

Si no existe evidencia suficiente:

"No se puede determinar la causa con la información disponible."

No forzar una conclusión.

==================================================
19. PRÓXIMOS PASOS
==================================================

## 12. Próximos pasos

Debe identificar acciones necesarias después del análisis.

Puede incluir:

- ejecutar debug;
- realizar prueba;
- consultar configuración;
- solicitar información;
- validar con negocio;
- analizar código;
- revisar integración;
- crear especificación funcional;
- corregir documentación;
- generar ticket;
- realizar regresión.

Utilizar:

### Acción 01

Descripción:

Responsable:

Dependencia:

### Acción 02

Descripción:

Responsable:

Dependencia:

No asignar responsables ficticios.

==================================================
20. DOCUMENTACIÓN RELACIONADA
==================================================

## 13. Documentación relacionada

Debe permitir conectar el análisis con conocimiento existente.

Utilizar:

### Tickets relacionados

-

### Requerimientos relacionados

-

### Especificaciones funcionales relacionadas

-

### Pruebas funcionales relacionadas

-

### Debug relacionados

-

### Investigaciones relacionadas

-

### Procesos relacionados

-

### Objetos SAP relacionados

-

No inventar referencias.

==================================================
21. TRAZABILIDAD DEL RAZONAMIENTO
==================================================

El análisis debe mantener una relación clara entre:

HECHO
↓
EVIDENCIA
↓
ANÁLISIS
↓
HIPÓTESIS
↓
VALIDACIÓN
↓
CONCLUSIÓN

Cuando una conclusión derive de múltiples evidencias, indicarlas.

Ejemplo:

Conclusión:
La hipótesis HIP-01 queda confirmada.

Evidencias:
- EVID-01
- EVID-03

No permitir conclusiones sin base identificable.

==================================================
22. DISTINCIÓN ENTRE SÍNTOMA Y CAUSA
==================================================

El análisis debe diferenciar:

SÍNTOMA
→ comportamiento observado.

CAUSA
→ condición que explica el comportamiento.

No asumir que el síntoma es la causa.

Ejemplo conceptual:

Síntoma:
"El documento no aparece en el mosaico."

Hipótesis:
"El filtro de selección podría excluir el documento."

Causa confirmada:
"El criterio X excluye el documento bajo la condición Y."

La causa solamente debe marcarse como confirmada cuando exista evidencia suficiente.

==================================================
23. ANÁLISIS FUNCIONAL VS DEBUG
==================================================

Este documento puede registrar información proveniente de debug, pero no debe convertirse en un documento de debug.

Si existe una sesión de debug independiente:

referenciar:

Debug relacionado:
- ...

El análisis debe interpretar funcionalmente la información obtenida mediante debug.

El detalle técnico de la sesión de debug pertenece al template:

templates/debug.md

==================================================
24. ANÁLISIS FUNCIONAL VS INVESTIGACIÓN
==================================================

Una investigación busca información.

Un análisis interpreta información disponible para responder una pregunta o explicar un comportamiento.

Si se realizó una investigación independiente:

referenciarla.

No duplicar innecesariamente toda la investigación dentro del análisis.

==================================================
25. HECHOS, HIPÓTESIS E INFORMACIÓN FALTANTE
==================================================

Este principio es obligatorio.

Toda información relevante debe clasificarse cuando exista riesgo de confusión entre:

- hecho;
- hipótesis;
- inferencia;
- información faltante;
- conclusión.

Nunca presentar una hipótesis como hecho.

Nunca presentar una inferencia como conclusión confirmada sin indicar su carácter.

==================================================
26. REGLA CONTRA LA INVENCIÓN
==================================================

Si una información no está confirmada:

NO INVENTAR.

Utilizar:

- No confirmado.
- Información faltante.
- Pendiente de validación.
- Hipótesis.
- Requiere evidencia adicional.

Nunca inventar:

- objetos SAP;
- tablas;
- campos;
- programas;
- clases;
- funciones;
- transacciones;
- configuraciones;
- reglas;
- causas;
- datos;
- resultados;
- documentos;
- relaciones.

==================================================
27. SEGURIDAD
==================================================

El template debe cumplir:

standards/security-standard.md

No incorporar:

- contraseñas;
- tokens;
- API keys;
- credenciales;
- claves privadas;
- datos personales innecesarios;
- datos productivos innecesarios;
- información confidencial innecesaria.

Los datos técnicos SAP pueden conservarse cuando sean necesarios para la trazabilidad.

Las evidencias deben ser sanitizadas cuando corresponda.

==================================================
28. VERSIONADO
==================================================

El template debe cumplir:

standards/versioning-standard.md

La versión inicial será:

version: "1.0"

Si el análisis cambia significativamente:

- actualizar la versión;
- documentar el cambio;
- preservar la trazabilidad histórica.

No modificar silenciosamente conclusiones históricas.

==================================================
29. USO POR EL AGENTE DE IA
==================================================

Cuando el agente utilice este template deberá:

1. Identificar la pregunta que debe responder.
2. Recuperar documentación relacionada.
3. Identificar el contexto.
4. Separar información disponible de hechos confirmados.
5. Registrar evidencia.
6. Analizar las relaciones relevantes.
7. Formular hipótesis cuando corresponda.
8. Identificar información faltante.
9. Evaluar impactos.
10. Identificar dependencias.
11. Formular una conclusión proporcional a la evidencia.
12. Identificar próximos pasos.
13. Relacionar el conocimiento generado con documentos existentes.
14. Aplicar las reglas de seguridad.
15. No inventar información.

El agente no debe buscar una conclusión previamente asumida.

Debe permitir que la evidencia determine la conclusión.

==================================================
30. PRINCIPIO DE EVIDENCIA
==================================================

La evidencia tiene prioridad sobre la interpretación.

El orden recomendado es:

EVIDENCIA
↓
HECHO
↓
ANÁLISIS
↓
HIPÓTESIS
↓
VALIDACIÓN
↓
CONCLUSIÓN

Cuando la evidencia sea insuficiente:

No forzar una conclusión.

==================================================
31. PRINCIPIO DE REUTILIZACIÓN
==================================================

Antes de iniciar un análisis, el agente debe buscar conocimiento existente relacionado con:

- ticket;
- síntoma;
- proceso;
- objeto SAP;
- transacción;
- tabla;
- programa;
- función;
- integración;
- regla de negocio;
- incidente similar.

Si existe un análisis anterior relevante:

- reutilizarlo;
- referenciarlo;
- identificar similitudes y diferencias;
- no asumir que ambos escenarios son idénticos.

==================================================
32. CRITERIO DE CALIDAD
==================================================

Un análisis completado mediante este template debe permitir que otro consultor comprenda:

- qué se investigó;
- por qué;
- qué información existía;
- qué se confirmó;
- qué evidencia se encontró;
- qué hipótesis fueron consideradas;
- qué información faltaba;
- qué impactos se identificaron;
- qué se concluyó;
- qué sigue pendiente.

El documento debe preservar el razonamiento suficiente para que otro consultor pueda continuar el análisis sin empezar desde cero.

==================================================
33. FORMATO FINAL
==================================================

El archivo generado debe comenzar exactamente con:

---
ticket_id: ""
document_type: "analysis"
version: "1.0"
status: "draft"
date: ""
author: ""
---

Después debe contener exactamente:

# Análisis

## Metadata

## 1. Objetivo del análisis

## 2. Contexto

## 3. Información disponible

## 4. Hechos identificados

## 5. Evidencias

## 6. Análisis funcional

## 7. Hipótesis

## 8. Información faltante

## 9. Impactos identificados

## 10. Dependencias

## 11. Conclusión

## 12. Próximos pasos

## 13. Documentación relacionada

Cada sección debe contener instrucciones breves mediante comentarios HTML y estructuras vacías listas para completar.

No incluir:

- tickets ficticios;
- usuarios ficticios;
- sociedades ficticias;
- centros ficticios;
- documentos ficticios;
- objetos SAP ficticios;
- causas ficticias;
- conclusiones ficticias;
- evidencias ficticias;
- datos ficticios.

El resultado debe ser un TEMPLATE, no un análisis de ejemplo.

==================================================
34. REGLA FINAL DE GENERACIÓN
==================================================

Genera ÚNICAMENTE:

templates/analysis.md

No generar otros templates.

No generar otros estándares.

No modificar otros archivos.

No generar documentación de ejemplo.

No incluir explicaciones fuera del archivo.

El resultado debe estar listo para incorporarse directamente al repositorio `agenteSAP`.
