"""Unit tests for pakdocling Pydantic models."""

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


def test_cnic_model_defaults() -> None:
    data = CNICData(cnic_number="35202-1234567-1", full_name="Muhammad Ali")
    assert data.cnic_number == "35202-1234567-1"
    assert data.full_name == "Muhammad Ali"
    assert data.variant == CNICVariant.UNKNOWN
    assert data.gender == Gender.UNKNOWN


def test_matric_model() -> None:
    data = MatricCertificateData(
        roll_number="123456",
        student_name="Ayesha Khan",
        board="BISE Lahore",
        obtained_marks=950.0,
        total_marks=1100.0,
        percentage=86.36,
    )
    assert data.roll_number == "123456"
    assert data.percentage == 86.36
    assert data.board == "BISE Lahore"


def test_intermediate_model() -> None:
    data = IntermediateCertificateData(
        roll_number="654321",
        student_name="Zaid Ahmed",
        group="Pre-Engineering",
        grade="A+",
    )
    assert data.roll_number == "654321"
    assert data.group == "Pre-Engineering"
    assert data.grade == "A+"


def test_university_degree_model() -> None:
    data = UniversityDegreeData(
        student_name="Hamza Tariq",
        degree_title="Bachelor of Science in Computer Science",
        university_name="NUST",
        cgpa=3.85,
    )
    assert data.student_name == "Hamza Tariq"
    assert data.cgpa == 3.85
    assert data.max_cgpa == 4.0


def test_extraction_result_wrapper() -> None:
    cnic = CNICData(cnic_number="61101-1234567-2")
    result = ExtractionResult(
        document_type=DocumentType.CNIC,
        success=True,
        data=cnic,
        processing_time_ms=45.2,
    )
    assert result.document_type == DocumentType.CNIC
    assert result.success is True
    assert result.data.cnic_number == "61101-1234567-2"  # type: ignore[union-attr]
