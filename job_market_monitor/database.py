from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable


SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
  job_id TEXT PRIMARY KEY,
  track TEXT NOT NULL,
  title TEXT NOT NULL,
  organization TEXT NOT NULL,
  department TEXT,
  city TEXT,
  state_province TEXT,
  country TEXT,
  work_mode TEXT,
  official_url TEXT,
  discovery_url TEXT,
  source_name TEXT,
  date_posted TEXT,
  application_deadline TEXT,
  first_seen TEXT,
  last_seen TEXT,
  status TEXT,
  appointment_type TEXT,
  employment_type TEXT,
  term_length TEXT,
  salary_raw TEXT,
  salary_min TEXT,
  salary_max TEXT,
  currency TEXT,
  pay_period TEXT,
  china_base_salary TEXT,
  china_annual_package TEXT,
  china_housing_allowance TEXT,
  china_startup_funds TEXT,
  china_other_benefits TEXT,
  required_degree TEXT,
  preferred_degree TEXT,
  required_methods TEXT,
  preferred_methods TEXT,
  required_years TEXT,
  visa_language TEXT,
  visa_sponsorship TEXT,
  description TEXT,
  summary TEXT,
  overall_fit_score INTEGER,
  confidence TEXT,
  fit_band TEXT,
  hard_barriers TEXT,
  matched_experience TEXT,
  gaps TEXT,
  recommended_action TEXT,
  component_domain INTEGER,
  component_methods INTEGER,
  component_transferable INTEGER,
  component_degree INTEGER,
  component_seniority INTEGER,
  component_practicality INTEGER,
  discipline_judgment_cn TEXT
);
CREATE TABLE IF NOT EXISTS source_health (
  run_date TEXT,
  source_name TEXT,
  organization TEXT,
  careers_url TEXT,
  adapter_type TEXT,
  official_status TEXT,
  success INTEGER,
  jobs_found INTEGER,
  details TEXT
);
"""


def connect(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def upsert_jobs(conn: sqlite3.Connection, job_records: Iterable[dict], run_date: str) -> tuple[int, int]:
    inserted = 0
    updated = 0
    for rec in job_records:
        exists = conn.execute("SELECT job_id FROM jobs WHERE job_id = ?", (rec["job_id"],)).fetchone()
        if exists:
            updated += 1
            conn.execute(
                """
                UPDATE jobs SET
                  track=:track,title=:title,organization=:organization,department=:department,
                  city=:city,state_province=:state_province,country=:country,work_mode=:work_mode,
                  official_url=:official_url,discovery_url=:discovery_url,source_name=:source_name,
                  date_posted=:date_posted,application_deadline=:application_deadline,last_seen=:last_seen,
                  status=:status,appointment_type=:appointment_type,employment_type=:employment_type,
                  term_length=:term_length,salary_raw=:salary_raw,salary_min=:salary_min,salary_max=:salary_max,
                  currency=:currency,pay_period=:pay_period,china_base_salary=:china_base_salary,
                  china_annual_package=:china_annual_package,china_housing_allowance=:china_housing_allowance,
                  china_startup_funds=:china_startup_funds,china_other_benefits=:china_other_benefits,
                  required_degree=:required_degree,preferred_degree=:preferred_degree,
                  required_methods=:required_methods,preferred_methods=:preferred_methods,
                  required_years=:required_years,visa_language=:visa_language,visa_sponsorship=:visa_sponsorship,
                  description=:description,summary=:summary,overall_fit_score=:overall_fit_score,
                  confidence=:confidence,fit_band=:fit_band,hard_barriers=:hard_barriers,
                  matched_experience=:matched_experience,gaps=:gaps,recommended_action=:recommended_action,
                  component_domain=:component_domain,component_methods=:component_methods,
                  component_transferable=:component_transferable,component_degree=:component_degree,
                  component_seniority=:component_seniority,component_practicality=:component_practicality,
                  discipline_judgment_cn=:discipline_judgment_cn
                WHERE job_id=:job_id
                """,
                {**rec, "last_seen": run_date},
            )
        else:
            inserted += 1
            conn.execute(
                """
                INSERT INTO jobs (
                  job_id,track,title,organization,department,city,state_province,country,work_mode,
                  official_url,discovery_url,source_name,date_posted,application_deadline,
                  first_seen,last_seen,status,appointment_type,employment_type,term_length,
                  salary_raw,salary_min,salary_max,currency,pay_period,
                  china_base_salary,china_annual_package,china_housing_allowance,china_startup_funds,china_other_benefits,
                  required_degree,preferred_degree,required_methods,preferred_methods,required_years,visa_language,visa_sponsorship,
                  description,summary,overall_fit_score,confidence,fit_band,hard_barriers,matched_experience,gaps,recommended_action,
                  component_domain,component_methods,component_transferable,component_degree,component_seniority,component_practicality,
                  discipline_judgment_cn
                ) VALUES (
                  :job_id,:track,:title,:organization,:department,:city,:state_province,:country,:work_mode,
                  :official_url,:discovery_url,:source_name,:date_posted,:application_deadline,
                  :first_seen,:last_seen,:status,:appointment_type,:employment_type,:term_length,
                  :salary_raw,:salary_min,:salary_max,:currency,:pay_period,
                  :china_base_salary,:china_annual_package,:china_housing_allowance,:china_startup_funds,:china_other_benefits,
                  :required_degree,:preferred_degree,:required_methods,:preferred_methods,:required_years,:visa_language,:visa_sponsorship,
                  :description,:summary,:overall_fit_score,:confidence,:fit_band,:hard_barriers,:matched_experience,:gaps,:recommended_action,
                  :component_domain,:component_methods,:component_transferable,:component_degree,:component_seniority,:component_practicality,
                  :discipline_judgment_cn
                )
                """,
                {**rec, "first_seen": run_date, "last_seen": run_date},
            )
    conn.commit()
    return inserted, updated
