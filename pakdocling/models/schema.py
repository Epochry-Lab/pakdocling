"""Schema definitions for Pakistani Document Intelligence Library."""

from enum import Enum
from typing import Any, Union

from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    """Supported document types in pakdocling."""

    CNIC = "cnic"
    MATRIC = "matric"
    INTERMEDIATE = "intermediate"
    DEGREE = "degree"
    AUTO = "auto"


class CNICVariant(str, Enum):
    """CNIC physical document format variants."""

    OLD_GREEN = "old_green"
    NEW_BLUE = "new_blue"
    UNKNOWN = "unknown"


class Gender(str, Enum):
    """Gender classification."""

    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNKNOWN = "unknown"


class CNICData(BaseModel):
    """Structured data model for Pakistani Computerized National Identity Card (CNIC)."""

    cnic_number: Union[str, None] = Field(
        default=None,
        description="13-digit CNIC number in standard XXXXX-XXXXXXX-X format",
    )
    variant: CNICVariant = Field(
        default=CNICVariant.UNKNOWN,
        description="CNIC physical card format (old green / new blue smart)",
    )
    full_name: Union[str, None] = Field(default=None, description="Cardholder full name")
    father_name: Union[str, None] = Field(default=None, description="Father's full name")
    husband_name: Union[str, None] = Field(
        default=None, description="Husband's full name if applicable"
    )
    gender: Gender = Field(default=Gender.UNKNOWN, description="Gender of cardholder")
    country_of_stay: Union[str, None] = Field(
        default=None, description="Country of stay / residence"
    )
    date_of_birth: Union[str, None] = Field(
        default=None, description="Date of birth (DD.MM.YYYY format)"
    )
    date_of_issue: Union[str, None] = Field(
        default=None, description="Date of issue (DD.MM.YYYY format)"
    )
    date_of_expiry: Union[str, None] = Field(
        default=None, description="Date of expiry (DD.MM.YYYY or Lifetime)"
    )
    confidence: float = Field(
        default=0.0, description="Overall field extraction confidence score (0-1)"
    )
    raw_text: Union[str, None] = Field(default=None, description="Raw extracted OCR text lines")


class MatricCertificateData(BaseModel):
    """Structured data model for Matriculation (SSC / 10th Grade) Certificate."""

    roll_number: Union[str, None] = Field(
        default=None, description="Candidate Examination Roll Number"
    )
    registration_number: Union[str, None] = Field(
        default=None, description="Board Registration Number"
    )
    student_name: Union[str, None] = Field(default=None, description="Student Full Name")
    father_name: Union[str, None] = Field(default=None, description="Father Full Name")
    board: Union[str, None] = Field(
        default=None, description="Board of Intermediate and Secondary Education (e.g. BISE Lahore)"
    )
    passing_year: Union[int, None] = Field(
        default=None, description="Year of passing / examination"
    )
    total_marks: Union[float, None] = Field(default=None, description="Total maximum marks")
    obtained_marks: Union[float, None] = Field(default=None, description="Total marks obtained")
    percentage: Union[float, None] = Field(
        default=None, description="Calculated or stated percentage"
    )
    grade: Union[str, None] = Field(default=None, description="Assigned grade (e.g. A+, A, B, C)")
    group: Union[str, None] = Field(
        default=None, description="Study group (e.g. Science, Humanities)"
    )
    confidence: float = Field(
        default=0.0, description="Overall field extraction confidence score (0-1)"
    )
    raw_text: Union[str, None] = Field(default=None, description="Raw extracted OCR text lines")


class IntermediateCertificateData(BaseModel):
    """Structured data model for Intermediate (HSSC / 12th Grade) Certificate."""

    roll_number: Union[str, None] = Field(
        default=None, description="Candidate Examination Roll Number"
    )
    registration_number: Union[str, None] = Field(
        default=None, description="Board Registration Number"
    )
    student_name: Union[str, None] = Field(default=None, description="Student Full Name")
    father_name: Union[str, None] = Field(default=None, description="Father Full Name")
    board: Union[str, None] = Field(
        default=None,
        description="Board of Intermediate and Secondary Education (e.g. BISE Rawalpindi)",
    )
    passing_year: Union[int, None] = Field(
        default=None, description="Year of passing / examination"
    )
    total_marks: Union[float, None] = Field(default=None, description="Total maximum marks")
    obtained_marks: Union[float, None] = Field(default=None, description="Total marks obtained")
    percentage: Union[float, None] = Field(
        default=None, description="Calculated or stated percentage"
    )
    grade: Union[str, None] = Field(default=None, description="Assigned grade (e.g. A+, A, B, C)")
    group: Union[str, None] = Field(
        default=None,
        description="Study group (e.g. Pre-Engineering, Pre-Medical, ICS, General Science)",
    )
    confidence: float = Field(
        default=0.0, description="Overall field extraction confidence score (0-1)"
    )
    raw_text: Union[str, None] = Field(default=None, description="Raw extracted OCR text lines")


class UniversityDegreeData(BaseModel):
    """Structured data model for Higher Education University Degree or Transcript."""

    student_name: Union[str, None] = Field(default=None, description="Student Full Name")
    father_name: Union[str, None] = Field(default=None, description="Father Full Name")
    roll_number: Union[str, None] = Field(
        default=None, description="Student Roll Number / Registration ID"
    )
    registration_number: Union[str, None] = Field(
        default=None, description="University Registration Number"
    )
    degree_title: Union[str, None] = Field(
        default=None,
        description="Degree Award Title (e.g. Bachelor of Science in Computer Science)",
    )
    major: Union[str, None] = Field(default=None, description="Major / Discipline")
    university_name: Union[str, None] = Field(default=None, description="Issuing University Name")
    graduation_year: Union[int, None] = Field(
        default=None, description="Graduation / Completion Year"
    )
    award_date: Union[str, None] = Field(default=None, description="Official degree conferral date")
    cgpa: Union[float, None] = Field(
        default=None, description="Cumulative Grade Point Average (CGPA)"
    )
    max_cgpa: Union[float, None] = Field(default=4.0, description="Maximum scale CGPA")
    total_marks: Union[float, None] = Field(default=None, description="Total Marks if applicable")
    obtained_marks: Union[float, None] = Field(
        default=None, description="Obtained Marks if applicable"
    )
    confidence: float = Field(
        default=0.0, description="Overall field extraction confidence score (0-1)"
    )
    raw_text: Union[str, None] = Field(default=None, description="Raw extracted OCR text lines")


ExtractedDocumentData = Union[
    CNICData,
    MatricCertificateData,
    IntermediateCertificateData,
    UniversityDegreeData,
]


class ConversionResult(BaseModel):
    """Wrapper result for all pakdocling conversions (Docling-aligned format)."""

    document_type: DocumentType = Field(description="Identified document type")
    success: bool = Field(description="Indicates whether extraction succeeded")
    data: Union[
        CNICData,
        MatricCertificateData,
        IntermediateCertificateData,
        UniversityDegreeData,
        dict[str, Any],
    ] = Field(description="Extracted structured document model or dictionary")
    errors: list[str] = Field(
        default_factory=list, description="List of warnings or extraction errors"
    )
    processing_time_ms: float = Field(default=0.0, description="Processing time in milliseconds")

    @property
    def document(
        self,
    ) -> Union[
        CNICData,
        MatricCertificateData,
        IntermediateCertificateData,
        UniversityDegreeData,
        dict[str, Any],
    ]:
        """Alias property matching Docling's .document attribute access."""
        return self.data

    def export_to_json(self, indent: Union[int, None] = None) -> str:
        """Export conversion result to JSON string (Docling format)."""
        return self.model_dump_json(indent=indent)

    def export_to_dict(self) -> dict[str, Any]:
        """Export conversion result to Python dictionary (Docling format)."""
        return self.model_dump()


# Backward compatibility alias
ExtractionResult = ConversionResult
