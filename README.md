# Market Monitor for Judy

Automated three-track job-market monitoring with SQLite state, markdown/csv reports, local interactive dashboard, and explicit click-to-generate email drafts.

## Requirements

- Python 3.11+
- `pip install -r requirements.txt`
- Local/Desktop run for default output paths under `/Users/judyzhang/Desktop/Job/*`

## First run

```bash
cd /home/runner/work/Market-Monitor-for-Judy-/Market-Monitor-for-Judy-
pip install -r requirements.txt
python -m job_market_monitor.run full-refresh --dry-run
```

## Daily run

```bash
python -m job_market_monitor.run daily
```

Or non-interactive:

```bash
claude -p "/job-market-monitor daily"
```

## Dashboard

```bash
scripts/open_latest_dashboard.sh
```

Server binds to `127.0.0.1:8765` only.

## Add source

Edit `config/sources.yml` with:
- track
- organization
- careers_url
- official_status
- adapter_type
- search_terms
- enabled
- notes

## Scheduling

Default schedule: 8:00 AM `America/Los_Angeles` (`config/schedule.yml`).

### 1) Claude Code Desktop local scheduled task (recommended)
Use a Desktop local schedule invoking `/job-market-monitor daily`. This mode can write directly to `/Users/judyzhang/Desktop/Job/*`.

### 2) Claude Code cloud Routine (optional)
Cloud routine cannot write directly to `/Users/judyzhang/Desktop`. Use repository/cloud storage outputs, then sync locally separately.

### 3) Manual non-interactive run

```bash
claude -p "/job-market-monitor daily"
```

## Troubleshooting

- If `/Users/judyzhang/Desktop` is unavailable, the run exits with a clear error.
- Source failures are listed in `reports/source_health.md`.
- Salary is never estimated; missing values are labeled `Not disclosed / 未披露`.
