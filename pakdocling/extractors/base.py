"""Base Extractor interface for document parsers."""

from abc import ABC, abstractmethod

from pydantic import BaseModel

from pakdocling.ocr.engine import OCRResultItem


class BaseExtractor(ABC):
    """Abstract base class for all document field extractors."""

    @abstractmethod
    def extract(self, items: list[OCRResultItem], raw_text: str) -> BaseModel:
        """Extract structured fields from OCR result items and raw text string."""
        pass

    @abstractmethod
    def supports_raw_text(self, raw_text: str) -> bool:
        """Return True if raw_text matches document characteristics."""
        pass
