import json
import tempfile
import unittest
from pathlib import Path

from app.models.practice import Practice


class PracticeTargetDurationTests(unittest.TestCase):
    def test_target_duration_survives_json_round_trip(self):
        with tempfile.TemporaryDirectory() as folder:
            filename = Path(folder) / "practice.json"
            Practice(name="Tuesday", target_minutes=75).save_to_json(filename)
            loaded = Practice.load_from_json(filename)
            self.assertEqual(loaded.target_minutes, 75)

    def test_older_file_defaults_to_ninety_minutes(self):
        with tempfile.TemporaryDirectory() as folder:
            filename = Path(folder) / "legacy.json"
            filename.write_text(json.dumps({"name": "Legacy", "activities": {}}), encoding="utf-8")
            loaded = Practice.load_from_json(filename)
            self.assertEqual(loaded.target_minutes, 90)


if __name__ == "__main__":
    unittest.main()
