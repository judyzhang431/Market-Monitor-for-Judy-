from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import yaml


@dataclass
class AppConfig:
    repo_root: Path
    desktop_root: Path
    summary_dir: Path
    industry_dir: Path
    us_academia_dir: Path
    cn_academia_dir: Path
    timezone: str


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_app_config(repo_root: Path) -> AppConfig:
    schedule = load_yaml(repo_root / "config" / "schedule.yml")
    desktop_root = Path(os.environ.get("JMM_DESKTOP_ROOT", "/Users/judyzhang/Desktop"))
    job_root = desktop_root / "Job"
    return AppConfig(
        repo_root=repo_root,
        desktop_root=desktop_root,
        summary_dir=Path(os.environ.get("JMM_SUMMARY_DIR", str(job_root / "Summary_everyday"))),
        industry_dir=Path(os.environ.get("JMM_INDUSTRY_DIR", str(job_root / "Industry"))),
        us_academia_dir=Path(os.environ.get("JMM_US_ACADEMIA_DIR", str(job_root / "USAacademia"))),
        cn_academia_dir=Path(os.environ.get("JMM_CN_ACADEMIA_DIR", str(job_root / "CNAcademia"))),
        timezone=schedule.get("timezone", "America/Los_Angeles"),
    )
