from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from job_market_monitor.drafts import folder_for_track, sanitize_filename, write_draft_atomic
from job_market_monitor.filters import is_excluded, normalize_salary
from job_market_monitor.models import Job, TRACK_CN_ACADEMIA, TRACK_INDUSTRY, TRACK_US_ACADEMIA
from job_market_monitor.reports import write_dashboard_html


class MonitorTests(unittest.TestCase):
    def test_china_postdoc_excluded(self):
        job = Job(
            track=TRACK_CN_ACADEMIA,
            title="博士后",
            organization="A",
            department="",
            city="",
            state_province="",
            country="",
            work_mode="",
            official_url="http://example.com",
            discovery_url="",
            source_name="",
            date_posted="",
            application_deadline="",
            status="active",
            appointment_type="",
            employment_type="",
            term_length="",
            salary_raw="",
            salary_min="",
            salary_max="",
            currency="",
            pay_period="",
            china_base_salary="",
            china_annual_package="",
            china_housing_allowance="",
            china_startup_funds="",
            china_other_benefits="",
            required_degree="",
            preferred_degree="",
            required_methods="",
            preferred_methods="",
            required_years="",
            visa_language="",
            visa_sponsorship="possible_or_unknown",
            description="",
            summary="",
            hard_barriers="",
            matched_experience="",
            gaps="",
            recommended_action="",
            confidence="",
            discipline_judgment_cn="",
        )
        self.assertTrue(is_excluded(job))

    def test_salary_normalization(self):
        self.assertEqual(normalize_salary(""), "Not disclosed / 未披露")

    def test_track_folder_routing(self):
        base = Path("/tmp")
        self.assertTrue(str(folder_for_track(TRACK_INDUSTRY, base / "i", base / "u", base / "c")).endswith("i"))
        self.assertTrue(str(folder_for_track(TRACK_US_ACADEMIA, base / "i", base / "u", base / "c")).endswith("u"))
        self.assertTrue(str(folder_for_track(TRACK_CN_ACADEMIA, base / "i", base / "u", base / "c")).endswith("c"))

    def test_draft_collision_suffix(self):
        with tempfile.TemporaryDirectory() as td:
            p1 = write_draft_atomic(Path(td), "RAND_2026-08-10", "a")
            p2 = write_draft_atomic(Path(td), "RAND_2026-08-10", "b")
            self.assertNotEqual(p1.name, p2.name)
            self.assertTrue(p2.name.endswith("_2.txt"))

    def test_sanitize_filename(self):
        self.assertEqual(sanitize_filename("Stanford University"), "Stanford_University")
        self.assertEqual(sanitize_filename("A/B:C"), "A_B_C")

    def test_dashboard_click_preview_does_not_trigger_generation(self):
        with tempfile.TemporaryDirectory() as td:
            html_path = write_dashboard_html(
                Path(td),
                "Industry-1_USAcademia-0_CNAcademia-0_2026-08-10",
                "<table><tbody><tr data-job-id='job_x'></tr></tbody></table>",
            )
            content = html_path.read_text(encoding="utf-8")
            self.assertIn("fetch(`/api/job/${encodeURIComponent(selectedJobId)}`)", content)
            self.assertIn("fetch('/api/generate-draft'", content)


if __name__ == "__main__":
    unittest.main()
