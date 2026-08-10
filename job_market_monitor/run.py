from __future__ import annotations

from argparse import ArgumentParser
from datetime import date
from html import escape
from pathlib import Path
import sqlite3

from .candidate import load_candidate_profile
from .collectors import load_sources, collect_jobs_from_fixture
from .config import load_app_config
from .database import connect, upsert_jobs
from .filters import is_excluded, is_recent_or_active
from .matcher import score_job
from .reports import write_markdown_reports, write_source_health, write_profile_match_notes, write_dashboard_html, fetch_active_shortlist
from .models import TRACK_ORDER
from .server import run_server


def ensure_desktop_paths(cfg):
    if not cfg.desktop_root.exists():
        raise RuntimeError(
            f"Required path {cfg.desktop_root} is not available. This run must execute on Claude Code Desktop/local with access to /Users/judyzhang/Desktop."
        )
    cfg.industry_dir.mkdir(parents=True, exist_ok=True)
    cfg.us_academia_dir.mkdir(parents=True, exist_ok=True)
    cfg.cn_academia_dir.mkdir(parents=True, exist_ok=True)
    cfg.summary_dir.mkdir(parents=True, exist_ok=True)


def run_pipeline(repo_root: Path, mode: str = "daily", dry_run: bool = False) -> dict:
    cfg = load_app_config(repo_root)
    ensure_desktop_paths(cfg)

    db_path = repo_root / "data" / "jobs.sqlite3"
    conn = connect(db_path)
    _ = load_candidate_profile(repo_root / "data" / "candidate_profile.yml")

    sources = load_sources(repo_root / "config" / "sources.yml")
    run_date = date.today().isoformat()

    all_jobs = []
    conn.execute("DELETE FROM source_health")
    for source in sources:
        jobs_found = 0
        success = 1
        details = "ok"
        try:
            jobs = collect_jobs_from_fixture(repo_root, source)
            filtered = []
            for job in jobs:
                if is_excluded(job) or not is_recent_or_active(job, date.today()):
                    continue
                scoring = score_job(job)
                rec = job.to_record()
                rec.update(scoring)
                filtered.append(rec)
            all_jobs.extend(filtered)
            jobs_found = len(filtered)
        except Exception as exc:
            success = 0
            details = str(exc)
        conn.execute(
            "INSERT INTO source_health (run_date,source_name,organization,careers_url,adapter_type,official_status,success,jobs_found,details) VALUES (?,?,?,?,?,?,?,?,?)",
            (run_date, source["organization"], source["organization"], source["careers_url"], source["adapter_type"], source["official_status"], success, jobs_found, details),
        )

    inserted, updated = upsert_jobs(conn, all_jobs, run_date)

    latest_path, daily_path, basename, counts = write_markdown_reports(conn, repo_root / "reports", cfg.summary_dir, cfg.timezone)
    write_source_health(conn, repo_root / "reports")
    write_profile_match_notes(repo_root / "reports")

    grouped = fetch_active_shortlist(conn)
    sections = []
    for track in TRACK_ORDER:
        rows = grouped.get(track, [])
        sections.append(f"<details open><summary><b>{track}</b> ({len(rows)})</summary>")
        if not rows:
            sections.append("<p>No qualifying new or updated positions found in this run.</p></details>")
            continue
        sections.append("<table><thead><tr><th>Rank</th><th>Company / University</th><th>Position and Department / Lab</th><th>Base City and Work Mode</th><th>Salary / Package</th><th>Posted / Deadline</th><th>Match</th><th>Highlighted Matching Experience</th><th>Gaps / Eligibility</th><th>Web Sources</th></tr></thead><tbody>")
        for idx, r in enumerate(rows, start=1):
            loc = ", ".join([x for x in [r["city"], r["state_province"], r["country"]] if x]) or "Location not disclosed"
            loc = f"{loc} · {r['work_mode'] or 'Location not disclosed'}"
            pos = escape(r["title"]) + (f"<br>{escape(r['department'])}" if r["department"] else "")
            source = f"<a href='{escape(r['official_url'])}' target='_blank'>Official posting</a><br>Checked {run_date}"
            matched = escape(r["matched_experience"] or "").replace(";", "<br>")
            gaps = escape((r["hard_barriers"] or "") + ("; " if r["hard_barriers"] and r["gaps"] else "") + (r["gaps"] or "")).replace(";", "<br>")
            sections.append(
                f"<tr class='selectable' data-job-id='{escape(r['job_id'])}'><td>{idx}</td><td>{escape(r['organization'])}</td><td>{pos}</td><td>{escape(loc)}</td><td>{escape(r['salary_raw'])}</td><td>{escape(r['date_posted'])} / {escape(r['application_deadline'])}</td><td>{r['overall_fit_score']}/100 · {escape(r['fit_band'])} · {escape(r['confidence'])} · {escape(r['recommended_action'])}</td><td>{matched}</td><td>{gaps}</td><td>{source}</td></tr>"
            )
        sections.append("</tbody></table></details>")

    dashboard_path = write_dashboard_html(cfg.summary_dir, basename, "\n".join(sections))

    # Save matching markdown/csv with dashboard basename
    (cfg.summary_dir / f"{dashboard_path.stem}.md").write_text((repo_root / "reports" / "daily" / f"{run_date}.md").read_text(encoding="utf-8"), encoding="utf-8")
    (cfg.summary_dir / f"{dashboard_path.stem}.csv").write_text((repo_root / "reports" / "latest.csv").read_text(encoding="utf-8"), encoding="utf-8")

    if dry_run:
        conn.close()
        return {"inserted": inserted, "updated": updated, "latest": str(latest_path), "daily": str(daily_path), "dashboard": str(dashboard_path), "counts": counts}

    conn.close()
    return {"inserted": inserted, "updated": updated, "latest": str(latest_path), "daily": str(daily_path), "dashboard": str(dashboard_path), "counts": counts}


def main():
    parser = ArgumentParser()
    parser.add_argument("command", choices=["daily", "full-refresh", "dashboard", "draft", "open-latest", "serve", "explain", "add-source"])
    parser.add_argument("arg", nargs="?")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    cfg = load_app_config(repo_root)

    if args.command in {"daily", "full-refresh"}:
        result = run_pipeline(repo_root, args.command, dry_run=args.dry_run)
        print(result)
    elif args.command == "dashboard":
        run_server(repo_root / "data" / "jobs.sqlite3", cfg.industry_dir, cfg.us_academia_dir, cfg.cn_academia_dir, cfg.timezone)
    elif args.command == "serve":
        run_server(repo_root / "data" / "jobs.sqlite3", cfg.industry_dir, cfg.us_academia_dir, cfg.cn_academia_dir, cfg.timezone)
    elif args.command == "open-latest":
        import subprocess
        latest = sorted(cfg.summary_dir.glob("Industry-*_USAcademia-*_CNAcademia-*.html"))
        if not latest:
            raise SystemExit("No dashboard found")
        subprocess.run(["open", str(latest[-1])], check=False)
        print(str(latest[-1]))
    elif args.command == "draft":
        if not args.arg:
            raise SystemExit("job_id required")
        conn = sqlite3.connect(str(repo_root / "data" / "jobs.sqlite3"))
        conn.row_factory = sqlite3.Row
        from .drafts import generate_draft

        out, _ = generate_draft(conn, args.arg, cfg.industry_dir, cfg.us_academia_dir, cfg.cn_academia_dir, cfg.timezone)
        print(str(out))
    elif args.command == "explain":
        if not args.arg:
            raise SystemExit("job_id required")
        conn = sqlite3.connect(str(repo_root / "data" / "jobs.sqlite3"))
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (args.arg,)).fetchone()
        if not row:
            raise SystemExit("not found")
        print({k: row[k] for k in row.keys()})
    elif args.command == "add-source":
        if not args.arg:
            raise SystemExit("URL required")
        print("Add source by editing config/sources.yml with required fields: track, organization, careers URL, official/discovery status, adapter type, search terms, enabled, notes.")


if __name__ == "__main__":
    main()
