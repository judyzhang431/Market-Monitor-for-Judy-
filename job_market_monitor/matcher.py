from __future__ import annotations

from .models import Job, TRACK_CN_ACADEMIA


def score_job(job: Job) -> dict:
    desc = f"{job.title} {job.description}".lower()
    domain = 5
    methods = 5
    transferable = 8
    degree = 8
    seniority = 7
    practicality = 5

    if any(k in desc for k in ["child", "early childhood", "maternal", "health", "education", "rural", "agric"]):
        domain = 20
    if any(k in desc for k in ["rct", "randomized", "causal", "evaluation", "stata", "did", "2sls"]):
        methods = 20
    if any(k in desc for k in ["project management", "field", "survey", "stakeholder"]):
        transferable = 13
    if "phd" in desc or "doctor" in desc:
        degree = 14
    if any(k in desc for k in ["senior director", "15+ years"]):
        seniority = 2
    if "us citizen" in desc or "security clearance" in desc or job.visa_sponsorship == "explicit_no":
        practicality = 0
    elif job.visa_sponsorship == "explicit_yes":
        practicality = 10

    total = domain + methods + transferable + degree + seniority + practicality
    fit_band = "Strong" if total >= 75 else "Possible" if total >= 60 else "Stretch" if total >= 45 else "Below"

    if job.track == TRACK_CN_ACADEMIA and not job.discipline_judgment_cn:
        discipline_judgment_cn = "2) Research fit strong; formal discipline code uncertain"
    else:
        discipline_judgment_cn = job.discipline_judgment_cn

    return {
        "overall_fit_score": total,
        "component_domain": domain,
        "component_methods": methods,
        "component_transferable": transferable,
        "component_degree": degree,
        "component_seniority": seniority,
        "component_practicality": practicality,
        "fit_band": fit_band,
        "discipline_judgment_cn": discipline_judgment_cn,
    }
