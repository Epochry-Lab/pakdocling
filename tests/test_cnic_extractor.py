"""Unit tests for CNIC Extractor."""

from pakdocling.extractors.cnic import CNICExtractor
from pakdocling.models.schema import CNICVariant, Gender


def test_cnic_extractor_male_new_blue() -> None:
    extractor = CNICExtractor()
    mock_text = """
    NATIONAL IDENTITY CARD
    ISLAMIC REPUBLIC OF PAKISTAN
    Name: Muhammad Bilal Khan
    Father Name: Tariq Mehmood Khan
    Gender: M
    Country of Stay: Pakistan
    Identity Number: 35202-9876543-1
    Date of Birth: 15.08.1995
    Date of Issue: 10.01.2020
    Date of Expiry: 10.01.2030
    """

    data = extractor.extract(items=[], raw_text=mock_text)

    assert data.cnic_number == "35202-9876543-1"
    assert data.full_name == "Muhammad Bilal Khan"
    assert data.father_name == "Tariq Mehmood Khan"
    assert data.gender == Gender.MALE
    assert data.date_of_birth == "15.08.1995"
    assert data.date_of_issue == "10.01.2020"
    assert data.date_of_expiry == "10.01.2030"
    assert data.confidence > 0.8


def test_cnic_extractor_female_lifetime() -> None:
    extractor = CNICExtractor()
    mock_text = """
    PAKISTAN NATIONAL IDENTITY CARD
    Name: Fatima Zahra
    Husband Name: Hassan Raza
    Identity Number: 61101-1234567-2
    Date of Birth: 01.01.1960
    Date of Issue: 05.05.2015
    Date of Expiry: Lifetime
    """

    data = extractor.extract(items=[], raw_text=mock_text)

    assert data.cnic_number == "61101-1234567-2"
    assert data.full_name == "Fatima Zahra"
    assert data.husband_name == "Hassan Raza"
    assert data.gender == Gender.FEMALE
    assert data.date_of_expiry == "Lifetime"


def test_cnic_supports_raw_text() -> None:
    extractor = CNICExtractor()
    assert extractor.supports_raw_text("35201-1234567-3") is True
    assert extractor.supports_raw_text("Matriculation Certificate BISE Lahore") is False
