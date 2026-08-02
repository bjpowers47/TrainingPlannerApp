import tempfile
import unittest
from pathlib import Path

from app.models.drill import Drill
from app.models.practice import Practice


class PracticeWarmUpTests(unittest.TestCase):
    def test_warm_up_is_included_in_total_without_becoming_an_activity(self):
        practice = Practice(warm_up_minutes=12)
        practice.add_activity(
            "Ball Mastery",
            Drill(
                id=1,
                name="Toe Taps",
                development_block_id=1,
                duration_minutes=8,
                sets=1,
                work_seconds=480,
                rest_seconds=0,
            ),
        )

        self.assertEqual(practice.total_duration(), 20)
        self.assertEqual(practice.activity_count(), 1)
        self.assertEqual(practice.get_block_names()[0], "Ball Mastery")

    def test_warm_up_survives_json_round_trip(self):
        practice = Practice(name="Tuesday", warm_up_minutes=10)
        with tempfile.TemporaryDirectory() as folder:
            filename = Path(folder) / "practice.json"
            practice.save_to_json(str(filename))
            restored = Practice.load_from_json(str(filename))

        self.assertEqual(restored.warm_up_minutes, 10)
        self.assertEqual(restored.total_duration(), 10)

    def test_older_practice_files_default_to_no_warm_up(self):
        with tempfile.TemporaryDirectory() as folder:
            filename = Path(folder) / "practice.json"
            filename.write_text(
                '{"name": "Old Practice", "activities": {}}', encoding="utf-8"
            )
            restored = Practice.load_from_json(str(filename))

        self.assertEqual(restored.warm_up_minutes, 0)


if __name__ == "__main__":
    unittest.main()
