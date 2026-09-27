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
