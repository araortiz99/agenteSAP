# Evidence Provenance

Toda evidencia SAP Help debe ser reconstruible desde su origen.

## Identidad

Formato conceptual:

`EVD-SAPHELP-XXXXXXXX`

La identidad no sustituye la metadata de origen.

## Campos

Cada evidencia debe conservar:

- source_type;
- source_system;
- repository;
- branch;
- commit_sha o version;
- path;
- document_id;
- section_path;
- chunk_id;
- content_hash;
- help_url;
- source_url;
- retrieved_at;
- authority_level;
- confidence;
- status.

## Regla

El Consultant puede citar una evidencia SAP Help únicamente si esa evidencia está registrada en Traceability. No puede inventar un EVD ni una URL.

## Separación

- SAP_STANDARD → evidencia estándar.
- INTERNAL → evidencia interna.
- OPTIONAL_RUNTIME → observación runtime.

Una cita de SAP_STANDARD no puede utilizarse como cita de una configuración interna.
