"""Unit tests for DocumentConverter and convert with MockOCREngine."""

import numpy as np

from pakdocling import DocumentConverter, convert
from pakdocling.models import DocumentType
from pakdocling.ocr import MockOCREngine


def test_converter_cnic_conversion() -> None:
    mock_text = (
        "PAKISTAN NATIONAL IDENTITY CARD\n"
        "Name: Ali Raza\n"
        "CNIC: 35202-1234567-1\n"
        "Date of Birth: 01.01.1990"
    )
    mock_ocr = MockOCREngine(mock_text=mock_text)

    converter = DocumentConverter(ocr_engine=mock_ocr)

    dummy_img = np.zeros((100, 100, 3), dtype=np.uint8)
    result = converter.convert(dummy_img, doc_type=DocumentType.AUTO, do_preprocess=False)

    assert result.success is True
    assert result.document_type == DocumentType.CNIC
    assert result.document.cnic_number == "35202-1234567-1"  # type: ignore[union-attr]
    assert result.data.cnic_number == "35202-1234567-1"  # type: ignore[union-attr]

    # Test export methods
    json_export = result.export_to_json(indent=2)
    assert "35202-1234567-1" in json_export

    dict_export = result.export_to_dict()
    assert dict_export["document_type"] == DocumentType.CNIC


def test_convert_functional_interface() -> None:
    mock_text = "BISE Lahore\nSECONDARY SCHOOL CERTIFICATE\nRoll No: 123456\nName: Usman Ali"
    mock_ocr = MockOCREngine(mock_text=mock_text)

    dummy_img = np.zeros((50, 50, 3), dtype=np.uint8)
    result = convert(dummy_img, doc_type="auto", ocr_engine=mock_ocr)

    assert result.success is True
    assert result.document_type == DocumentType.MATRIC
    assert result.document.roll_number == "123456"  # type: ignore[union-attr]
