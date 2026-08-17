import tempfile
import unittest
from pathlib import Path

from app.database import Database
from app.models.drill import Drill
from app.models.practice import Practice
from app.repositories.drill_repository import DrillRepository
from app.services.practice_output_controller import PracticeOutputController
from app.services.practice_pdf_service import export_practice_pdf


class EfficiencyRegressionTests(unittest.TestCase):
    def test_repository_filters_drills_in_sql(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = DrillRepository(Database(Path(folder) / "planner.db"))
            repository.save(Drill(id=1, name="One", development_block_id=1))
            repository.save(Drill(id=2, name="Two", development_block_id=2))
            repository.save(
                Drill(id=3, name="Archived", development_block_id=1, active=False)
            )

            block_drills = repository.get_by_development_block(1)

        self.assertEqual([drill.name for drill in block_drills], ["One"])

    def test_large_practice_export_remains_complete(self):
        practice = Practice(name="Scale Check")
        for number in range(50):
            practice.add_activity(
                "Ball Mastery",
                Drill(
                    id=number + 1,
                    name=f"Activity {number + 1}",
                    development_block_id=1,
                    purpose="First direction\nSecond direction",
                ),
            )
            practice.get_activities("Ball Mastery")[-1].print_details = True

        with tempfile.TemporaryDirectory() as folder:
            filename = Path(folder) / "large.pdf"
            export_practice_pdf(filename, practice)
            content = filename.read_bytes()

        self.assertIn(b"Activity 1", content)
        self.assertIn(b"Activity 50", content)
        self.assertGreater(content.count(b"/Type /Page"), 1)

    def test_output_filename_is_safe_and_readable(self):
        self.assertEqual(
            PracticeOutputController.safe_filename('Tuesday: U12 / "A"'),
            "Tuesday_ U12 _ _A_",
        )


if __name__ == "__main__":
    unittest.main()
