"""Matriculation Certificate Extractor for BISE 10th grade certificates."""

import re
from typing import Union
from pakdocling.extractors.base import BaseExtractor
from pakdocling.models.schema import MatricCertificateData
from pakdocling.ocr.engine import OCRResultItem


class MatricExtractor(BaseExtractor):
    """Extractor for Pakistani BISE Matriculation (SSC 10th Grade) Certificates."""

    ROLL_REGEX = re.compile(r"\b(?:roll\s*no|rollno|roll\s*#)[.:\s]*([0-9]{5,8})\b", re.IGNORECASE)
    REG_REGEX = re.compile(
        r"\b(?:registration|reg)\s*(?:no|num|#)?[.:\s]*([a-zA-Z0-9/\-]+)\b", re.IGNORECASE
    )
    YEAR_REGEX = re.compile(r"\b(19\d{2}|20\d{2})\b")
    MARKS_FRACTION_REGEX = re.compile(r"\b(\d{3,4})\s*[/]\s*(\d{3,4})\b")
    OBTAINED_REGEX = re.compile(
        r"\b(?:marks\s*obtained|obtained\s*marks|marks)[.:\s]*(\d{3,4})\b", re.IGNORECASE
    )
    TOTAL_REGEX = re.compile(r"\b(?:out\s*of|total\s*marks|total)[.:\s]*(\d{3,4})\b", re.IGNORECASE)
    GRADE_REGEX = re.compile(
        r"\b(?:grade|division)[.:\s]*([a-fA-F]\+?|1st|2nd|3rd)", re.IGNORECASE
    )

    BOARDS = [
        "BISE Lahore",
        "BISE Rawalpindi",
        "BISE Multan",
        "BISE Faisalabad",
        "BISE Gujranwala",
        "BISE Sargodha",
        "BISE Sahiwal",
        "BISE Bahawalpur",
        "BISE D.G. Khan",
        "BISE Karachi",
        "BISE Hyderabad",
        "BISE Sukkur",
        "BISE Larkana",
        "BISE Mirpurkhas",
        "BISE Peshawar",
        "BISE Swat",
        "BISE Abbottabad",
        "BISE Bannu",
        "BISE Mardan",
        "BISE Kohat",
        "BISE Quetta",
        "BISE Mirpur",
        "Federal Board",
        "FBISE",
    ]

    def supports_raw_text(self, raw_text: str) -> bool:
        lower = raw_text.lower()
        if "matric" in lower or "secondary school certificate" in lower or "ssc" in lower:
            return True
        return any(board.lower() in lower for board in self.BOARDS)

    def _extract_board(self, text: str) -> Union[str, None]:
        for board in self.BOARDS:
            if board.lower() in text.lower():
                return board

        m = re.search(
            r"board\s+of\s+intermediate\s+(?:and|&)\s+secondary\s+education[,\s]+([a-zA-Z\s]+)",
            text,
            re.IGNORECASE,
        )
        if m:
            city = m.group(1).strip().split()[0]
            return f"BISE {city.capitalize()}"
        return None

    def _extract_names(self, lines: list[str]) -> tuple[Union[str, None], Union[str, None]]:
        student_name: Union[str, None] = None
        father_name: Union[str, None] = None

        for i, line in enumerate(lines):
            clean = line.strip()
            lower = clean.lower()

            if any(kw in lower for kw in ["certified that", "student name", "candidate name", "name:"]):
                parts = clean.split(":", 1)
                val = parts[1].strip() if len(parts) > 1 else ""
                if not val and i + 1 < len(lines):
                    val = lines[i + 1].strip()
                val = re.sub(r"^(certified that|mr\.|ms\.|miss|syed|syeda)\s+", "", val, flags=re.IGNORECASE).strip()
                if val and not student_name:
                    student_name = val

            if any(kw in lower for kw in ["son of", "daughter of", "father name", "father's name"]):
                parts = clean.split(":", 1)
                val = parts[1].strip() if len(parts) > 1 else ""
                if not val and i + 1 < len(lines):
                    val = lines[i + 1].strip()
                val = re.sub(r"^(son of|daughter of|s/o|d/o|mr\.)\s+", "", val, flags=re.IGNORECASE).strip()
                if val and not father_name:
                    father_name = val

        return student_name, father_name

    def _extract_group(self, text: str) -> Union[str, None]:
        lower = text.lower()
        if "science" in lower:
            return "Science"
        if "humanities" in lower or "arts" in lower:
            return "Humanities"
        if "general" in lower:
            return "General"
        return None

    def extract(self, items: list[OCRResultItem], raw_text: str) -> MatricCertificateData:
        lines = [item.text for item in items] if items else [line.strip() for line in raw_text.splitlines() if line.strip()]

        board = self._extract_board(raw_text)
        student_name, father_name = self._extract_names(lines)
        group = self._extract_group(raw_text)

        roll_match = self.ROLL_REGEX.search(raw_text)
        roll_num = roll_match.group(1) if roll_match else None

        reg_match = self.REG_REGEX.search(raw_text)
        reg_num = reg_match.group(1) if reg_match else None

        year_match = self.YEAR_REGEX.search(raw_text)
        passing_year = int(year_match.group(1)) if year_match else None

        obtained_marks: Union[float, None] = None
        total_marks: Union[float, None] = None

        frac_match = self.MARKS_FRACTION_REGEX.search(raw_text)
        if frac_match:
            obtained_marks = float(frac_match.group(1))
            total_marks = float(frac_match.group(2))
        else:
            obt_m = self.OBTAINED_REGEX.search(raw_text)
            if obt_m:
                obtained_marks = float(obt_m.group(1))
            tot_m = self.TOTAL_REGEX.search(raw_text)
            if tot_m:
                total_marks = float(tot_m.group(1))

        if not total_marks and obtained_marks:
            total_marks = 1100.0  # Standard total marks in Pakistani Matric certificates

        percentage: Union[float, None] = None
        if obtained_marks is not None and total_marks:
            percentage = round((obtained_marks / total_marks) * 100.0, 2)

        grade_match = self.GRADE_REGEX.search(raw_text)
        grade = grade_match.group(1).upper() if grade_match else None

        found_fields = sum(
            1
            for f in [roll_num, student_name, father_name, board, passing_year, obtained_marks]
            if f is not None
        )
        confidence = round(found_fields / 6.0, 2)

        return MatricCertificateData(
            roll_number=roll_num,
            registration_number=reg_num,
            student_name=student_name,
            father_name=father_name,
            board=board,
            passing_year=passing_year,
            total_marks=total_marks,
            obtained_marks=obtained_marks,
            percentage=percentage,
            grade=grade,
            group=group,
            confidence=confidence,
            raw_text=raw_text,
        )
