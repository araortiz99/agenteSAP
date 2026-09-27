# SAP Standard Knowledge

This directory contains reusable knowledge derived from official SAP documentation.

## Separation rule

`knowledge/sap-standard/` describes SAP-provided functionality.

Organization-specific processes, configuration, Z developments, tickets and local business rules remain outside this directory.

## MVP scope

Initial scope:

- SAP S/4HANA
- Materials Management (MM)
- official SAP Help Portal documentation
- English source material where available

## Metadata

SAP Standard Knowledge should identify:

```yaml
knowledge_type: standard
knowledge_scope: global
source_type: sap_documentation
origin: sap
product: SAP S/4HANA
module: MM
release: "2025"
certainty: confirmed
```

The metadata is descriptive and must be supported by the source.

## Source catalog

See [source-catalog.md](source-catalog.md).

## Future structure

```
knowledge/sap-standard/
├── index.md
├── source-catalog.md
└── mm/
    ├── README.md
    └── <topic>.md
```

Topic files will be added only after source retrieval and validation.
