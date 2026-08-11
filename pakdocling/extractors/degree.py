"""University Degree and Transcript Extractor for Pakistani Higher Education Institutes."""

import re
from typing import Union

from pakdocling.extractors.base import BaseExtractor
from pakdocling.models.schema import UniversityDegreeData
from pakdocling.ocr.engine import OCRResultItem


class DegreeExtractor(BaseExtractor):
    """Extractor for Pakistani University Degrees, Diplomas, and Transcripts."""

    CGPA_REGEX = re.compile(
        r"\b(?:cgpa|gpa|cumulativ[e\s]+gpa)[.:\s]*([0-3]\.\d{1,2}|4\.00?)\b", re.IGNORECASE
    )
    CGPA_FRACTION_REGEX = re.compile(r"\b([0-3]\.\d{1,2}|4\.00?)\s*[/]\s*(4\.00?|5\.00?)\b")
    REG_REGEX = re.compile(
        r"\b(?:registration|reg|roll)\s*(?:no|num|#)?[.:\s]*([a-zA-Z0-9/\-]+)\b", re.IGNORECASE
    )
    YEAR_REGEX = re.compile(r"\b(19\d{2}|20\d{2})\b")
    DEGREE_TITLE_REGEX = re.compile(
        r"\b(bachelor\s+of\s+[a-zA-Z\s]+|master\s+of\s+[a-zA-Z\s]+|doctor\s+of\s+[a-zA-Z\s]+|bs\s+[a-zA-Z\s]+|ms\s+[a-zA-Z\s]+|m\.?phil\s+[a-zA-Z\s]+|ph\.?d\s+[a-zA-Z\s]+)\b",
        re.IGNORECASE,
    )

    def _extract_degree_title(self, text: str) -> tuple[Union[str, None], Union[str, None]]:
        for line in text.splitlines():
            line_clean = line.strip()
            m = self.DEGREE_TITLE_REGEX.search(line_clean)
            if m:
                full_title = m.group(1).strip()
                # Stop if title captured trailing keywords
                full_title = re.split(
                    r"\s+(graduation|year|cgpa|date|roll|reg|marks)\b",
                    full_title,
                    flags=re.IGNORECASE,
                )[0].strip()
                major: Union[str, None] = None
                if " in " in full_title.lower():
                    parts = re.split(r"\s+in\s+", full_title, flags=re.IGNORECASE)
                    major = parts[1].strip()
                return full_title, major
        return None, None

    UNIVERSITIES = [
        "National University of Sciences and Technology",
        "NUST",
        "FAST National University",
        "NUCES",
        "Quaid-i-Azam University",
        "QAU",
        "Lahore University of Management Sciences",
        "LUMS",
        "University of the Punjab",
        "UET Lahore",
        "UET Peshawar",
        "UET Taxila",
        "COMSATS University",
        "Aga Khan University",
        "GIKI",
        "Ghulam Ishaq Khan Institute",
        "Institute of Business Administration",
        "IBA Karachi",
        "Allama Iqbal Open University",
        "AIOU",
        "Air University",
        "Bahria University",
        "National University of Modern Languages",
        "NUML",
        "PIEAS",
        "NED University",
        "Dow University of Health Sciences",
    ]

    def supports_raw_text(self, raw_text: str) -> bool:
        lower = raw_text.lower()
        if any(
            kw in lower
            for kw in [
                "degree",
                "transcript",
                "bachelor",
                "master",
                "cgpa",
                "university",
                "conferred upon",
            ]
        ):
            return True
        return any(uni.lower() in lower for uni in self.UNIVERSITIES)

    def _extract_university(self, text: str) -> Union[str, None]:
        for uni in self.UNIVERSITIES:
            if uni.lower() in text.lower():
                return uni

        m = re.search(
            r"\b(university\s+of\s+[a-zA-Z\s]+|institute\s+of\s+[a-zA-Z\s]+)\b", text, re.IGNORECASE
        )
        if m:
            return m.group(1).strip()
        return None

    def _extract_names(self, lines: list[str]) -> tuple[Union[str, None], Union[str, None]]:
        student_name: Union[str, None] = None
        father_name: Union[str, None] = None

        for i, line in enumerate(lines):
            clean = line.strip()
            lower = clean.lower()

            if any(
                kw in lower for kw in ["conferred upon", "awarded to", "certified that", "name:"]
            ):
                parts = clean.split(":", 1)
                val = parts[1].strip() if len(parts) > 1 else ""
                if not val and i + 1 < len(lines):
                    val = lines[i + 1].strip()
                val = re.sub(
                    r"^(conferred upon|awarded to|certified that|mr\.|ms\.|miss)\s+",
                    "",
                    val,
                    flags=re.IGNORECASE,
                ).strip()
                if val and not student_name:
                    student_name = val

            if any(kw in lower for kw in ["son of", "daughter of", "father name", "father's name"]):
                parts = clean.split(":", 1)
                val = parts[1].strip() if len(parts) > 1 else ""
                if not val and i + 1 < len(lines):
                    val = lines[i + 1].strip()
                val = re.sub(
                    r"^(son of|daughter of|s/o|d/o|mr\.)\s+", "", val, flags=re.IGNORECASE
                ).strip()
                if val and not father_name:
                    father_name = val

        return student_name, father_name

    def _extract_cgpa(self, text: str) -> tuple[Union[float, None], Union[float, None]]:
        frac = self.CGPA_FRACTION_REGEX.search(text)
        if frac:
            return float(frac.group(1)), float(frac.group(2))

        m = self.CGPA_REGEX.search(text)
        if m:
            return float(m.group(1)), 4.0

        return None, 4.0

    def extract(self, items: list[OCRResultItem], raw_text: str) -> UniversityDegreeData:
        lines = (
            [item.text for item in items]
            if items
            else [line.strip() for line in raw_text.splitlines() if line.strip()]
        )

        uni_name = self._extract_university(raw_text)
        student_name, father_name = self._extract_names(lines)
        cgpa, max_cgpa = self._extract_cgpa(raw_text)
        degree_title, major = self._extract_degree_title(raw_text)

        reg_match = self.REG_REGEX.search(raw_text)
        reg_num = reg_match.group(1) if reg_match else None

        years = self.YEAR_REGEX.findall(raw_text)
        grad_year = int(years[-1]) if years else None

        found_fields = sum(
            1
            for f in [student_name, uni_name, degree_title, cgpa or grad_year, reg_num]
            if f is not None
        )
        confidence = round(found_fields / 5.0, 2)

        return UniversityDegreeData(
            student_name=student_name,
            father_name=father_name,
            roll_number=reg_num,
            registration_number=reg_num,
            degree_title=degree_title,
            major=major,
            university_name=uni_name,
            graduation_year=grad_year,
            award_date=str(grad_year) if grad_year else None,
            cgpa=cgpa,
            max_cgpa=max_cgpa if max_cgpa else 4.0,
            confidence=confidence,
            raw_text=raw_text,
        )
