"""Pakdocling extractor modules."""

from pakdocling.extractors.base import BaseExtractor
from pakdocling.extractors.cnic import CNICExtractor
from pakdocling.extractors.degree import DegreeExtractor
from pakdocling.extractors.intermediate import IntermediateExtractor
from pakdocling.extractors.matric import MatricExtractor

__all__ = [
    "BaseExtractor",
    "CNICExtractor",
    "MatricExtractor",
    "IntermediateExtractor",
    "DegreeExtractor",
]
