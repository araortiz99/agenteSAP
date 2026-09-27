# SAP Standard Knowledge

## Propósito

Esta carpeta contiene conocimiento derivado exclusivamente de documentación oficial de SAP.

Su objetivo es aportar al agente una capa de conocimiento SAP Standard independiente del conocimiento específico de la organización.

## Principios

- Una fuente SAP oficial no describe automáticamente el proceso interno de la organización.
- El release/version debe quedar identificado.
- El conocimiento debe conservar trazabilidad hacia la fuente.
- Si la documentación no permite confirmar una afirmación, debe marcarse como `partial`, `under_validation` o `not_confirmed`.
- El contenido local no debe sobrescribir silenciosamente una definición SAP Standard.
- Cuando SAP Standard y conocimiento interno se combinan, el proceso o regla correspondiente debe clasificarse como `mixed`.

## Estructura

```text
knowledge/
└── sap-standard/
    ├── README.md
    └── mm/
        ├── product-master.md
        └── inventory-management.md
```

## Metadata mínima

Los documentos SAP Standard deben incluir:

- `knowledge_type: standard`
- `knowledge_scope: global`
- `origin: sap`
- `source_type: sap_documentation`
- producto SAP
- módulo/componente
- release/version
- URL oficial
- fecha de recuperación
- certainty

## Alcance MVP

El primer alcance es:

- SAP S/4HANA on-premise 2025
- SAP MM
- Product Master
- Inventory Management and Inventory

Las fuentes utilizadas deben ser páginas del SAP Help Portal.

## Fuente oficial

El SAP Help Portal es el portal oficial de documentación de productos SAP. 

Fuente: https://help.sap.com/docs/

## No incluido

Esta capa no debe contener:

- configuraciones específicas de la organización;
- desarrollos Z;
- tickets internos;
- reglas de negocio locales;
- credenciales o secretos;
- conclusiones derivadas de documentación interna.

