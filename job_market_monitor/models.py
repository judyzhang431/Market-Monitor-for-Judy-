from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import date
from hashlib import sha1
import re
from typing import Any


TRACK_INDUSTRY = "US Industry and Non-Academic Research"
TRACK_US_ACADEMIA = "US Academia, Including Postdocs"
TRACK_CN_ACADEMIA = "China Academia, Excluding Postdocs"
TRACK_ORDER = [TRACK_INDUSTRY, TRACK_US_ACADEMIA, TRACK_CN_ACADEMIA]


@dataclass
class Job:
    track: str
    title: str
    organization: str
    department: str
    city: str
    state_province: str
    country: str
    work_mode: str
    official_url: str
    discovery_url: str
    source_name: str
    date_posted: str
    application_deadline: str
    status: str
    appointment_type: str
    employment_type: str
    term_length: str
    salary_raw: str
    salary_min: str
    salary_max: str
    currency: str
    pay_period: str
    china_base_salary: str
    china_annual_package: str
    china_housing_allowance: str
    china_startup_funds: str
    china_other_benefits: str
    required_degree: str
    preferred_degree: str
    required_methods: str
    preferred_methods: str
    required_years: str
    visa_language: str
    visa_sponsorship: str
    description: str
    summary: str
    hard_barriers: str
    matched_experience: str
    gaps: str
    recommended_action: str
    confidence: str
    discipline_judgment_cn: str

    def canonical_location(self) -> str:
        parts = [self.city, self.state_province, self.country]
        return ", ".join([p for p in parts if p])

    def stable_job_id(self) -> str:
        norm = "|".join(
            [
                normalize_text(self.organization),
                normalize_text(self.title),
                normalize_text(self.canonical_location()),
                normalize_url(self.official_url),
            ]
        )
        digest = sha1(norm.encode("utf-8")).hexdigest()[:16]
        return f"job_{digest}"

    def to_record(self) -> dict[str, Any]:
        record = asdict(self)
        record["job_id"] = self.stable_job_id()
        return record


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "").strip().lower())


def normalize_url(url: str) -> str:
    return re.sub(r"/$", "", (url or "").strip().lower())


def today_iso() -> str:
    return date.today().isoformat()
