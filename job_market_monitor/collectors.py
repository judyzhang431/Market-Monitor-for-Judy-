from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import Job
from .filters import normalize_salary


DEFAULT_FIELDS = {
    "department": "",
    "city": "",
    "state_province": "",
    "country": "",
    "work_mode": "Location not disclosed",
    "discovery_url": "",
    "date_posted": "",
    "application_deadline": "",
    "status": "active",
    "appointment_type": "",
    "employment_type": "",
    "term_length": "",
    "salary_raw": "Not disclosed / 未披露",
    "salary_min": "",
    "salary_max": "",
    "currency": "",
    "pay_period": "",
    "china_base_salary": "",
    "china_annual_package": "",
    "china_housing_allowance": "",
    "china_startup_funds": "",
    "china_other_benefits": "",
    "required_degree": "",
    "preferred_degree": "",
    "required_methods": "",
    "preferred_methods": "",
    "required_years": "",
    "visa_language": "",
    "visa_sponsorship": "possible_or_unknown",
    "description": "",
    "summary": "",
    "hard_barriers": "",
    "matched_experience": "",
    "gaps": "",
    "recommended_action": "Review",
    "confidence": "Medium confidence",
    "discipline_judgment_cn": "",
}


def load_sources(sources_path: Path) -> list[dict[str, Any]]:
    import yaml

    with sources_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return [s for s in data.get("sources", []) if s.get("enabled", True)]


def collect_jobs_from_fixture(repo_root: Path, source: dict[str, Any]) -> list[Job]:
    fixture_path = repo_root / "data" / "fixtures" / "jobs.json"
    with fixture_path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    selected = [j for j in raw if j.get("track") == source["track"] and j.get("organization") == source["organization"]]
    jobs: list[Job] = []
    for item in selected:
        values = {**DEFAULT_FIELDS, **item}
        values["source_name"] = source["organization"]
        values["salary_raw"] = normalize_salary(values["salary_raw"])
        jobs.append(Job(**values))
    return jobs
