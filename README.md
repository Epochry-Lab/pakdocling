# pakdocling: Pakistani Document Intelligence Library 🇵🇰

[![PyPI Version](https://img.shields.io/pypi/v/pakdocling.svg)](https://pypi.org/project/pakdocling/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

An open-source Python library for structured data extraction from Pakistani identity and educational documents.

## 🎯 The Problem

Existing international OCR engines (EasyOCR, Tesseract, AWS Textract) return unstructured, line-by-line raw text without understanding document layouts. They do not know what a Pakistani CNIC looks like, cannot parse field structures of Pakistani Board Matric/Intermediate certificates, and do not return structured JSON objects with named fields.

Pakistani developers building **KYC pipelines**, **HR systems**, and **edtech platforms** currently solve this manually or with expensive proprietary APIs.

`pakdocling` solves this by taking document images as input and returning validated, typed **Pydantic JSON objects**.

---

## 📄 Documents Supported in v1

| Document Type | Document ID | Key Fields Extracted |
| :--- | :--- | :--- |
| **CNIC** | `cnic` | 13-digit CNIC number, Name, Father/Husband Name, Gender, DOB, Issue Date, Expiry Date, Card Format (`old_green` vs `new_blue` Smart Card) |
| **Matric Certificate** | `matric` | Roll No, Registration No, Student Name, Father Name, Board (BISE Lahore, Karachi, Rawalpindi, etc.), Passing Year, Total & Obtained Marks, Grade, Group |
| **Intermediate Certificate** | `intermediate` | Roll No, Reg No, Student Name, Father Name, BISE Board, Passing Year, Total/Obtained Marks, Grade, Group (Pre-Engineering, Pre-Medical, ICS, Commerce) |
| **University Degree / Transcript** | `degree` | Student Name, Father Name, Registration No, Degree Award Title, Major, Issuing University (NUST, FAST, QAU, LUMS, PU, etc.), Graduation Year, CGPA |

---

## 🚀 Installation

```bash
pip install pakdocling
```

For development mode:
```bash
git clone https://github.com/Epochry-Lab/pakdocling.git
cd pakdocling
pip install -e ".[dev]"
```

---

## 💻 Python API Usage

### 1. Extracting Data from a CNIC Image

```python
from pakdocling import extract_document

# Auto-detect or specify doc_type='cnic'
result = extract_document("path/to/cnic_card.jpg", doc_type="cnic")

if result.success:
    cnic = result.data
    print(f"CNIC Number: {cnic.cnic_number}")
    print(f"Name: {cnic.full_name}")
    print(f"Father Name: {cnic.father_name}")
    print(f"Gender: {cnic.gender}")
    print(f"Date of Birth: {cnic.date_of_birth}")
    print(f"Card Variant: {cnic.variant}")
```

### 2. Outputting Validated JSON

```python
from pakdocling import DocumentPipeline, DocumentType

pipeline = DocumentPipeline()
result = pipeline.extract("matric_certificate.png", doc_type=DocumentType.MATRIC)

# Export Pydantic model to JSON
print(result.model_dump_json(indent=2))
```

### 3. Offline & Fast Testing with `MockOCREngine`

```python
from pakdocling import DocumentPipeline, MockOCREngine

mock_ocr = MockOCREngine(mock_text="""
NATIONAL UNIVERSITY OF SCIENCES AND TECHNOLOGY (NUST)
Certified that Zainab Shah Registration No NUST-2019-BSCS-0042
is awarded Bachelor of Science in Software Engineering
CGPA: 3.85 / 4.00
Graduation Year: 2023
""")

pipeline = DocumentPipeline(ocr_engine=mock_ocr)
result = pipeline.extract("dummy.png", doc_type="degree")
print(result.data.degree_title)  # "Bachelor of Science in Software Engineering"
print(result.data.cgpa)          # 3.85
```

---

## 🛠️ Command Line Interface (CLI)

`pakdocling` comes with a CLI powered by Typer and Rich:

```bash
# Check version & supported document schemas
pakdocling info

# Extract data from an image file and print formatted JSON
pakdocling extract sample_cnic.jpg --doc-type cnic

# Extract and save JSON to a file
pakdocling extract degree_transcript.png --doc-type auto -o output.json
```

---

## 🏗️ Core Technology Stack

- **EasyOCR**: Deep learning OCR engine for multi-language text extraction.
- **OpenCV & NumPy**: Image preprocessing pipeline (deskewing, noise reduction, adaptive thresholding, contrast enhancement).
- **Pydantic v2**: Type safety, field validation, and JSON serialization.
- **Typer & Rich**: Modern terminal CLI interface.

---

## 🤝 Contributing

Contributions are welcome! Check out [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

## 📜 License

Distributed under the MIT License. See `LICENSE` for details.
