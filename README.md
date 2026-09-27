# agenteSAP

Agente consultivo para conocimiento y documentación funcional SAP.

## Estado

MVP inicial en construcción.

El primer vertical implementado es una capacidad de búsqueda read-only sobre el repositorio:

`search_knowledge()`

## Arquitectura inicial

```
Usuario
  ↓
Agente
  ↓
Capabilities
  ↓
Tools
  ↓
GitHub repository
  ↓
knowledge / tickets / standards / templates
```

## Seguridad

El MVP no ejecuta SAP y no modifica SAP.

El código utiliza GitHub únicamente para lectura. Las credenciales, cuando sean necesarias, deben proporcionarse mediante variables de entorno y nunca almacenarse en el repositorio.

## Próximo paso

Implementar `get_ticket()` sobre el mismo contrato y agregar pruebas de integración contra el repositorio.
