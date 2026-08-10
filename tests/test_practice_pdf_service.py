import tempfile
import unittest
from pathlib import Path

from app.models.drill import Drill
from app.models.practice import Practice
from app.services.practice_pdf_service import build_practice_pdf_lines, export_practice_pdf


class PracticePdfServiceTests(unittest.TestCase):
    def test_pdf_contains_warm_up_blocks_drill_details_and_total(self):
        practice = Practice(
            name="Tuesday Training",
            practice_date="2026-08-01",
            warm_up_minutes=10,
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
        self.assertIn("Warm Up", text)
        self.assertIn("Ball Mastery", text)
        self.assertIn("Toe Taps", text)
        self.assertIn("Equipment: Ball, Cones", text)
        self.assertIn("Total Planned Time: 15 min", text)

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

    def test_assigned_coaches_print_beside_the_block(self):
        practice = Practice(block_coaches={"Ball Mastery": ["Alex", "Sam"]})
        text = "\n".join(value for _style, value in build_practice_pdf_lines(practice))
        self.assertIn("Ball Mastery — Coaches: Alex, Sam", text)

    def test_empty_practice_still_generates_a_complete_pdf(self):
        practice = Practice()
        with tempfile.TemporaryDirectory() as folder:
            filename = Path(folder) / "empty.pdf"
            export_practice_pdf(filename, practice)
            content = filename.read_bytes()
        self.assertIn(b"Training Manager Practice Plan", content)
        self.assertIn(b"No activities planned.", content)
        self.assertIn(b"Total Planned Time: 0 min", content)

    def test_configured_sport_prefixes_training_manager_title(self):
        practice = Practice(sport="Basketball")
        lines = build_practice_pdf_lines(practice)
        self.assertEqual(lines[0], ("title", "Basketball Training Manager Practice Plan"))


if __name__ == "__main__":
    unittest.main()
