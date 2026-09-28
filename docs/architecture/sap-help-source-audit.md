# SAP Help Source Audit — Initial MM Phase

## Fuente oficial

La organización oficial de SAP en GitHub es `SAP`; su información pública identifica `SAP-docs` como una organización dedicada a documentación SAP. La organización SAP-docs contiene repositorios de documentación en Markdown que explican su relación con SAP Help Portal.

## Evidencia auditada

### SAP Help Portal

- Material Master — SAP S/4HANA on-premise 2023 Latest.
- Inventory Management / Inventory — documentación MM-IM.
- Goods Movement — SAP S/4HANA on-premise 2025 FPS01.

Estas páginas exponen versión/producto, lo que permite construir provenance de release.

### Repositorio SAP-docs de referencia de patrón

`SAP-docs/sap-hana-cloud-data-intelligence` fue inspeccionado como ejemplo de repositorio oficial de documentación Markdown. Contiene `docs/`, `LICENSE`, `LICENSES`, `REUSE.toml` y describe que sus Markdown son revisados para publicación en SAP Help Portal.

**No se utiliza ese repositorio como fuente de S/4HANA MM.** Su función en esta auditoría es demostrar que los repositorios SAP-docs no deben asumirse como una única estructura universal.

## Decisión

Para el MVP MM:

1. SAP Help Portal es la autoridad documental funcional.
2. SAP-docs sólo se utilizará como source repository cuando la correspondencia con la documentación objetivo esté demostrada.
3. No se copia contenido masivo.
4. La licencia de cada fuente debe registrarse; si no está disponible de forma verificable, permanece sin completar.
5. No se inventa `repository`, `commit_sha` o licencia para páginas que sólo fueron auditadas desde Help Portal.

## Gap abierto

Todavía no se ha identificado de forma verificable un repositorio SAP-docs específico que sea la fuente de los documentos S/4HANA MM utilizados en este MVP. Esto no bloquea el modelo de metadata ni el ingestion foundation, pero sí bloquea declarar una ingesta Git reproducible para esos documentos concretos.

## Safe next step

Identificar, para cada documento MM seleccionado, el repository/path/commit correspondiente cuando SAP lo exponga como fuente editable. Hasta entonces, mantener Help Portal como referencia oficial y conservar URL, versión, fecha de recuperación y hash del contenido recuperado.
