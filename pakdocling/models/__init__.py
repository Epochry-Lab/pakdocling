"""Pakdocling models package."""

from pakdocling.models.schema import (
    CNICData,
    CNICVariant,
    ConversionResult,
    DocumentType,
    ExtractedDocumentData,
    ExtractionResult,
    Gender,
    IntermediateCertificateData,
    MatricCertificateData,
    UniversityDegreeData,
)

__all__ = [
    "DocumentType",
    "CNICVariant",
    "Gender",
    "CNICData",
    "MatricCertificateData",
    "IntermediateCertificateData",
    "UniversityDegreeData",
    "ExtractedDocumentData",
    "ConversionResult",
    "ExtractionResult",
]
