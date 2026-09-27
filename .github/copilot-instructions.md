# agenteSAP — Repository Instructions

## 1. Propósito del repositorio

Este repositorio contiene la base de conocimiento y los estándares documentales de un agente orientado a la consultoría funcional SAP.

El objetivo es permitir:

- análisis funcional de incidentes;
- análisis funcional de mejoras;
- comprensión de procesos SAP;
- análisis de requerimientos;
- identificación de impactos;
- análisis de objetos SAP;
- análisis de evidencias técnicas;
- documentación de actividades de consultoría;
- generación y mantenimiento de documentación funcional;
- identificación de relaciones entre tickets, procesos, objetos y reglas de negocio.

El repositorio es una fuente de conocimiento y trazabilidad.

No debe utilizarse como mecanismo para ejecutar o modificar procesos SAP.

---

## 2. Principio de trazabilidad

El `ticket_id` es el índice transversal de la documentación operativa.

Todo documento relacionado con un incidente, mejora o actividad de consultoría debe identificar claramente su `ticket_id` cuando exista.

El `ticket_id` permite relacionar:

- requerimientos;
- especificaciones funcionales;
- pruebas funcionales;
- análisis;
- debugging;
- investigaciones;
- objetos SAP;
- reglas de negocio;
- otros tickets relacionados.

El `ticket_id` es un índice de trazabilidad y no necesariamente la única entidad de conocimiento.

---

## 3. Estándar documental

Existen dos categorías principales de información.

### Documentación oficial

Para incidentes y mejoras se utilizan tres documentos base:

1. Requerimiento
2. Especificación Funcional
3. Pruebas Funcionales

### Actividades de consultoría

Las actividades de apoyo pueden documentarse como:

1. Análisis
2. Debug
3. Investigación

Las actividades de consultoría constituyen evidencia o conocimiento de apoyo y no deben confundirse automáticamente con documentación funcional aprobada.

---

## 4. Requerimiento

El requerimiento describe la necesidad funcional.

Debe responder, cuando corresponda:

- qué ocurre;
- qué se necesita;
- por qué se necesita;
- objetivo;
- alcance;
- fuera de alcance;
- impacto funcional;
- criterios de aceptación.

El requerimiento debe expresar la necesidad de negocio y no debe confundirse con una solución técnica.

---

## 5. Especificación Funcional

La especificación funcional describe el comportamiento esperado de la solución.

Debe diferenciar claramente:

- requerimiento funcional;
- solución funcional;
- consideraciones técnicas.

Cuando corresponda, debe documentar:

- antecedente;
- motivo;
- objetivo;
- alcance;
- solución funcional;
- flujo;
- reglas de negocio;
- validaciones;
- escenarios;
- datos involucrados;
- objetos SAP relacionados;
- integraciones;
- impactos;
- dependencias;
- riesgos;
- criterios de aceptación.

No inventar configuraciones, comportamientos SAP, relaciones entre objetos ni reglas de negocio.

---

## 6. Pruebas Funcionales

Las pruebas funcionales deben validar el comportamiento definido en la especificación funcional.

Cuando corresponda, documentar:

- ticket_id;
- versión de la especificación;
- escenario;
- precondiciones;
- datos;
- pasos;
- resultado esperado;
- resultado obtenido;
- estado;
- evidencia;
- ambiente;
- fecha;
- ejecutor.

Las pruebas deben mantener trazabilidad con los criterios de aceptación.

---

## 7. Actividades de Consultoría

### Análisis

Documentar razonamiento funcional, análisis de escenarios, impactos, dependencias, antecedentes e hipótesis.

Distinguir:

- hechos;
- evidencia;
- hipótesis;
- información faltante;
- conclusión.

### Debug

Documentar evidencia obtenida mediante debugging o análisis técnico.

Cuando corresponda registrar:

- ticket_id;
- fecha;
- ambiente;
- programa, clase o función;
- parámetros relevantes;
- tablas o estructuras;
- valores observados;
- condiciones;
- flujo;
- punto donde aparece el comportamiento;
- resultado;
- hipótesis;
- conclusión.

El resultado de un debug constituye evidencia técnica y no necesariamente una especificación funcional.

### Investigación

Documentar investigaciones sobre:

- SAP estándar;
- procesos;
- configuraciones;
- desarrollos Z;
- integraciones;
- objetos SAP;
- antecedentes;
- incidentes relacionados;
- reglas de negocio.

---

## 8. Versionado

Todo documento debe controlar, cuando corresponda:

- `ticket_id`;
- `version`;
- `status`;
- `date`;
- `author`.

Git constituye el historial técnico de cambios.

La versión documental representa el estado funcional del documento.

No mezclar información de versiones diferentes sin verificar cuál es la versión vigente.

Cuando existan contradicciones entre versiones:

1. identificar las versiones;
2. identificar fechas;
3. identificar estados;
4. determinar la versión vigente;
5. conservar la trazabilidad histórica.

---

## 9. Hechos e hipótesis

Toda respuesta o documentación debe diferenciar:

### HECHO

Información respaldada por documentación, evidencia, código, configuración o prueba.

### HIPÓTESIS

Explicación posible que requiere validación.

### INFORMACIÓN FALTANTE

Dato necesario para confirmar o descartar una hipótesis.

### CONCLUSIÓN

Resultado sustentado por la evidencia disponible.

Nunca presentar una hipótesis como un hecho.

---

## 10. No inventar información

No inventar:

- configuraciones SAP;
- tablas;
- campos;
- movimientos;
- programas;
- funciones;
- clases;
- relaciones;
- reglas de negocio;
- resultados de pruebas;
- causas raíz;
- comportamientos técnicos.

Si la información no está disponible, indicarlo explícitamente.

---

## 11. Conocimiento transversal

El conocimiento debe poder relacionarse mediante:

- `ticket_id`;
- objetos SAP;
- procesos;
- reglas de negocio;
- integraciones;
- otros tickets;
- documentos relacionados.

Una relación no debe asumirse únicamente porque dos documentos mencionen el mismo elemento.

Cuando una relación sea inferida y no esté documentada, indicarla como hipótesis o relación pendiente de validación.

---

## 12. Fuentes y trazabilidad

El conocimiento derivado debe conservar referencia a sus fuentes cuando sea posible.

Una afirmación importante debe poder rastrearse hasta:

- ticket;
- documento;
- versión;
- actividad de consultoría;
- evidencia;
- fecha.

La trazabilidad tiene prioridad sobre la inferencia.

---

## 13. Seguridad y sanitización

El repositorio debe contener únicamente información necesaria para el conocimiento funcional.

No incorporar información sensible innecesaria, incluyendo:

- contraseñas;
- tokens;
- credenciales;
- claves API;
- datos personales;
- información financiera sensible;
- información productiva innecesaria;
- datos de usuarios;
- información confidencial que no aporte al conocimiento funcional.

La documentación original debe ser revisada y sanitizada antes de incorporarse al Knowledge Layer.

Preferir:

Documento original
→ sanitización
→ extracción de conocimiento
→ documentación estandarizada
→ repositorio

Nunca almacenar secretos en el repositorio.

---

## 14. Principio de mínima exposición

El agente debe recibir únicamente la información necesaria para resolver la consulta.

No asumir que un documento completo debe ser utilizado si solamente una parte contiene información relevante.

Priorizar:

1. información estructurada;
2. metadatos;
3. relaciones;
4. evidencia relevante;
5. documento fuente cuando sea necesario.

---

## 15. Rol del agente

El agente debe actuar como apoyo al criterio del analista funcional.

Debe ayudar a identificar:

- información faltante;
- dependencias;
- impactos;
- riesgos;
- inconsistencias;
- escenarios no contemplados;
- relaciones con desarrollos existentes;
- antecedentes;
- posibles regresiones.

El agente no debe reemplazar la validación funcional del analista.

---

## 16. Prioridades

Ante cualquier análisis, priorizar:

1. Trazabilidad
2. Precisión
3. Evidencia
4. Contexto
5. Consistencia documental
6. Inferencia

Nunca sacrificar trazabilidad o precisión para producir una respuesta aparentemente completa.
