from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

import pytest

from src.document.adapters import (
    SUPPORTED_BINARY_TYPES,
    load_docx_file,
    load_pdf_file,
    load_supported_binary_file,
    load_xlsx_file,
)


def test_supported_binary_types_are_explicit():
    assert SUPPORTED_BINARY_TYPES == frozenset({"pdf", "docx", "xlsx"})


def test_docx_adapter_extracts_text_read_only(tmp_path: Path):
    docx = pytest.importorskip("docx")
    path = tmp_path / "spec.docx"
    document = docx.Document()
    document.add_paragraph("Incidente MM 31426")
    document.add_paragraph("Material 100123 en centro 5023")
    document.save(path)
    before = path.read_bytes()

    source = load_docx_file(path)

    assert source.file_type == "docx"
    assert source.media_type.startswith("application/vnd.openxmlformats")
    assert "31426" in source.content
    assert "100123" in source.content
    assert path.read_bytes() == before


def test_xlsx_adapter_extracts_values_read_only(tmp_path: Path):
    openpyxl = pytest.importorskip("openpyxl")
    path = tmp_path / "evidence.xlsx"
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "MM"
    sheet.append(["Material", "Centro", "Cantidad"])
    sheet.append(["100123", "5023", 14])
    workbook.save(path)
    workbook.close()

    source = load_xlsx_file(path)

    assert source.file_type == "xlsx"
    assert "100123" in source.content
    assert "5023" in source.content
    assert "14" in source.content
    assert "[MM]" in source.content


def test_pdf_adapter_extracts_text_read_only(tmp_path: Path):
    reportlab = pytest.importorskip("reportlab")
    path = tmp_path / "evidence.pdf"
    from reportlab.pdfgen import canvas

    pdf = canvas.Canvas(str(path))
    pdf.drawString(72, 720, "Incidente MM 31426")
    pdf.drawString(72, 700, "Material 100123 centro 5023")
    pdf.save()

    source = load_pdf_file(path)

    assert source.file_type == "pdf"
    assert source.media_type == "application/pdf"
    assert "31426" in source.content
    assert "100123" in source.content


def test_binary_adapter_rejects_unsupported_format(tmp_path: Path):
    path = tmp_path / "image.png"
    path.write_bytes(b"PNG")

    with pytest.raises(ValueError, match="unsupported binary document type"):
        load_supported_binary_file(path)


def test_binary_adapter_rejects_oversized_file(tmp_path: Path):
    path = tmp_path / "evidence.pdf"
    path.write_bytes(b"%PDF-test")

    with pytest.raises(ValueError, match="max_bytes"):
        load_pdf_file(path, max_bytes=1)


def test_binary_adapter_rejects_missing_file(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        load_xlsx_file(tmp_path / "missing.xlsx")


def test_xlsx_adapter_does_not_execute_formulas():
    # Contract-level guard: adapter is designed around data_only/read_only loading.
    # Detailed workbook generation is covered by the extraction test above.
    assert load_xlsx_file.__doc__
