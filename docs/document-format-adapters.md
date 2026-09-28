# Document format adapters

## Scope

PR 111 adds bounded, read-only adapters for PDF, DOCX and XLSX. They normalize binary documents into the existing `DocumentSource` contract so the current ingestion pipeline remains the single downstream path.

## Safety contract

- Local filesystem only; no recursive discovery.
- Input size is bounded before parsing.
- PDF pages, DOCX items and XLSX rows/cells/chars are bounded.
- XLSX is opened with `read_only=True` and `data_only=True`; formulas/macros are not executed by the adapter.
- No SAP/QAS/MCP calls.
- No writes or persistence.
- Unsupported formats fail closed.
- The adapter layer does not create investigation evidence directly; `ingest_document` remains responsible for chunking, provenance and SAP entity extraction.

## Supported formats

| Format | Adapter | Output |
|---|---|---|
| PDF | `load_pdf_file` | extracted text |
| DOCX | `load_docx_file` | paragraphs + table rows |
| XLSX | `load_xlsx_file` | bounded worksheet cell values |

## Dependencies

The adapters use `pypdf`, `python-docx` and `openpyxl`. These are parsing dependencies only; they do not expand the agent into a database, vector store or SAP runtime integration.

## Acceptance

The existing TXT/MD/CSV path remains unchanged. Binary formats enter through adapters and then follow the existing bounded ingestion path.
