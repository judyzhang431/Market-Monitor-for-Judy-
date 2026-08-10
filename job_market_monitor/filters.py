from __future__ import annotations

from datetime import date, timedelta
from .models import Job, TRACK_CN_ACADEMIA


def is_recent_or_active(job: Job, today: date) -> bool:
    if job.status.lower() not in {"active", "open"}:
        return False
    if not job.date_posted:
        return True
    try:
        posted = date.fromisoformat(job.date_posted)
    except ValueError:
        return True
    return posted >= today - timedelta(days=45) or job.status.lower() == "open"


def is_excluded(job: Job) -> bool:
    title_lower = (job.title or "").lower()
    if any(x in title_lower for x in ["intern", "internship", "student", "assistant"]):
        return True
    if any(x in title_lower for x in ["clinical", "nurse", "physician", "lab technician"]):
        return True
    if job.track == TRACK_CN_ACADEMIA and any(x in title_lower for x in ["postdoc", "博士后"]):
        return True
    return False


def normalize_salary(raw: str) -> str:
    return raw.strip() if raw and raw.strip() else "Not disclosed / 未披露"
