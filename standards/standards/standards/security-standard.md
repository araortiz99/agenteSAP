
---

# Prompt 2 — `standards/security-standard.md`

```text
Actúa como arquitecto de seguridad de información, arquitecto de conocimiento, consultor funcional SAP senior y especialista en seguridad aplicada a repositorios Git/GitHub y documentación empresarial.

Tu tarea es generar el archivo:

standards/security-standard.md

Este archivo será el ESTÁNDAR MAESTRO DE SEGURIDAD Y SANITIZACIÓN del repositorio `agenteSAP`.

IMPORTANTE:

- No debes crear templates.
- No debes crear otros estándares.
- No debes modificar otros archivos.
- Debes generar únicamente el contenido completo de:
  standards/security-standard.md

Este estándar debe complementar:

standards/documentation-standard.md

y

standards/versioning-standard.md

No debe duplicar innecesariamente sus contenidos.

Su objetivo específico es definir qué información puede almacenarse, qué información debe protegerse, qué información debe sanitizarse, cómo debe tratarse la información sensible y qué controles debe aplicar un agente de IA antes de generar o modificar conocimiento.

==================================================
1. CONTEXTO
==================================================

El repositorio `agenteSAP` será utilizado como base de conocimiento para un futuro agente especializado en consultoría funcional SAP.

El repositorio puede contener:

- tickets;
- requerimientos;
- especificaciones;
- pruebas;
- análisis;
- debug;
- investigaciones;
- objetos SAP;
- tablas;
- programas;
- transacciones;
- configuraciones;
- procesos;
- reglas de negocio;
- evidencias;
- datos técnicos;
- información histórica.

Parte de esta información puede provenir de ambientes corporativos.

Por lo tanto, debe existir una política clara para evitar almacenar:

- credenciales;
- secretos;
- información personal innecesaria;
- información confidencial;
- datos productivos no requeridos;
- información que permita acceso indebido a sistemas.

El estándar debe priorizar:

SEGURIDAD
+
MÍNIMA EXPOSICIÓN
+
UTILIDAD FUNCIONAL
+
TRAZABILIDAD.

==================================================
2. OBJETIVO
==================================================

Definir reglas para:

- clasificación de información;
- sanitización;
- anonimización;
- protección de secretos;
- manejo de datos personales;
- manejo de información productiva;
- manejo de documentos SAP;
- manejo de evidencia;
- uso seguro de Git/GitHub;
- generación de contenido mediante IA;
- revisión de documentación antes de incorporarla al repositorio.

==================================================
3. PRINCIPIO FUNDAMENTAL
==================================================

Debe almacenarse solamente la información necesaria para cumplir el objetivo funcional o técnico del documento.

PRINCIPIO:

UTILIDAD NECESARIA
+
MÍNIMA EXPOSICIÓN
=
DOCUMENTACIÓN SEGURA

No debe almacenarse información sensible solamente porque esté disponible.

==================================================
4. CLASIFICACIÓN DE INFORMACIÓN
==================================================

La información debe clasificarse conceptualmente en:

### PÚBLICA

Información que puede divulgarse sin impacto relevante.

Ejemplos:

- documentación pública de SAP;
- conceptos generales;
- información técnica pública.

### INTERNA

Información relacionada con procesos internos pero sin sensibilidad crítica.

Ejemplos:

- procesos funcionales;
- estructuras documentales;
- reglas internas no sensibles;
- nombres técnicos SAP.

### CONFIDENCIAL

Información cuyo acceso debe limitarse.

Ejemplos:

- datos internos de negocio;
- información de proveedores;
- importes;
- configuraciones internas;
- información operativa.

### RESTRINGIDA

Información que nunca debe almacenarse directamente en el repositorio salvo mecanismos específicamente autorizados.

Ejemplos:

- credenciales;
- secretos;
- tokens;
- claves privadas;
- información financiera altamente sensible;
- datos personales sensibles.

==================================================
5. SECRETOS
==================================================

Está PROHIBIDO almacenar directamente:

- contraseñas;
- tokens;
- API keys;
- access tokens;
- refresh tokens;
- claves privadas;
- certificados privados;
- secretos de aplicaciones;
- credenciales SAP;
- credenciales de bases de datos;
- credenciales de APIs;
- cadenas de conexión con credenciales;
- cookies de autenticación;
- session tokens.

Ejemplo prohibido:

```text
password=xxxxx

API_KEY=xxxxx
Authorization: Bearer xxxxx

Nunca almacenar secretos reales aunque sean utilizados únicamente para pruebas.

==================================================
6. ARCHIVOS SENSIBLES

No deben incorporarse al repositorio archivos que contengan:

dumps productivos;
exportaciones completas de bases de datos;
listados masivos de clientes;
listados masivos de proveedores;
credenciales;
configuraciones secretas;
archivos de producción no sanitizados;
logs con información sensible;
archivos temporales que contengan secretos.

Antes de incorporar un archivo debe verificarse su contenido.

==================================================
7. DATOS PERSONALES

Debe evitarse almacenar innecesariamente:

nombres completos;
documentos de identidad;
teléfonos;
direcciones;
correos personales;
información bancaria;
información médica;
información privada;
identificadores personales.

Cuando el dato personal no sea necesario para comprender el problema, debe eliminarse o anonimizarse.

Ejemplo:

En lugar de:

Juan Pérez - CI 1234567 - juan.perez@empresa.com

utilizar:

Usuario de tienda

o:

Usuario funcional

cuando la identidad no sea relevante.

==================================================
8. DATOS SAP

Los identificadores técnicos SAP pueden conservarse cuando sean necesarios para comprender el problema.

Ejemplos:

transacciones;
tablas;
campos;
programas;
clases;
funciones;
objetos Z;
centros;
sociedades;
movimientos;
tipos de documento;
clases de documento;
documentos SAP.

Ejemplos:

ZMM_IM_0004
ZMMT_CONF_INV_MP
MB52
MIGO
MIRO
BKPF
BSEG
PY44

Estos datos no deben eliminarse automáticamente si su ausencia destruye la trazabilidad funcional.

==================================================
9. DOCUMENTOS SAP

Los números de documentos SAP pueden conservarse cuando sean necesarios para reproducir o analizar un escenario.

Sin embargo, deben evitarse cuando:

no aportan valor;
contienen información sensible;
el escenario puede documentarse mediante datos ficticios;
el documento pertenece a producción y no es necesario para el conocimiento reutilizable.

Cuando sea posible, utilizar ejemplos sanitizados.

==================================================
10. DATOS PRODUCTIVOS

Debe evitarse almacenar datos productivos reales cuando no sean necesarios.

Si un análisis requiere datos reales para explicar un incidente, conservar solamente los campos necesarios.

Ejemplo:

En lugar de almacenar una extracción completa de BSEG:

utilizar únicamente:

sociedad;
ejercicio;
documento;
posición;
cuenta;
importe si es necesario;
moneda;
campo relevante.

Eliminar información irrelevante.

==================================================
11. SANITIZACIÓN

La sanitización consiste en transformar información sensible para conservar su utilidad sin exponer datos innecesarios.

Ejemplos:

Juan Pérez
→ Usuario A
proveedor@empresa.com
→ proveedor@example
4500037613
→ Documento SAP de ejemplo

No alterar los identificadores técnicos que sean necesarios para reproducir el conocimiento.

==================================================
12. ANONIMIZACIÓN

Cuando una identidad no sea necesaria, reemplazarla por una referencia genérica.

Ejemplos:

Usuario 1
Usuario 2
Proveedor A
Proveedor B
Tienda A
Centro A

Debe mantenerse consistencia dentro del mismo documento.

Si "Proveedor A" representa al mismo proveedor en todo el documento, no cambiar arbitrariamente su nombre.

==================================================
13. DATOS FINANCIEROS

Los importes deben incluirse solamente cuando sean relevantes para:

análisis;
impacto;
pruebas;
conciliación;
validación.

Cuando el importe exacto no sea necesario, utilizar:

rangos;
valores aproximados;
datos ficticios;
ejemplos sanitizados.

No almacenar información financiera innecesaria.

==================================================
14. LOGS Y DEBUG

Los logs y resultados de debug deben revisarse antes de incorporarse.

Deben eliminarse:

passwords;
tokens;
cookies;
credenciales;
información personal;
información confidencial irrelevante.

Debe conservarse:

programa;
clase;
método;
función;
transacción;
parámetros relevantes;
valores necesarios;
comportamiento observado;
sy-subrc;
registros relevantes;
evidencia necesaria para la conclusión.
==================================================
15. CÓDIGO ABAP

El código puede almacenarse cuando sea necesario para el análisis.

Sin embargo, antes de incorporarlo debe verificarse que no contenga:

credenciales;
endpoints privados innecesarios;
tokens;
secretos;
claves;
información personal;
datos productivos incrustados.

El código funcional no debe modificarse solamente para ocultar información si esto destruye su valor analítico.

Cuando sea necesario, reemplazar únicamente los datos sensibles.

==================================================
16. INTEGRACIONES

Las integraciones pueden documentarse utilizando:

sistema origen;
sistema destino;
interfaz;
API;
middleware;
proceso;
formato;
flujo;
comportamiento.

No almacenar:

credenciales;
tokens;
secretos;
certificados;
URLs privadas con información de autenticación.

Cuando un endpoint sea sensible:

https://sistema-interno.example/api

puede representarse como:

Endpoint interno del sistema

si la URL exacta no es necesaria.

==================================================
17. CONFIGURACIÓN SAP

La configuración puede documentarse cuando sea funcionalmente necesaria.

Ejemplos:

movimientos;
clases de documento;
cuentas;
determinación;
parámetros;
reglas;
tablas de configuración.

Debe evitarse almacenar configuraciones completas cuando solamente una parte sea necesaria.

Documentar únicamente lo relevante para el conocimiento.

==================================================
18. GITHUB

El repositorio debe considerarse un sistema de almacenamiento potencialmente accesible por terceros según su configuración.

Por ello:

NO asumir que GitHub es un almacenamiento seguro para secretos.

Nunca utilizar el repositorio como almacén de:

passwords;
tokens;
claves privadas;
secretos;
credenciales.

Incluso si el repositorio es privado, debe aplicarse la misma disciplina.

==================================================
19. GIT HISTORY

Eliminar un secreto del archivo actual no significa necesariamente que haya desaparecido del historial Git.

Si accidentalmente se incorpora información sensible:

detener la propagación;
identificar el secreto;
revocar o rotar la credencial;
eliminar la exposición;
evaluar el historial Git;
realizar limpieza del historial cuando corresponda;
revisar clones, forks o copias afectadas.

La eliminación del archivo no debe considerarse suficiente si el secreto ya fue committeado.

==================================================
20. ARCHIVOS TEMPORALES

No incorporar automáticamente:

archivos temporales;
exports;
dumps;
logs completos;
archivos de prueba;
screenshots sin revisión;
archivos generados por herramientas;
archivos locales;
configuraciones de IDE.

Antes de hacer commit debe verificarse el contenido.

==================================================
21. SCREENSHOTS

Las capturas de pantalla pueden contener información sensible.

Antes de almacenarlas verificar:

usuarios;
correos;
documentos;
importes;
URLs;
tokens;
datos productivos;
información personal.

Si es necesario:

recortar;
ocultar;
anonimizar;
reemplazar;
eliminar la captura.
==================================================
22. EVIDENCIA

La seguridad no debe destruir la evidencia necesaria para el análisis.

Debe buscarse el equilibrio:

SEGURIDAD
vs.
TRAZABILIDAD

Cuando sea posible, conservar:

objeto;
campo;
comportamiento;
resultado;
estructura;
relación;
condición;

sin conservar datos sensibles innecesarios.

==================================================
23. GENERACIÓN MEDIANTE IA

Cuando un agente de IA genere documentación deberá verificar antes de guardar:

secretos;
credenciales;
datos personales;
información financiera;
datos productivos;
información confidencial;
endpoints sensibles;
información innecesaria.

La IA no debe reproducir automáticamente todo el contenido proporcionado por el usuario.

Debe seleccionar únicamente lo necesario para construir conocimiento seguro.

==================================================
24. REGLA DE NO COPIA CIEGA

Está prohibido incorporar automáticamente al repositorio:

conversaciones completas;
logs completos;
correos completos;
exports completos;
dumps;
archivos adjuntos completos;

sin revisar previamente su contenido.

El conocimiento debe ser extraído y estructurado.

No debe utilizarse el repositorio como depósito indiscriminado de información.

==================================================
25. REGLA DE MÍNIMA INFORMACIÓN

Para cada dato almacenado debe poder responderse:

"¿Este dato es necesario para comprender, reproducir o reutilizar el conocimiento?"

Si la respuesta es NO:

el dato debe eliminarse, anonimizarse o reemplazarse.

==================================================
26. INFORMACIÓN QUE DEBE CONSERVARSE

Debe conservarse cuando sea necesaria:

evidencia funcional;
comportamiento observado;
nombres técnicos SAP;
reglas de negocio;
relaciones;
estructura de procesos;
condiciones;
resultados;
errores;
mensajes;
objetos;
referencias;
datos mínimos de reproducción.
==================================================
27. INFORMACIÓN QUE DEBE ELIMINARSE

Debe eliminarse o sanitizarse cuando no sea necesaria:

contraseñas;
tokens;
API keys;
secretos;
información personal;
datos bancarios;
datos médicos;
credenciales;
cookies;
session IDs;
dumps;
información productiva irrelevante;
información confidencial sin utilidad funcional.
==================================================
28. INCIDENTES DE SEGURIDAD

Si se detecta que información sensible fue incorporada al repositorio:

NO asumir que simplemente borrarla resuelve el problema.

Debe:

identificar qué información fue expuesta;
determinar si sigue siendo válida;
revocar o rotar secretos cuando corresponda;
identificar commits afectados;
evaluar el alcance;
limpiar el repositorio cuando sea necesario;
revisar copias afectadas;
documentar el incidente según las políticas internas aplicables.

No incluir secretos reales en documentación de incidentes de seguridad.

==================================================
29. REVISIÓN ANTES DE COMMIT

Antes de realizar commit debe revisarse:

Secretos
¿Hay passwords?
¿Hay tokens?
¿Hay API keys?
¿Hay credenciales?
¿Hay claves privadas?
Datos personales
¿Hay nombres innecesarios?
¿Hay documentos personales?
¿Hay teléfonos?
¿Hay correos personales?
Datos productivos
¿Hay información que no sea necesaria?
¿Hay exports completos?
¿Hay datos masivos?
SAP
¿Los objetos técnicos son necesarios?
¿Se preservó la trazabilidad?
Evidencia
¿Se mantuvo suficiente información para comprender el caso?
==================================================
30. SEGURIDAD Y TRAZABILIDAD

Nunca aplicar sanitización de manera que destruya la posibilidad de comprender:

qué ocurrió;
dónde ocurrió;
qué objeto fue afectado;
qué proceso estuvo involucrado;
qué condición provocó el comportamiento;
qué evidencia permitió concluirlo.

Cuando un dato pueda reemplazarse por un identificador anonimizado sin perder significado, debe preferirse esa alternativa.

==================================================
31. SEGURIDAD Y REUTILIZACIÓN

El conocimiento almacenado debe poder reutilizarse sin depender de datos sensibles.

Por ejemplo:

En lugar de almacenar:

El usuario Juan Pérez de la tienda Los Laureles ejecutó...

preferir:

Un usuario de tienda ejecutó...

si la identidad no aporta conocimiento funcional.

==================================================
32. REGLA CONTRA LA INVENCIÓN

La sanitización tampoco permite inventar información.

No inventar:

usuarios;
documentos;
datos;
configuraciones;
endpoints;
objetos;
reglas;
relaciones.

Si un dato fue anonimizado, debe indicarse cuando sea necesario.

Ejemplo:

Documento anonimizado por seguridad.
==================================================
33. CONTROL AUTOMÁTICO FUTURO

El estándar debe permitir implementar posteriormente controles automáticos como:

secret scanning;
detección de API keys;
detección de passwords;
detección de tokens;
análisis de archivos sensibles;
validación de metadata;
revisión de documentación;
detección de datos personales.

La estructura debe ser compatible con herramientas de seguridad de Git/GitHub.

==================================================
34. PRINCIPIO DE SEGURIDAD POR DEFECTO

Ante la duda sobre si un dato debe almacenarse:

NO almacenarlo hasta determinar que es necesario.

La ausencia de información innecesaria es preferible a su exposición.

==================================================
35. CHECKLIST FINAL

Antes de incorporar documentación al repositorio:

Secretos
No existen passwords.
No existen tokens.
No existen API keys.
No existen credenciales.
No existen claves privadas.
Datos personales
Se eliminaron datos personales innecesarios.
Se anonimizaron identidades cuando corresponde.
Datos productivos
Solo se conserva la información necesaria.
No existen exports innecesarios.
No existen dumps completos.
SAP
Se conservaron los identificadores técnicos necesarios.
No se eliminó información que destruya la trazabilidad.
Evidencia
La sanitización no destruyó la evidencia funcional.
Las conclusiones siguen siendo verificables.
Git
El archivo puede almacenarse de manera segura.
No existen secretos en el contenido.
No existen archivos sensibles innecesarios.
==================================================
36. PRINCIPIO FINAL

La seguridad del conocimiento debe seguir esta cadena:

INFORMACIÓN
↓
CLASIFICACIÓN
↓
RELEVANCIA
↓
SANITIZACIÓN
↓
VALIDACIÓN
↓
ALMACENAMIENTO
↓
REUTILIZACIÓN SEGURA

El objetivo no es ocultar el conocimiento.

El objetivo es conservar el conocimiento útil eliminando la exposición innecesaria.

La documentación de agenteSAP debe ser:

SEGURA
+
ÚTIL
+
TRAZABLE
+
REUTILIZABLE.

==================================================
37. INSTRUCCIÓN FINAL

Genera únicamente:

standards/security-standard.md

El archivo debe:

estar completamente escrito en Markdown;
ser autocontenido;
complementar standards/documentation-standard.md;
complementar standards/versioning-standard.md;
ser normativo;
ser claro para consultores funcionales SAP;
ser interpretable por agentes de IA;
ser compatible con Git/GitHub;
priorizar seguridad por defecto;
no inventar información;
no crear otros archivos;
no incluir explicaciones externas a este estándar.

### Cómo quedarían ahora tus `standards`

```text
standards/
├── documentation-standard.md
├── versioning-standard.md
└── security-standard.md

Y conceptualmente cada uno tiene una responsabilidad distinta:

Estándar	Responde
documentation-standard.md	¿Cómo documentamos el conocimiento?
versioning-standard.md	¿Cómo evoluciona y controlamos sus versiones?
security-standard.md	¿Qué podemos almacenar y cómo protegemos la información?
