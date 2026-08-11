"""Unit tests for Matric, Intermediate, and Degree extractors."""

from pakdocling.extractors.degree import DegreeExtractor
from pakdocling.extractors.intermediate import IntermediateExtractor
from pakdocling.extractors.matric import MatricExtractor


def test_matric_extractor() -> None:
    extractor = MatricExtractor()
    mock_text = """
    BOARD OF INTERMEDIATE AND SECONDARY EDUCATION LAHORE
    SECONDARY SCHOOL CERTIFICATE (MATRICULATION)
    ANNUAL EXAMINATION 2020
    Roll No: 154321
    Registration No: 2018-LHR-9876
    Certified that: Ahmed Ali
    Son of: Kamran Ali
    Group: Science
    Marks Obtained: 980 / 1100
    Grade: A+
    """

    data = extractor.extract(items=[], raw_text=mock_text)

    assert data.roll_number == "154321"
    assert data.registration_number == "2018-LHR-9876"
    assert data.student_name == "Ahmed Ali"
    assert data.father_name == "Kamran Ali"
    assert data.board == "BISE Lahore"
    assert data.passing_year == 2020
    assert data.obtained_marks == 980.0
    assert data.total_marks == 1100.0
    assert data.percentage == 89.09
    assert data.grade == "A+"
    assert data.group == "Science"


def test_intermediate_extractor() -> None:
    extractor = IntermediateExtractor()
    mock_text = """
    BOARD OF INTERMEDIATE AND SECONDARY EDUCATION RAWALPINDI
    HIGHER SECONDARY SCHOOL CERTIFICATE (HSSC)
    ANNUAL EXAMINATION 2022
    Roll No: 654321
    Reg No: 2020-RWP-4321
    Name: Sara Khan
    Daughter of: Shahbaz Khan
    Group: Pre-Medical
    Marks: 995
    Out of: 1100
    Grade: A+
    """

    data = extractor.extract(items=[], raw_text=mock_text)

    assert data.roll_number == "654321"
    assert data.student_name == "Sara Khan"
    assert data.father_name == "Shahbaz Khan"
    assert data.board == "BISE Rawalpindi"
    assert data.passing_year == 2022
    assert data.obtained_marks == 995.0
    assert data.group == "Pre-Medical"


def test_degree_extractor() -> None:
    extractor = DegreeExtractor()
    mock_text = """
    NATIONAL UNIVERSITY OF SCIENCES AND TECHNOLOGY (NUST)
    ISLAMABAD, PAKISTAN
    It is certified that: Zainab Shah
    Daughter of: Anwar Shah
    Registration No: NUST-2019-BSCS-0042
    having fulfilled all academic requirements is hereby awarded the degree of
    Bachelor of Science in Software Engineering
    Graduation Year: 2023
    CGPA: 3.82 / 4.00
    """

    data = extractor.extract(items=[], raw_text=mock_text)

    assert data.student_name == "Zainab Shah"
    assert data.father_name == "Anwar Shah"
    assert data.university_name == "National University of Sciences and Technology"
    assert data.degree_title == "Bachelor of Science in Software Engineering"
    assert data.major == "Software Engineering"
    assert data.registration_number == "NUST-2019-BSCS-0042"
    assert data.cgpa == 3.82
    assert data.graduation_year == 2023
