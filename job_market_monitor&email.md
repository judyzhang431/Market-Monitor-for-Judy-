# Claude Code Job-Market Monitor for Judy (Zhidi) Zhang

This file contains a ready-to-paste build prompt for Claude Code, a daily-run prompt, and setup commands. The complete file is under Claude's 30,000-character prompt limit; paste the master prompt in Section 2 when building the monitor.

## 1. Start the project

Run these commands in Terminal:

```bash
mkdir -p ~/job-market-monitor
cd ~/job-market-monitor
claude
```

Then paste the full master prompt below into Claude Code.

## 2. Master build prompt for Claude Code

```text
Build a maintainable, automated job-market monitoring system for me. Work in the current folder and implement the system, not merely describe it. First inspect the environment, then create a short plan and proceed. Ask a question only if you are genuinely blocked; otherwise use the defaults in this prompt.

## Candidate

Name: Zhidi (Judy) Zhang / 张之的
Personal website: https://zhidizhang.com/
Current institutional profile: https://sccei.fsi.stanford.edu/people/zhidi-zhang

Use those public pages as profile sources, supplemented by the verified summary below. Save a normalized candidate profile locally so daily runs do not depend on repeatedly scraping the website. Never invent credentials, publications, software skills, or work authorization.

Verified profile summary:

- PhD in Management of Agricultural Economy / Agricultural Business from Zhejiang University.
- Visiting Postdoctoral Scholar at Stanford University's Rural Education Action Program / Stanford Center on China's Economy and Institutions.
- Postdoctoral researcher in early childhood development at Zhejiang University.
- Former visiting researcher in psychology at UCLA.
- Main domains: early childhood development, health human capital, adverse childhood experiences, intergenerational transmission, development economics, rural China, caregiver mental health, maternal employment, and aging/cognition.
- Led or co-led field research and a cluster-randomized parenting intervention; experience includes project management, research protocols, survey design, field-team recruitment and training, data collection, quantitative analysis, mixed-methods research, academic writing, and coordination across Chinese and U.S. research teams.
- Methods that may be matched when the job description calls for them: randomized controlled trials, impact/program evaluation, causal-inference-oriented applied research, OLS/2SLS, fixed effects/DID, clustered data, survey research, qualitative interviews, mixed methods, and Stata.
- Publication/work pipeline includes early childhood intervention participation, conditional cash transfers, caregiver ACEs, maternal occupation and child development, caregiver mental health, and presbyopia/cognition/family support.
- Languages: Chinese and English.
- U.S. work authorization must be checked. Treat employer sponsorship as required or needing confirmation; never assume that current J-1 status automatically authorizes a future position.
- Do not describe the candidate as holding an MPH, MD, psychology PhD, clinical license, software-engineering background, or machine-learning specialization.

## Search tracks

Create exactly three top-level tracks.

### A. US industry and non-academic research

Include private companies, research/consulting organizations, NGOs, foundations, think tanks, international organizations, and appropriate government research roles. Search beyond exact degree names.

Priority role families:

- Economist, applied economist, health economist, education economist, agricultural economist
- Research scientist, social scientist, behavioral scientist, quantitative researcher
- Program evaluator, impact-evaluation researcher, monitoring/evaluation/learning researcher
- Public-health researcher, health-policy researcher, health-services or outcomes researcher
- ECD, education, family, child-policy, maternal/child-health, or social-policy researcher
- Research program manager, research project manager, evaluation manager
- Agribusiness, food-systems, rural-development, or agricultural-policy researcher/analyst
- Social-impact, philanthropy, global-development, or evidence-policy researcher

Do not include generic software engineering, laboratory biomedical science, clinical-care, or ML engineering jobs unless the description explicitly accepts applied social science/economics/public health research experience and the core requirements are plausible for this candidate.

Priority employer groups to configure, using official career pages whenever possible:

- Technology and large employers: Amazon, Google, Microsoft, Meta, Apple, Uber, LinkedIn, Salesforce
- Research/evaluation/consulting: RAND, Mathematica, Abt Global, RTI International, American Institutes for Research, NORC, Westat, MDRC, Child Trends, Urban Institute, Brookings, ICF, FHI 360
- Child/ECD/education: ZERO TO THREE, Sesame Workshop, Teaching Strategies, ETS, Pearson, education research organizations and child-policy institutes
- Agriculture/food/development: Cargill, Corteva, Bayer Crop Science, Syngenta, John Deere, USDA/ERS, IFPRI, World Bank, J-PAL, Innovations for Poverty Action
- Foundations and international/public-interest organizations: Gates Foundation and other evidence, health, education, or child-development funders

This list is a starting configuration, not a claim that every employer currently has a suitable role.

### B. US academia, including postdoctoral positions

Include:

- Postdoctoral fellow/scholar/associate
- Research associate, research scientist, staff scientist in social science, research faculty
- Assistant professor, lecturer, teaching/research faculty when the discipline and record are plausible
- Lab, center, institute, and grant-funded project positions

Search relevant schools/departments/centers in agricultural and applied economics, economics, public policy, public health, population health, maternal and child health, education, human development, psychology, social policy, and global development.

Configure discovery from official university/lab career pages plus appropriate academic boards such as HigherEdJobs, AcademicJobsOnline, AEA JOE, EconJobMarket, Chronicle, Nature Careers, APHA career listings, SRCD career listings, and postdoctoral listings. Aggregators are for discovery; verify every shortlisted opening on the employer's official page.

Prioritize centers/labs with ECD, development economics, population health, health policy, education policy, rural development, impact evaluation, or China research. Include universities nationally, not only a fixed list.

### C. China academia, excluding postdoctoral positions

Exclude every 博士后/postdoc opening, student position, internship, and position that is clearly temporary postdoctoral training.

Include appropriate:

- 助理教授、讲师、预聘制教师、教学科研岗
- 特聘研究员、特聘副研究员、副研究员、研究科学家/研究岗
- 青年人才、百人计划/青年百人、准聘/长聘教职 and other independent faculty/research appointments
- Positions advertised at open rank when a recent PhD is genuinely eligible

Search https://www.gaoxiaojob.com/ for discovery and verify results on each university's official 人事处/人才招聘/学院 website. Expand nationwide across universities and research institutes.

Use Chinese and English discipline/keyword variants, including:

- 农业经济管理、农林经济管理、农业经济学、应用经济学、发展经济学、劳动经济学、人口资源与环境经济学
- 公共卫生、卫生经济学、健康经济学、健康政策与管理、社会医学与卫生事业管理、妇幼保健、全球健康
- 儿童发展、早期儿童发展、学前教育、发展心理学、家庭研究、社会政策、人口学
- 农村发展、共同富裕、健康人力资本、项目评估、政策评估、随机对照试验、因果推断、调查研究

For China, distinguish three different judgments:

1. The formal discipline/degree requirement is clearly eligible.
2. Research fit is strong but the formal discipline code is uncertain.
3. The degree requirement is a likely mismatch.

Do not reject a position merely because it is housed in a school of public health or education if the notice accepts economics, management, social science, or related disciplines. Do flag notices that strictly require an MPH/MD/public-health PhD, education PhD, psychology PhD, or a specific Chinese discipline code.

## Source and collection rules

Create `config/sources.yml` so sources can be added, disabled, or reprioritized without changing code. Each source needs: track, organization, careers URL, official/discovery status, adapter type, search terms, enabled flag, and notes.

Use this priority order:

1. Public official ATS endpoints, job feeds, structured data, or employer search APIs
2. JSON-LD and stable HTML on official job pages
3. Official sitemaps/RSS feeds
4. Search-engine discovery restricted to official employer domains
5. Approved aggregator listings, followed by official-page verification

Support common ATS patterns when practical, including Greenhouse, Lever, Ashby, and Workday. Isolate every source adapter so one changed website does not break the complete run.

Follow robots.txt, site terms, and reasonable rate limits. Use caching, retries with backoff, descriptive user-agent information, and low concurrency. Do not bypass CAPTCHA, login walls, bot protection, or access controls. Do not scrape LinkedIn or another site in a way that violates its terms. If a source is blocked, record it in the coverage report and use compliant official-domain web discovery instead.

“All jobs” means all active jobs found in the enabled, documented source set and search queries. Never claim complete coverage of the entire internet.

## Hard eligibility and exclusion rules

- Only include openings that are still active. Capture the posting date and deadline when available.
- Prefer jobs posted in the last 45 days; retain older jobs only when the official page confirms they remain open.
- Exclude expired, closed, filled, duplicated, internship, undergraduate/graduate assistant, and unrelated clinical or laboratory positions.
- China track: exclude all postdocs.
- US tracks: capture `visa_sponsorship` as `explicit_yes`, `possible_or_unknown`, or `explicit_no`, with the exact supporting sentence or source. Do not infer sponsorship from employer size.
- Flag U.S. citizenship/permanent residency, security clearance, unrestricted work authorization, clinical license, or other hard barriers.
- Flag positions requiring substantially more seniority than the candidate has.
- Do not exclude a job because the candidate lacks one preferred qualification; distinguish “required” from “preferred.”

## Data model and deduplication

Use SQLite as the durable state store and export human-readable CSV/Markdown. Create a stable job ID from normalized organization, title, location, and canonical URL. Track URL redirects and duplicate postings across boards.

Store at least:

- job_id, track, title, organization, department/lab, city, state/province, country, remote/hybrid/on-site
- canonical official URL, discovery URL, source name
- date_posted, application_deadline, first_seen, last_seen, status
- appointment type, full-time/part-time, permanent/fixed-term, term length
- salary_raw, salary_min, salary_max, currency, pay_period
- for China separately: base salary, annual package, housing/settling allowance, research startup funds, and `待遇面议` when applicable
- required degree/discipline, preferred degree/discipline, required methods, preferred methods
- required years/seniority, visa/work-authorization language
- normalized job-description text and a short factual summary
- overall_fit_score, confidence, fit_band, hard_barriers, matched_experience, gaps, and recommended_action

Salary rules:

- Report the exact employer-listed salary or package and its period/currency.
- If absent, write `Not disclosed / 未披露`.
- Never fabricate or silently estimate salary.
- If an external estimate is added later, place it in a separate clearly labeled estimated field with its source; never mix it with employer-listed compensation.

## Matching and ranking

Implement transparent, track-aware scoring from 0 to 100. Store component scores and explanations. Suggested components:

- Domain/research-topic fit: 25
- Methods and research-design fit: 25
- Transferable project/field/program-management fit: 15
- Degree/discipline eligibility: 15
- Seniority and publication-stage fit: 10
- Work-authorization/location/appointment practicality: 10

Hard barriers must be visible and may cap the final score even when topical fit is high. Use:

- Strong match: 75–100
- Possible match: 60–74
- Stretch: 45–59
- Below 45: retain in the database for audit but omit from the main daily digest

For each shortlisted position, create an evidence table with two columns:

- Job requirement or responsibility, quoted or closely paraphrased
- Matching candidate experience, using only verified facts

Highlight up to five strongest matches and up to three meaningful gaps. Good candidate evidence can include ECD research, health human capital, rural China, RCT/impact evaluation, quantitative and mixed methods, survey/field-team leadership, cross-institutional project management, academic writing/publication, and Chinese-English context. Do not use vague claims such as “excellent fit” without evidence.

Give extra attention to descriptions containing combinations of:

- economics/social science/public health/education/child development
- causal inference, program evaluation, RCT, survey research, longitudinal research, health/education policy
- applied research plus stakeholder or field-program management
- China, rural development, agriculture, maternal/child health, family policy, human capital

Identify likely gaps such as mandatory Python/R/SQL, advanced ML, clinical credentials, a different required doctorate, U.S. work authorization without sponsorship, or many years of industry experience. A listed preferred skill is not a hard barrier.

## Outputs

Create these outputs on every successful run:

- `reports/latest.md`: complete current shortlist, separated into the three tracks
- `reports/latest.csv`: flat spreadsheet-ready version
- `reports/daily/YYYY-MM-DD.md`: daily digest
- `reports/source_health.md`: sources checked, success/failure, last successful check, jobs found, and coverage limitations
- `reports/profile_match_notes.md`: reusable mapping between Judy's verified experience and common job requirements

The daily digest must begin with a compact summary:

- Number of newly found strong/possible/stretch matches by track
- Previously seen jobs with material changes
- Deadlines within 7 days and within 14 days
- Sources that failed or were blocked

Then show only new jobs, materially updated jobs, and jobs closing soon. Present the results as **three separate Markdown tables in this exact order**:

1. `US Industry and Non-Academic Research`
2. `US Academia, Including Postdocs`
3. `China Academia, Excluding Postdocs`

Do not combine the three tracks into one table. Use the following column structure for every table:

| Rank | Company / University | Position and Department / Lab | Base City and Work Mode | Salary / Package | Posted / Deadline | Match | Highlighted Matching Experience | Gaps / Eligibility | Web Sources |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Column rules:

- `Rank`: ranking within that track, beginning with 1.
- `Company / University`: official organization name; for China, preserve the official Chinese name and add an English name only when verified.
- `Position and Department / Lab`: preserve the original job title, then show the department, lab, institute, or team on a second line when available.
- `Base City and Work Mode`: city, state/province, country, plus on-site/hybrid/remote. Write `Location not disclosed` rather than guessing.
- `Salary / Package`: exact employer-listed salary and period/currency. For Chinese academic positions, separately label annual salary, housing/settling allowance, research startup funds, and other benefits when stated. Otherwise write `Not disclosed / 未披露`.
- `Posted / Deadline`: use exact dates. Preserve `Open until filled / 招满即止` when that is the employer's wording.
- `Match`: show `score/100`, fit band, confidence, and recommended action, for example `82/100 · Strong · High confidence · Apply now`.
- `Highlighted Matching Experience`: show three to five concise, evidence-based matches. Each item must connect a job-description requirement to a verified candidate experience, for example `RCT evaluation → led a cluster-randomized ECD program`. Use `<br>` to place separate matches on separate lines within the Markdown table cell. Bold the requirement keywords, not the entire cell.
- `Gaps / Eligibility`: show required-versus-preferred gaps; U.S. visa/sponsorship status for U.S. jobs; and formal degree/discipline eligibility for Chinese academic jobs. Put any hard barrier first.
- `Web Sources`: include descriptive Markdown links rather than bare URLs. The first link must be the verified official job posting. Optionally add the official careers-search page and the discovery source. If salary or sponsorship evidence comes from a different official page, link it separately and label it. Add `Checked YYYY-MM-DD`.

Example formatting for the source cell: `[Official posting](URL)<br>[Careers page](URL)<br>Checked 2026-08-10`.

If a track has no qualifying results, keep its heading and write `No qualifying new or updated positions found in this run.` Do not create fictional placeholder jobs.

In `reports/latest.md`, show the complete active shortlist in the same three-table structure. In the daily digest, use the same structure but include only new, materially updated, or closing-soon positions.

## Local interactive dashboard and click-to-generate email drafts

In addition to Markdown and CSV reports, create a local interactive HTML dashboard for macOS. This is the primary user-facing daily summary. It must run locally through a small backend bound only to `127.0.0.1`; do not expose it to the public internet.

Use these exact folder mappings:

- Table 1, US industry/non-academic research → `/Users/judyzhang/Desktop/Job/Industry`
- Table 2, US academia including postdocs → `/Users/judyzhang/Desktop/Job/USAacademia`
- Table 3, China academia excluding postdocs → `/Users/judyzhang/Desktop/Job/CNAcademia`
- Daily interactive summaries → `/Users/judyzhang/Desktop/Job/Summary_everyday`

On setup, create these four directories if they do not exist. Before writing, verify that `/Users/judyzhang/Desktop` is actually available. If this project is running in a cloud/container environment without access to that path, stop with a clear message; do not silently write to a different location.

### Dashboard behavior

- Display three clearly separated, collapsible tables matching the three tracks and column rules above.
- Make every genuine job row selectable. Clicking a row should open a detail panel containing the complete job summary, match evidence, gaps, salary, deadline, and verified sources.
- The detail panel must have an explicit `Generate email draft (.txt)` button. A single row click should preview/select the job; generating a file should require clicking this button so accidental row clicks do not create unwanted files.
- Also provide `Open official posting`, `Copy email draft`, and `Open destination folder` actions.
- After draft generation, show the exact file path and a success/error message without reloading the complete table.
- The dashboard must never send an email, submit an application, upload a résumé, or contact an employer.
- Provide `scripts/open_latest_dashboard.sh` or an equivalent simple command that starts the local server, opens the most recent summary in the default browser, and avoids starting duplicate server processes.

### Daily summary naming

Count the actual job rows shown in each of the three daily tables. Save the primary HTML dashboard in `/Users/judyzhang/Desktop/Job/Summary_everyday` using:

`Industry-{table1_count}_USAcademia-{table2_count}_CNAcademia-{table3_count}_{YYYY-MM-DD}.html`

Example:

`Industry-6_USAcademia-9_CNAcademia-12_2026-08-10.html`

Use the local calendar date in `America/Los_Angeles`. Do not count headings or `no results` messages as rows. Save matching Markdown and CSV summaries with the same basename when practical. If the exact filename already exists, update it atomically when it represents the same daily run; otherwise preserve the existing file and append `_2`, `_3`, and so on rather than overwriting unrelated user content.

### Email-draft folder routing and filenames

When the user clicks `Generate email draft (.txt)`, look up the selected `job_id` in SQLite and route it by its stored track. Never accept a client-provided filesystem path.

Filename pattern:

`{sanitized_company_or_university_name}_{YYYY-MM-DD}.txt`

Examples:

- `RAND_2026-08-10.txt`
- `Stanford_University_2026-08-10.txt`
- `浙江大学_2026-08-10.txt`

Sanitize characters that are unsafe in macOS filenames while preserving readable English or Chinese names. The date is the draft-generation date in `America/Los_Angeles`. If another draft for the same organization already exists on that date, preserve the original and create `_2`, `_3`, and so on. Do not overwrite a draft silently.

### Email-draft content

Every `.txt` draft must contain:

- `Organization:`
- `Position:`
- `Job ID:`
- `Official posting:`
- `Contact person:` and `Contact email:` when explicitly listed; otherwise `Not listed—do not guess`
- `Suggested subject:`
- `Suggested use:` either `Application email`, `Inquiry email`, or `Apply through official portal; no verified email contact listed`
- A polished email body
- A short `Attachments/checklist` section
- `Generated on:` date and a note that the draft must be reviewed before sending

Tailor the body to the selected position using only verified candidate experience and the actual job description. Mention two or three of the strongest matches rather than copying the complete match table. Never invent a personal connection, recipient, publication, skill, visa status, or attachment.

Use a concise professional U.S. style for Tables 1 and 2. For Table 2, emphasize research alignment, methods, and the relevant lab/center. For Table 3, draft in formal Chinese unless the advertisement is explicitly English-language; mention the agricultural-economics doctorate, ECD/health-human-capital research, and Stanford/Zhejiang research experience only when relevant.

If the posting requires applying exclusively through a portal and provides no email address, still create the requested `.txt` draft but place `Apply through official portal; no verified email contact listed` prominently at the top.

### Dashboard safety and testing

- Bind the dashboard to localhost only and use a job ID lookup rather than raw path parameters.
- Escape job-description text before rendering to prevent HTML/script injection.
- Validate track-to-folder routing and filename sanitization.
- Write drafts atomically and test collision suffixes.
- Add tests confirming that Table 1, Table 2, and Table 3 drafts go only to their specified directories.
- Add tests confirming that clicking/previewing a row does not create a file; only the explicit generation action may create one.

Sort within each track by: hard eligibility, fit score, deadline urgency, then posting recency.

Use bilingual labels where useful for China positions, but preserve the original Chinese job title and compensation wording.

## Project structure and quality

Build a small, understandable project. Prefer Python, SQLite, YAML, and standard HTML/JSON parsing. Add dependencies only when they materially improve reliability. Keep secrets out of source control and provide `.env.example` if notification credentials may be added.

Create:

- a README with installation, first run, daily run, adding a source, and troubleshooting
- a candidate-profile file
- configuration files for sources, search terms, scoring, and schedule defaults
- modular collectors/parsers, normalization, deduplication, matching, and report generation
- cached test fixtures and tests that do not depend on live network access
- structured logs and useful exit codes
- a dry-run option

Validate output schemas and test deduplication, salary handling, expired-job exclusion, China-postdoc exclusion, and required-vs-preferred qualifications.

Do not push to GitHub, create external accounts, send email, or store credentials without asking me first. It is fine to prepare optional instructions for email delivery or a private GitHub repository.

## Claude Code skill

Create a project skill at:

`.claude/skills/job-market-monitor/SKILL.md`

It should support these natural invocations:

- `/job-market-monitor daily`
- `/job-market-monitor full-refresh`
- `/job-market-monitor add-source <URL>`
- `/job-market-monitor explain <job_id>`
- `/job-market-monitor dashboard`
- `/job-market-monitor draft <job_id>`
- `/job-market-monitor open-latest`

The skill should read the normalized candidate profile and configuration, run the appropriate scripts, inspect failures, and return the path to the generated digest plus a concise result summary. Keep the SKILL.md concise and put detail in referenced files/scripts.

Important: do not set `disable-model-invocation: true`, because scheduled tasks must be able to invoke this skill. Make it user-invocable and safe for unattended daily runs. It must never apply to a job, submit a form, or contact an employer.

## Scheduling support

Set the default daily schedule to 8:00 AM in `America/Los_Angeles`, but make it configurable. Prepare instructions for:

1. Claude Code Desktop local scheduled task (recommended when the computer is usually on)
2. Claude Code cloud Routine (recommended when the task must run while the computer is off; requires a repository and appropriate network access)
3. A manual non-interactive run using `claude -p`

Do not use `/loop` as the permanent solution because it is session-scoped. A daily run must compare against the SQLite state from prior runs and report only meaningful changes.

Because the required output folders are under `/Users/judyzhang/Desktop`, the default implementation and daily schedule must use Claude Code Desktop/local execution. A cloud Routine cannot directly write to the Mac Desktop. Document a cloud alternative only as an optional separate workflow that saves to repository/cloud storage and later syncs to the Mac; never claim that a cloud run wrote directly to these local paths.

## Definition of done

The build is complete only when:

- the three search tracks and exclusions are configured
- a test/dry run completes
- reports are generated with organization, city, salary, official link, and evidence-based experience matches
- duplicates and expired jobs are handled
- China postdocs are excluded
- missing salaries are clearly labeled rather than estimated
- source failures appear in the source-health report
- the skill can run the workflow with `/job-market-monitor daily`
- the local dashboard displays all three selectable tables and opens job details
- an explicit click generates a tailored `.txt` draft in the correct track folder without sending it
- the daily dashboard filename contains the three table counts and date
- filename collisions preserve earlier drafts
- the README contains exact scheduling instructions

At the end, show me the files created, tests run, the first-run coverage limitations, and the exact command/prompt I should use to schedule it daily. Do not claim that a blocked source was searched successfully.
```

## 3. Run it manually after Claude finishes building

Inside Claude Code:

```text
/job-market-monitor full-refresh
```

For later daily checks:

```text
/job-market-monitor daily
```

From Terminal, a non-interactive run can use:

```bash
cd ~/job-market-monitor
claude -p "/job-market-monitor daily"
```

Do not add `--bare`, because bare mode skips project skills and configuration.

## 4. Create the daily reminder

### Claude Code Desktop scheduled task (recommended)

Open the project in Claude Code Desktop and send:

```text
Create a local scheduled task named "Judy Job Market Monitor." Run it daily at 8:00 AM America/Los_Angeles. Invoke /job-market-monitor daily; save HTML, Markdown, and CSV summaries in /Users/judyzhang/Desktop/Job/Summary_everyday with the three table counts and date in each filename. Notify me of new strong/possible matches, deadlines within 14 days, and failed sources. Never generate email drafts automatically; create one only after I select a job and click Generate email draft. Run once now so I can approve the required permissions.
```

The Mac must be on and awake at run time.

### Alternative: Claude Code cloud Routine

Use this only if the monitor must run while the Mac is off. It cannot write to `/Users/judyzhang/Desktop`; put the project in a private repository first and exclude secrets/private notes. Then enter:

```text
/schedule daily at 8:00 AM America/Los_Angeles: clone the private job-market-monitor repository, run /job-market-monitor daily, preserve its durable job state, and return new matches, approaching deadlines, and source failures
```

Configure allowed career domains and persistent SQLite/output storage for cloud runs.
