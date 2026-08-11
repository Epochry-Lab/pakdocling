"""Document Intelligence Pipeline orchestrator."""

import time
from typing import Union, cast

import numpy as np
from PIL import Image  # type: ignore[import-untyped]

from pakdocling.extractors.base import BaseExtractor
from pakdocling.extractors.cnic import CNICExtractor
from pakdocling.extractors.degree import DegreeExtractor
from pakdocling.extractors.intermediate import IntermediateExtractor
from pakdocling.extractors.matric import MatricExtractor
from pakdocling.models.schema import (
    CNICData,
    ConversionResult,
    DocumentType,
    ExtractedDocumentData,
)
from pakdocling.ocr.engine import BaseOCREngine, EasyOCREngine
from pakdocling.preprocessing.image import ImagePreprocessor


class DocumentConverter:
    """Docling-aligned Document Converter for Pakistani documents."""

    def __init__(
        self,
        ocr_engine: Union[BaseOCREngine, None] = None,
        preprocessor: Union[ImagePreprocessor, None] = None,
    ) -> None:
        self.ocr_engine = ocr_engine or EasyOCREngine()
        self.preprocessor = preprocessor or ImagePreprocessor()

        self.extractors: dict[DocumentType, BaseExtractor] = {
            DocumentType.CNIC: CNICExtractor(),
            DocumentType.MATRIC: MatricExtractor(),
            DocumentType.INTERMEDIATE: IntermediateExtractor(),
            DocumentType.DEGREE: DegreeExtractor(),
        }

    def detect_document_type(self, raw_text: str) -> DocumentType:
        """Classify document type automatically based on raw text contents."""
        for doc_type, extractor in self.extractors.items():
            if extractor.supports_raw_text(raw_text):
                return doc_type
        return DocumentType.CNIC  # Default fallback if unknown

    def convert(
        self,
        source: Union[str, bytes, np.ndarray, Image.Image],
        doc_type: Union[DocumentType, str] = DocumentType.AUTO,
        do_preprocess: bool = True,
    ) -> ConversionResult:
        """Convert document image into a structured ConversionResult (Docling-aligned format).

        Args:
            source: Image file path, raw bytes, OpenCV ndarray, or PIL Image.
            doc_type: Document type ('cnic', 'matric', 'intermediate', 'degree', or 'auto').
            do_preprocess: Apply OpenCV deskewing and contrast enhancement prior to OCR.

        Returns:
            ConversionResult object containing structured data model and metadata.
        """
        start_time = time.time()
        errors: list[str] = []

        try:
            # Preprocess image
            if do_preprocess:
                prep_result = self.preprocessor.preprocess(source)
                target_image = prep_result["processed_gray"]
            else:
                target_image = self.preprocessor.load_image(source)

            # Perform OCR
            ocr_items, raw_text = self.ocr_engine.extract_text(target_image)

            # Determine document type
            if isinstance(doc_type, str):
                target_doc_type = DocumentType(doc_type.lower())
            else:
                target_doc_type = doc_type

            if target_doc_type == DocumentType.AUTO:
                target_doc_type = self.detect_document_type(raw_text)

            extractor = self.extractors.get(target_doc_type, CNICExtractor())
            extracted_data = cast(ExtractedDocumentData, extractor.extract(ocr_items, raw_text))

            processing_time = round((time.time() - start_time) * 1000.0, 2)

            return ConversionResult(
                document_type=target_doc_type,
                success=True,
                data=extracted_data,
                errors=errors,
                processing_time_ms=processing_time,
            )

        except Exception as e:
            processing_time = round((time.time() - start_time) * 1000.0, 2)
            errors.append(str(e))
            return ConversionResult(
                document_type=DocumentType.AUTO,
                success=False,
                data=CNICData(),
                errors=errors,
                processing_time_ms=processing_time,
            )

    def extract(
        self,
        image_source: Union[str, bytes, np.ndarray, Image.Image],
        doc_type: Union[DocumentType, str] = DocumentType.AUTO,
        do_preprocess: bool = True,
    ) -> ConversionResult:
        """Alias for convert() method."""
        return self.convert(source=image_source, doc_type=doc_type, do_preprocess=do_preprocess)


def convert(
    source: Union[str, bytes, np.ndarray, Image.Image],
    doc_type: Union[DocumentType, str] = DocumentType.AUTO,
    ocr_engine: Union[BaseOCREngine, None] = None,
) -> ConversionResult:
    """Convenience Docling-aligned functional interface for document conversion."""
    converter = DocumentConverter(ocr_engine=ocr_engine)
    return converter.convert(source=source, doc_type=doc_type)


# Backward compatibility aliases
DocumentPipeline = DocumentConverter
extract_document = convert
