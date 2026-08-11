"""OCR Engine interface and implementations for EasyOCR and Mock engines."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Union

import numpy as np


@dataclass
class OCRResultItem:
    """Individual OCR bounding box item with extracted text and confidence."""

    text: str
    bbox: Union[list[list[float]], None] = None
    confidence: float = 1.0


class BaseOCREngine(ABC):
    """Abstract base interface for OCR engines."""

    @abstractmethod
    def extract_text(self, image: Union[str, bytes, np.ndarray]) -> tuple[list[OCRResultItem], str]:
        """Perform OCR extraction on input image.

        Returns:
            A tuple of (list of OCRResultItem, raw concatenated text).
        """
        pass


class EasyOCREngine(BaseOCREngine):
    """EasyOCR implementation with lazy loading to defer PyTorch/EasyOCR initialization."""

    def __init__(self, languages: Union[list[str], None] = None, gpu: bool = False) -> None:
        self.languages = languages or ["en"]
        self.gpu = gpu
        self._reader: Any = None

    def _get_reader(self) -> Any:
        if self._reader is None:
            try:
                import easyocr  # type: ignore[import-untyped,import-not-found]

                self._reader = easyocr.Reader(self.languages, gpu=self.gpu)
            except ImportError as e:
                raise ImportError(
                    "EasyOCR is not installed. Please install easyocr via `pip install easyocr`."
                ) from e
        return self._reader

    def extract_text(self, image: Union[str, bytes, np.ndarray]) -> tuple[list[OCRResultItem], str]:
        from pakdocling.preprocessing.image import ImagePreprocessor

        preprocessed = ImagePreprocessor.load_image(image)
        reader = self._get_reader()

        # Read text from image array
        raw_results = reader.readtext(preprocessed)

        items: list[OCRResultItem] = []
        text_lines: list[str] = []

        for bbox, text, prob in raw_results:
            cleaned_text = str(text).strip()
            if cleaned_text:
                items.append(
                    OCRResultItem(
                        text=cleaned_text,
                        bbox=[[float(pt[0]), float(pt[1])] for pt in bbox],
                        confidence=float(prob),
                    )
                )
                text_lines.append(cleaned_text)

        full_raw_text = "\n".join(text_lines)
        return items, full_raw_text


class MockOCREngine(BaseOCREngine):
    """Mock OCR engine for fast unit testing and offline deterministic tests."""

    def __init__(
        self,
        mock_items: Union[list[OCRResultItem], None] = None,
        mock_text: Union[str, None] = None,
    ) -> None:
        self.mock_items = mock_items or []
        self.mock_text = mock_text

    def set_mock_data(
        self,
        mock_items: Union[list[OCRResultItem], None] = None,
        mock_text: Union[str, None] = None,
    ) -> None:
        if mock_items is not None:
            self.mock_items = mock_items
        if mock_text is not None:
            self.mock_text = mock_text

    def extract_text(self, image: Union[str, bytes, np.ndarray]) -> tuple[list[OCRResultItem], str]:
        if self.mock_text and not self.mock_items:
            lines = [line.strip() for line in self.mock_text.splitlines() if line.strip()]
            items = [OCRResultItem(text=line, confidence=0.99) for line in lines]
            return items, self.mock_text

        raw_text = self.mock_text or "\n".join([item.text for item in self.mock_items])
        return self.mock_items, raw_text
