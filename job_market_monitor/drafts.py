from __future__ import annotations

from datetime import datetime
from pathlib import Path
import os
import re
import sqlite3
import tempfile
from zoneinfo import ZoneInfo

from .models import TRACK_INDUSTRY, TRACK_US_ACADEMIA, TRACK_CN_ACADEMIA


def sanitize_filename(value: str) -> str:
    value = re.sub(r"[\\/:*?\"<>|]", "_", value.strip())
    value = re.sub(r"\s+", "_", value)
    return value or "Organization"


def folder_for_track(track: str, industry_dir: Path, us_academia_dir: Path, cn_academia_dir: Path) -> Path:
    if track == TRACK_INDUSTRY:
        return industry_dir
    if track == TRACK_US_ACADEMIA:
        return us_academia_dir
    if track == TRACK_CN_ACADEMIA:
        return cn_academia_dir
    raise ValueError("Unknown track")


def build_email_draft(row: sqlite3.Row, now_date: str) -> str:
    contact = "Not listed—do not guess"
    contact_email = "Not listed—do not guess"
    portal_only = "Apply through official portal; no verified email contact listed" if contact_email.startswith("Not listed") else "Application email"
    subject = f"Application inquiry: {row['title']}"
    intro = "Dear Hiring Team," if row["track"] != TRACK_CN_ACADEMIA else "尊敬的招聘团队："
    body = (
        f"{intro}\n\n"
        f"I am writing regarding the {row['title']} position at {row['organization']}. "
        "My background includes early childhood development and health human capital research, "
        "including cluster-randomized intervention work, quantitative impact evaluation, and cross-institutional project management in China and the U.S. "
        "I believe this aligns with your needs in applied social science research.\n\n"
        "Thank you for your consideration. I would value the opportunity to discuss fit further.\n"
    )
    if row["track"] == TRACK_CN_ACADEMIA:
        body = (
            "尊敬的招聘团队：\n\n"
            f"我写信申请贵单位的{row['title']}岗位。本人拥有农业经济管理博士背景，长期从事早期儿童发展与健康人力资本研究，"
            "并具备随机对照评估、调查研究与跨机构项目协作经验。"
            "如岗位方向契合，期待进一步沟通。\n\n"
            "感谢审阅。\n"
        )
    return (
        f"Organization: {row['organization']}\n"
        f"Position: {row['title']}\n"
        f"Job ID: {row['job_id']}\n"
        f"Official posting: {row['official_url']}\n"
        f"Contact person: {contact}\n"
        f"Contact email: {contact_email}\n"
        f"Suggested subject: {subject}\n"
        f"Suggested use: {portal_only}\n\n"
        f"{body}\n"
        "Attachments/checklist:\n"
        "- CV\n- Cover letter draft\n- Writing sample (if requested)\n\n"
        f"Generated on: {now_date} (America/Los_Angeles). Review before sending.\n"
    )


def write_draft_atomic(folder: Path, filename_base: str, content: str) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{filename_base}.txt"
    idx = 2
    while path.exists():
        path = folder / f"{filename_base}_{idx}.txt"
        idx += 1
    fd, tmp = tempfile.mkstemp(dir=str(folder), prefix=".tmp_draft_", suffix=".txt")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
    return path


def generate_draft(conn: sqlite3.Connection, job_id: str, industry_dir: Path, us_academia_dir: Path, cn_academia_dir: Path, tz_name: str) -> tuple[Path, str]:
    row = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
    if not row:
        raise KeyError("job_id not found")
    today = datetime.now(ZoneInfo(tz_name)).date().isoformat()
    folder = folder_for_track(row["track"], industry_dir, us_academia_dir, cn_academia_dir)
    name = sanitize_filename(row["organization"])
    content = build_email_draft(row, today)
    out = write_draft_atomic(folder, f"{name}_{today}", content)
    return out, content
