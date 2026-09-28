# Knowledge Sources

## Capas

| Capa | Identidad | Autoridad | Puede confirmar |
|---|---|---|---|
| SAP_STANDARD | SAP Help / SAP-docs oficial | estándar SAP | comportamiento estándar documentado |
| INTERNAL | Knowledge propio | implementación | procesos, Z, tickets y decisiones documentadas |
| OPTIONAL_RUNTIME | QAS read-only | sistema real | observaciones actuales |

Las capas nunca deben fusionarse semánticamente.

## SAP_STANDARD

Metadata mínima:

- source_type = SAP_STANDARD
- source_system = SAP_HELP
- repository
- branch
- commit_sha
- path
- document_id
- title
- product
- component
- version
- language
- help_url
- source_url
- last_modified
- retrieved_at
- content_hash
- license
- authority_level
- confidence
- status

Metadata inferida debe declarar `metadata_origin=inferred`.

## Versiones

No asumir equivalencia entre releases. Cuando una consulta no especifica release, la respuesta debe informar el release de la evidencia y advertir cuando la aplicabilidad requiera validación.

## Provenance

Cadena mínima:

`SAP Help → source → document → section → chunk → retrieval → EVD → reasoning → answer`

