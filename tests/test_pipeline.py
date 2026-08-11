"""Unit tests for DocumentPipeline with MockOCREngine."""

import numpy as np

from pakdocling.models import DocumentType
from pakdocling.ocr import MockOCREngine
from pakdocling.pipeline import DocumentPipeline, extract_document


def test_pipeline_cnic_extraction() -> None:
    mock_text = (
        "PAKISTAN NATIONAL IDENTITY CARD\n"
        "Name: Ali Raza\n"
        "CNIC: 35202-1234567-1\n"
        "Date of Birth: 01.01.1990"
    )
    mock_ocr = MockOCREngine(mock_text=mock_text)

    pipeline = DocumentPipeline(ocr_engine=mock_ocr)

    dummy_img = np.zeros((100, 100, 3), dtype=np.uint8)
    result = pipeline.extract(dummy_img, doc_type=DocumentType.AUTO, do_preprocess=False)

    assert result.success is True
    assert result.document_type == DocumentType.CNIC
    assert result.data.cnic_number == "35202-1234567-1"  # type: ignore[union-attr]


def test_pipeline_matric_auto_detection() -> None:
    mock_text = "BISE Lahore\nSECONDARY SCHOOL CERTIFICATE\nRoll No: 123456\nName: Usman Ali"
    mock_ocr = MockOCREngine(mock_text=mock_text)

    dummy_img = np.zeros((50, 50, 3), dtype=np.uint8)
    result = extract_document(dummy_img, doc_type="auto", ocr_engine=mock_ocr)

    assert result.success is True
    assert result.document_type == DocumentType.MATRIC
    assert result.data.roll_number == "123456"  # type: ignore[union-attr]
