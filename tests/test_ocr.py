"""Unit tests for OCR engines interface and MockOCREngine."""

import numpy as np

from pakdocling.ocr import MockOCREngine, OCRResultItem


def test_mock_ocr_engine_with_text() -> None:
    mock_text = "PAKISTAN NATIONAL IDENTITY CARD\nName: Usman Ali\nCNIC: 35201-1234567-3"
    engine = MockOCREngine(mock_text=mock_text)

    dummy_img = np.zeros((10, 10, 3), dtype=np.uint8)
    items, raw_text = engine.extract_text(dummy_img)

    assert raw_text == mock_text
    assert len(items) == 3
    assert items[0].text == "PAKISTAN NATIONAL IDENTITY CARD"
    assert items[2].text == "CNIC: 35201-1234567-3"


def test_mock_ocr_engine_with_items() -> None:
    items_in = [
        OCRResultItem(text="BISE Lahore", confidence=0.99),
        OCRResultItem(text="Roll No: 123456", confidence=0.95),
    ]
    engine = MockOCREngine(mock_items=items_in)

    dummy_img = np.zeros((10, 10, 3), dtype=np.uint8)
    items_out, raw_text = engine.extract_text(dummy_img)

    assert len(items_out) == 2
    assert "BISE Lahore" in raw_text
    assert "123456" in raw_text
