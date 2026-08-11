"""CNIC extractor for old green and new blue Smart Card formats."""

import re
from typing import Union

from pakdocling.extractors.base import BaseExtractor
from pakdocling.models.schema import CNICData, CNICVariant, Gender
from pakdocling.ocr.engine import OCRResultItem


class CNICExtractor(BaseExtractor):
    """Extractor for Pakistani Computerized National Identity Cards (CNIC)."""

    CNIC_REGEX = re.compile(r"\b(\d{5})[-\s]?(\d{7})[-\s]?(\d{1})\b")
    DATE_REGEX = re.compile(r"\b(\d{2})[./-](\d{2})[./-](\d{4})\b")

    def supports_raw_text(self, raw_text: str) -> bool:
        """Check if text contains CNIC indicators or 13-digit CNIC pattern."""
        if self.CNIC_REGEX.search(raw_text):
            return True
        keywords = ["identity card", "cnic", "national identity", "nadra", "pakistan"]
        lower = raw_text.lower()
        return sum(1 for kw in keywords if kw in lower) >= 2

    def _extract_cnic_number(self, text: str) -> Union[str, None]:
        match = self.CNIC_REGEX.search(text)
        if match:
            return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
        return None

    def _infer_gender(self, cnic_number: Union[str, None], text: str) -> Gender:
        lower = text.lower()
        if "female" in lower or "gender f" in lower or "gender: f" in lower:
            return Gender.FEMALE
        if "male" in lower or "gender m" in lower or "gender: m" in lower:
            return Gender.MALE

        if cnic_number:
            digits = cnic_number.replace("-", "").strip()
            if len(digits) == 13 and digits[-1].isdigit():
                last_digit = int(digits[-1])
                return Gender.MALE if last_digit % 2 != 0 else Gender.FEMALE

        return Gender.UNKNOWN

    def _detect_variant(self, text: str) -> CNICVariant:
        lower = text.lower()
        if any(kw in lower for kw in ["smart", "nicop", "chip", "identity card"]):
            return CNICVariant.NEW_BLUE
        if any(kw in lower for kw in ["identity", "pakistan", "green"]):
            return CNICVariant.OLD_GREEN
        return CNICVariant.NEW_BLUE

    def _extract_dates(
        self, lines: list[str]
    ) -> tuple[Union[str, None], Union[str, None], Union[str, None]]:
        dob: Union[str, None] = None
        issue: Union[str, None] = None
        expiry: Union[str, None] = None

        all_dates: list[str] = []
        for line in lines:
            for m in self.DATE_REGEX.finditer(line):
                all_dates.append(f"{m.group(1)}.{m.group(2)}.{m.group(3)}")

        for i, line in enumerate(lines):
            line_lower = line.lower()
            search_match = self.DATE_REGEX.search(line)
            found_date = (
                f"{search_match.group(1)}.{search_match.group(2)}.{search_match.group(3)}"
                if search_match
                else None
            )

            if "birth" in line_lower or "dob" in line_lower:
                if found_date:
                    dob = found_date
                elif i + 1 < len(lines):
                    next_m = self.DATE_REGEX.search(lines[i + 1])
                    if next_m:
                        dob = f"{next_m.group(1)}.{next_m.group(2)}.{next_m.group(3)}"

            elif "issue" in line_lower:
                if found_date:
                    issue = found_date
                elif i + 1 < len(lines):
                    next_m = self.DATE_REGEX.search(lines[i + 1])
                    if next_m:
                        issue = f"{next_m.group(1)}.{next_m.group(2)}.{next_m.group(3)}"

            elif "expiry" in line_lower:
                if "lifetime" in line_lower:
                    expiry = "Lifetime"
                elif found_date:
                    expiry = found_date
                elif i + 1 < len(lines):
                    next_m = self.DATE_REGEX.search(lines[i + 1])
                    if next_m:
                        expiry = f"{next_m.group(1)}.{next_m.group(2)}.{next_m.group(3)}"

        # Fallback date assignments if keywords missed
        if not dob and len(all_dates) >= 1:
            dob = all_dates[0]
        if not issue and len(all_dates) >= 2:
            issue = all_dates[1]
        if not expiry and len(all_dates) >= 3:
            expiry = all_dates[2]

        if not expiry and "lifetime" in "\n".join(lines).lower():
            expiry = "Lifetime"

        return dob, issue, expiry

    def _extract_names(
        self, lines: list[str]
    ) -> tuple[Union[str, None], Union[str, None], Union[str, None], Union[str, None]]:
        name: Union[str, None] = None
        father_name: Union[str, None] = None
        husband_name: Union[str, None] = None
        country: Union[str, None] = "Pakistan"

        for i, line in enumerate(lines):
            line_clean = line.strip()
            line_lower = line_clean.lower()

            if "father name" in line_lower or "father's name" in line_lower:
                parts = line_clean.split(":", 1)
                val = parts[1].strip() if len(parts) > 1 else ""
                if not val and i + 1 < len(lines):
                    val = lines[i + 1].strip()
                if val and not father_name:
                    father_name = val

            elif "husband name" in line_lower or "husband's name" in line_lower:
                parts = line_clean.split(":", 1)
                val = parts[1].strip() if len(parts) > 1 else ""
                if not val and i + 1 < len(lines):
                    val = lines[i + 1].strip()
                if val and not husband_name:
                    husband_name = val

            elif line_lower.startswith("name") or "name:" in line_lower:
                # Exclude father name or husband name lines
                if not any(k in line_lower for k in ["father", "husband"]):
                    parts = line_clean.split(":", 1)
                    val = parts[1].strip() if len(parts) > 1 else ""
                    if not val and i + 1 < len(lines):
                        val = lines[i + 1].strip()
                    if val and not name:
                        name = val

            elif "country of stay" in line_lower:
                parts = line_clean.split(":", 1)
                if len(parts) > 1 and parts[1].strip():
                    country = parts[1].strip()

        return name, father_name, husband_name, country

    def extract(self, items: list[OCRResultItem], raw_text: str) -> CNICData:
        lines = (
            [item.text for item in items]
            if items
            else [line.strip() for line in raw_text.splitlines() if line.strip()]
        )

        cnic_num = self._extract_cnic_number(raw_text)
        variant = self._detect_variant(raw_text)
        gender = self._infer_gender(cnic_num, raw_text)
        dob, issue, expiry = self._extract_dates(lines)
        name, father_name, husband_name, country = self._extract_names(lines)

        # Confidence calculation
        found_fields = sum(
            1
            for f in [cnic_num, name, father_name or husband_name, dob, issue, expiry]
            if f is not None
        )
        confidence = round(found_fields / 6.0, 2)

        return CNICData(
            cnic_number=cnic_num,
            variant=variant,
            full_name=name,
            father_name=father_name,
            husband_name=husband_name,
            gender=gender,
            country_of_stay=country,
            date_of_birth=dob,
            date_of_issue=issue,
            date_of_expiry=expiry,
            confidence=confidence,
            raw_text=raw_text,
        )
