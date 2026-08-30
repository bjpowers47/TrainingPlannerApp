import tempfile
import unittest
from pathlib import Path

from app.models.drill import Drill
from app.models.practice import Practice
from app.services.practice_pdf_service import (
    _contains_url,
    build_practice_pdf_lines,
    export_practice_pdf,
)


class PracticePdfServiceTests(unittest.TestCase):
    def test_url_detection_is_shared_by_print_and_pdf_renderers(self):
        self.assertTrue(_contains_url("Watch https://example.com/demo"))
        self.assertTrue(_contains_url("Review www.example.com/guide"))
        self.assertFalse(_contains_url("No web address here"))

    def test_pdf_contains_blocks_drill_details_and_total(self):
        practice = Practice(
            name="Tuesday Training",
            practice_date="2026-08-01",
        )
        practice.add_activity(
            "Ball Mastery",
            Drill(
                id=1,
                name="Toe Taps",
                development_block_id=1,
                purpose="Improve close control",
                sets=2,
                work_seconds=120,
                rest_seconds=30,
                equipment=["Ball", "Cones"],
                coaching_points=["Light touches"],
            ),
        )
        practice.get_activities("Ball Mastery")[0].print_details = True

        lines = build_practice_pdf_lines(practice)
        text = "\n".join(value for _style, value in lines)
        self.assertIn("Ball Mastery", text)
        self.assertIn("Toe Taps", text)
        self.assertIn("Equipment: Ball, Cones", text)
        self.assertIn("Total Planned Time: 5:00", text)

        with tempfile.TemporaryDirectory() as folder:
            filename = Path(folder) / "practice.pdf"
            export_practice_pdf(filename, practice)
            content = filename.read_bytes()
        self.assertTrue(content.startswith(b"%PDF-1.4"))
        self.assertTrue(content.endswith(b"%%EOF\n"))
        self.assertIn(b"Tuesday Training", content)

    def test_drill_details_are_omitted_until_selected(self):
        practice = Practice()
        practice.add_activity("Ball Mastery", Drill(id=1, name="Toe Taps", development_block_id=1, purpose="Improve control"))
        text = "\n".join(value for _style, value in build_practice_pdf_lines(practice))
        self.assertNotIn("Directions: Improve control", text)
        practice.get_activities("Ball Mastery")[0].print_details = True
        text = "\n".join(value for _style, value in build_practice_pdf_lines(practice))
        self.assertIn("Directions: Improve control", text)
        self.assertIn("Progressions: Not specified", text)
        self.assertIn("Practice Notes: Not specified", text)

    def test_practice_note_prints_beside_drill_name(self):
        practice = Practice()
        practice.add_activity(
            "Ball Mastery",
            Drill(id=1, name="Bell Taps (Sole Taps)", development_block_id=1),
        )
        practice.get_activities("Ball Mastery")[0].coach_notes = "Non-dominant Foot"

        lines = build_practice_pdf_lines(practice)

        self.assertIn(
            ("subheading", "Bell Taps (Sole Taps) — Non-dominant Foot"),
            lines,
        )

    def test_assigned_coaches_print_beside_the_block(self):
        practice = Practice(block_coaches={"Ball Mastery": ["Alex", "Sam"]})
        text = "\n".join(value for _style, value in build_practice_pdf_lines(practice))
        self.assertIn("Ball Mastery — Coaches: Alex, Sam", text)

    def test_unassigned_blocks_are_labeled_on_master_plan(self):
        practice = Practice()
        practice.add_activity(
            "Ball Mastery",
            Drill(id=1, name="Toe Taps", development_block_id=1),
        )
        text = "\n".join(value for _style, value in build_practice_pdf_lines(practice))
        self.assertIn("Ball Mastery — Coach: Unassigned", text)

    def test_empty_practice_still_generates_a_complete_pdf(self):
        practice = Practice()
        with tempfile.TemporaryDirectory() as folder:
            filename = Path(folder) / "empty.pdf"
            export_practice_pdf(filename, practice)
            content = filename.read_bytes()
        self.assertIn(b"Training Manager Practice Plan", content)
        self.assertIn(b"No activities planned.", content)
        self.assertIn(b"Total Planned Time: 0:00", content)

    def test_printed_times_include_exact_minutes_and_seconds(self):
        practice = Practice()
        practice.add_activity(
            "Ball Mastery",
            Drill(id=1, name="Toe Taps", development_block_id=1),
        )
        activity = practice.get_activities("Ball Mastery")[0]
        activity.sets = 1
        activity.work_seconds = 75
        activity.rest_seconds = 20

        text = "\n".join(
            value for _style, value in build_practice_pdf_lines(practice)
        )

        self.assertIn("Time: 1:35", text)
        self.assertIn("Work: 1:15", text)
        self.assertIn("Rest: 0:20", text)
        self.assertIn("Total Planned Time: 1:35", text)

    def test_export_preserves_user_entered_line_breaks(self):
        practice = Practice(name="Multiline Practice", objective="First goal\nSecond goal")
        practice.add_activity(
            "Ball Mastery",
            Drill(
                id=1,
                name="Toe Taps",
                development_block_id=1,
                purpose="First direction\nSecond direction",
                coaching_points=["First point", "Second point"],
                notes="First note\nSecond note",
            ),
        )
        practice.get_activities("Ball Mastery")[0].print_details = True

        lines = build_practice_pdf_lines(practice)
        self.assertIn(("normal", "Objective: First goal\nSecond goal"), lines)
        self.assertIn(("detail", "Directions: First direction\nSecond direction"), lines)
        self.assertIn(("detail", "Coaching Points: First point\nSecond point"), lines)

        with tempfile.TemporaryDirectory() as folder:
            filename = Path(folder) / "multiline.pdf"
            export_practice_pdf(filename, practice)
            content = filename.read_bytes()

        self.assertIn(b"(Objective: First goal) Tj", content)
        self.assertIn(b"(Second goal) Tj", content)
        self.assertIn(b"(Directions: First direction) Tj", content)
        self.assertIn(b"(Second direction) Tj", content)

    def test_export_highlights_lines_containing_urls(self):
        practice = Practice(name="Linked Practice")
        practice.add_activity(
            "Ball Mastery",
            Drill(
                id=1,
                name="Video Drill https://example.com/demo",
                development_block_id=1,
                purpose="Review www.example.com/guide before starting",
            ),
        )
        practice.get_activities("Ball Mastery")[0].print_details = True

        with tempfile.TemporaryDirectory() as folder:
            filename = Path(folder) / "linked.pdf"
            export_practice_pdf(filename, practice)
            content = filename.read_bytes()

        self.assertIn(b"% URL highlight", content)
        self.assertEqual(content.count(b"% URL highlight"), 2)
        self.assertIn(b"https://example.com/demo", content)
        self.assertIn(b"www.example.com/guide", content)

    def test_configured_sport_prefixes_training_manager_title(self):
        practice = Practice(sport="Basketball")
        lines = build_practice_pdf_lines(practice)
        self.assertEqual(lines[0], ("title", "Basketball Training Manager Practice Plan"))


if __name__ == "__main__":
    unittest.main()
