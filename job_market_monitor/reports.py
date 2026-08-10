from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from html import escape
from pathlib import Path
import csv
import os
import sqlite3
import tempfile
from zoneinfo import ZoneInfo

from .models import TRACK_ORDER

TABLE_HEADER = "| Rank | Company / University | Position and Department / Lab | Base City and Work Mode | Salary / Package | Posted / Deadline | Match | Highlighted Matching Experience | Gaps / Eligibility | Web Sources |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"


def fetch_active_shortlist(conn: sqlite3.Connection):
    rows = conn.execute(
        """
        SELECT * FROM jobs
        WHERE status IN ('active','open')
        ORDER BY
          CASE WHEN hard_barriers != '' THEN 1 ELSE 0 END,
          overall_fit_score DESC,
          CASE WHEN application_deadline = '' THEN 1 ELSE 0 END,
          application_deadline ASC,
          date_posted DESC
        """
    ).fetchall()
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["track"]].append(row)
    return grouped


def _row_to_md(rank: int, row, checked_date: str) -> str:
    pos = row["title"] + (f"<br>{row['department']}" if row["department"] else "")
    loc_parts = [row["city"], row["state_province"], row["country"]]
    loc = ", ".join([p for p in loc_parts if p]) or "Location not disclosed"
    loc = f"{loc} · {row['work_mode'] or 'Location not disclosed'}"
    salary = row["salary_raw"] or "Not disclosed / 未披露"
    posted_deadline = f"{row['date_posted'] or 'Unknown'} / {row['application_deadline'] or 'Unknown'}"
    match = f"{row['overall_fit_score']}/100 · {row['fit_band']} · {row['confidence']} · {row['recommended_action']}"
    evidence = (row["matched_experience"] or "").replace(";", "<br>")
    gaps = (row["hard_barriers"] + ("<br>" if row["hard_barriers"] and row["gaps"] else "") + (row["gaps"] or "")).strip() or "None noted"
    source = f"[Official posting]({row['official_url']})"
    if row["discovery_url"]:
        source += f"<br>[Discovery]({row['discovery_url']})"
    source += f"<br>Checked {checked_date}"
    return f"| {rank} | {row['organization']} | {pos} | {loc} | {salary} | {posted_deadline} | {match} | {evidence} | {gaps} | {source} |\n"


def write_markdown_reports(conn: sqlite3.Connection, reports_dir: Path, summary_dir: Path, tz_name: str) -> tuple[Path, Path, str, dict[str, int]]:
    grouped = fetch_active_shortlist(conn)
    la_now = datetime.now(ZoneInfo(tz_name))
    run_date = la_now.date().isoformat()

    latest = ["# Complete Active Shortlist\n"]
    daily = ["# Daily Digest\n"]
    counts = {track: len(grouped.get(track, [])) for track in TRACK_ORDER}

    summary_line = (
        f"New strong/possible/stretch by track: {counts[TRACK_ORDER[0]]}/{counts[TRACK_ORDER[1]]}/{counts[TRACK_ORDER[2]]}. "
        "Changed jobs: 0. Deadlines within 7 days: 0; within 14 days: 0. Sources failed or blocked: see source health."
    )
    daily.append(summary_line + "\n")

    for heading in TRACK_ORDER:
        latest.append(f"\n## {heading}\n")
        daily.append(f"\n## {heading}\n")
        rows = grouped.get(heading, [])
        if not rows:
            latest.append("No qualifying new or updated positions found in this run.\n")
            daily.append("No qualifying new or updated positions found in this run.\n")
            continue
        latest.append(TABLE_HEADER)
        daily.append(TABLE_HEADER)
        for idx, row in enumerate(rows, start=1):
            line = _row_to_md(idx, row, run_date)
            latest.append(line)
            daily.append(line)

    reports_dir.mkdir(parents=True, exist_ok=True)
    (reports_dir / "daily").mkdir(parents=True, exist_ok=True)
    latest_path = reports_dir / "latest.md"
    daily_path = reports_dir / "daily" / f"{run_date}.md"
    latest_path.write_text("".join(latest), encoding="utf-8")
    daily_path.write_text("".join(daily), encoding="utf-8")

    basename = f"Industry-{counts[TRACK_ORDER[0]]}_USAcademia-{counts[TRACK_ORDER[1]]}_CNAcademia-{counts[TRACK_ORDER[2]]}_{run_date}"
    _write_csv(conn, reports_dir / "latest.csv")
    return latest_path, daily_path, basename, counts


def _write_csv(conn: sqlite3.Connection, path: Path) -> None:
    rows = conn.execute("SELECT * FROM jobs WHERE status IN ('active','open')").fetchall()
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(rows[0].keys())
        for row in rows:
            writer.writerow([row[k] for k in row.keys()])


def write_source_health(conn: sqlite3.Connection, reports_dir: Path) -> Path:
    rows = conn.execute("SELECT * FROM source_health ORDER BY source_name").fetchall()
    lines = ["# Source Health\n", "| Source | Organization | URL | Adapter | Status | Jobs | Notes |\n", "| --- | --- | --- | --- | --- | --- | --- |\n"]
    for r in rows:
        status = "Success" if r["success"] else "Failed/Blocked"
        lines.append(f"| {r['source_name']} | {r['organization']} | {r['careers_url']} | {r['adapter_type']} | {status} | {r['jobs_found']} | {r['details']} |\n")
    path = reports_dir / "source_health.md"
    path.write_text("".join(lines), encoding="utf-8")
    return path


def write_profile_match_notes(reports_dir: Path) -> Path:
    content = """# Profile Match Notes

- **RCT / impact evaluation** -> led or co-led field research and a cluster-randomized parenting intervention.
- **ECD / child development** -> postdoctoral research on early childhood development.
- **Health human capital / policy** -> research topics include health human capital and caregiver mental health.
- **Applied quantitative methods** -> OLS/2SLS, DID/fixed effects, clustered data, survey analysis, Stata.
- **Field operations / management** -> project management, protocol design, recruitment/training, cross-country team coordination.
- **Bilingual context** -> Chinese and English proficiency with China/U.S. institutional collaboration.
"""
    path = reports_dir / "profile_match_notes.md"
    path.write_text(content, encoding="utf-8")
    return path


def write_dashboard_html(summary_dir: Path, basename: str, grouped_tables_markdown: str) -> Path:
    summary_dir.mkdir(parents=True, exist_ok=True)
    path = summary_dir / f"{basename}.html"
    html = f"""<!doctype html>
<html><head><meta charset='utf-8'><title>{escape(basename)}</title>
<style>
body{{font-family:Arial,sans-serif;margin:16px}} table{{border-collapse:collapse;width:100%}} td,th{{border:1px solid #ccc;padding:6px;vertical-align:top}} tr.selectable:hover{{background:#f4f8ff;cursor:pointer}} .panel{{border:1px solid #999;padding:10px;margin-top:12px}}
</style></head>
<body>
<h1>Daily Interactive Summary</h1>
<p>{escape(basename)}</p>
<div id='tables'>{grouped_tables_markdown}</div>
<div class='panel'>
<h2>Job details</h2>
<pre id='details'>Select a row to preview.</pre>
<button id='generateBtn' disabled>Generate email draft (.txt)</button>
<button id='openBtn' disabled>Open official posting</button>
<button id='copyBtn' disabled>Copy email draft</button>
<button id='folderBtn' disabled>Open destination folder</button>
<div id='status'></div>
</div>
<script>
let selectedJobId = null;
let selectedDraft = "";
document.querySelectorAll('tr[data-job-id]').forEach((row)=>{{
  row.addEventListener('click', async()=>{{
    selectedJobId = row.dataset.jobId;
    const r = await fetch(`/api/job/${{encodeURIComponent(selectedJobId)}}`);
    const data = await r.json();
    document.getElementById('details').textContent = JSON.stringify(data, null, 2);
    document.getElementById('generateBtn').disabled = false;
    document.getElementById('openBtn').disabled = false;
    document.getElementById('folderBtn').disabled = false;
  }});
}});
document.getElementById('generateBtn').addEventListener('click', async()=>{{
  const r = await fetch('/api/generate-draft', {{method:'POST', headers:{{'Content-Type':'application/json'}}, body:JSON.stringify({{job_id:selectedJobId}})}});
  const data = await r.json();
  selectedDraft = data.content || "";
  document.getElementById('copyBtn').disabled = !selectedDraft;
  document.getElementById('status').textContent = data.message + (data.path ? ` (${{data.path}})` : '');
}});
document.getElementById('openBtn').addEventListener('click', async()=>{{
  if(!selectedJobId) return;
  const r = await fetch(`/api/open-posting/${{encodeURIComponent(selectedJobId)}}`);
  const data = await r.json();
  if(data.url) window.open(data.url,'_blank');
}});
document.getElementById('copyBtn').addEventListener('click', async()=>{{
  if(selectedDraft) await navigator.clipboard.writeText(selectedDraft);
}});
document.getElementById('folderBtn').addEventListener('click', async()=>{{
  const r = await fetch(`/api/open-folder/${{encodeURIComponent(selectedJobId)}}`);
  const data = await r.json();
  document.getElementById('status').textContent = data.message;
}});
</script>
</body></html>
"""
    if path.exists():
        existing = path.read_text(encoding="utf-8", errors="ignore")
        if "Daily Interactive Summary" not in existing:
            suffix = 2
            while True:
                candidate = summary_dir / f"{basename}_{suffix}.html"
                if not candidate.exists():
                    path = candidate
                    break
                suffix += 1
    fd, tmp = tempfile.mkstemp(dir=str(summary_dir), prefix=".tmp_dashboard_", suffix=".html")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(html)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
    return path
