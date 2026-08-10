---
name: job-market-monitor
description: Run Judy job-market monitoring workflows safely.
---

# Job Market Monitor Skill

Use these invocations:

- `/job-market-monitor daily` -> `python -m job_market_monitor.run daily`
- `/job-market-monitor full-refresh` -> `python -m job_market_monitor.run full-refresh`
- `/job-market-monitor add-source <URL>` -> `python -m job_market_monitor.run add-source <URL>`
- `/job-market-monitor explain <job_id>` -> `python -m job_market_monitor.run explain <job_id>`
- `/job-market-monitor dashboard` -> `python -m job_market_monitor.run dashboard`
- `/job-market-monitor draft <job_id>` -> `python -m job_market_monitor.run draft <job_id>`
- `/job-market-monitor open-latest` -> `scripts/open_latest_dashboard.sh`

Behavior:
- Reads normalized candidate profile and config.
- Runs offline-safe collection, filtering, matching, SQLite update, and report generation.
- Returns generated digest/dashboard paths and concise result counts.
- Never submits applications, emails, or external forms.
