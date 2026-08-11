"""pakdocling - Pakistani Document Intelligence Library."""

from pakdocling.extractors import (
    BaseExtractor,
    CNICExtractor,
    DegreeExtractor,
    IntermediateExtractor,
    MatricExtractor,
)
from pakdocling.models import (
    CNICData,
    CNICVariant,
    DocumentType,
    ExtractionResult,
    Gender,
    IntermediateCertificateData,
    MatricCertificateData,
    UniversityDegreeData,
)
from pakdocling.ocr import BaseOCREngine, EasyOCREngine, MockOCREngine, OCRResultItem
from pakdocling.pipeline import DocumentPipeline, extract_document
from pakdocling.preprocessing import ImagePreprocessor

__version__ = "0.0.1"

__all__ = [
    "__version__",
    "DocumentType",
    "CNICVariant",
    "Gender",
    "CNICData",
    "MatricCertificateData",
    "IntermediateCertificateData",
    "UniversityDegreeData",
    "ExtractionResult",
    "BaseExtractor",
    "CNICExtractor",
    "MatricExtractor",
    "IntermediateExtractor",
    "DegreeExtractor",
    "OCRResultItem",
    "BaseOCREngine",
    "EasyOCREngine",
    "MockOCREngine",
    "ImagePreprocessor",
    "DocumentPipeline",
    "extract_document",
]
