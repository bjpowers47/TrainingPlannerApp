import tempfile
import unittest
from pathlib import Path

from app.models.drill import Drill
from app.models.practice import Practice


class RemovedWarmUpTests(unittest.TestCase):
    def test_total_is_calculated_only_from_activities(self):
        practice = Practice()
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

        self.assertEqual(practice.total_duration(), 8)
        self.assertEqual(practice.activity_count(), 1)
        self.assertEqual(practice.get_block_names()[0], "Ball Mastery")

    def test_legacy_warm_up_value_is_ignored_when_loading(self):
        with tempfile.TemporaryDirectory() as folder:
            filename = Path(folder) / "practice.json"
            filename.write_text(
                '{"name": "Old Practice", "warm_up_minutes": 10, "activities": {}}',
                encoding="utf-8",
            )
            restored = Practice.load_from_json(str(filename))

        self.assertFalse(hasattr(restored, "warm_up_minutes"))
        self.assertEqual(restored.total_duration(), 0)

    def test_new_practice_files_do_not_save_a_warm_up_field(self):
        practice = Practice(name="Tuesday")
        with tempfile.TemporaryDirectory() as folder:
            filename = Path(folder) / "practice.json"
            practice.save_to_json(str(filename))
            content = filename.read_text(encoding="utf-8")

        self.assertNotIn("warm_up_minutes", content)


if __name__ == "__main__":
    unittest.main()
