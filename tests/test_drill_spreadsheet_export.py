import tempfile
import unittest
from pathlib import Path

from openpyxl import load_workbook

from app.models.drill import Drill
from app.services.drill_spreadsheet_service import EXPORT_HEADERS, export_spreadsheet


class _Repository:
    def get_all(self):
        return [
            Drill(
                id=7,
                name="Passing Pattern",
                development_block_id=2,
                technical_focus_id=11,
                purpose="=unsafe formula text",
                duration_minutes=15,
                recommended_players="8–12",
                use_execution_details=True,
                sets=3,
                reps=4,
                work_seconds=45,
                rest_seconds=20,
                equipment=["Balls", "Cones"],
                coaching_points=["Scan", "Open body"],
                progressions=["One touch"],
                variations=["Add defender"],
                notes="Coach notes",
            ),
            Drill(id=8, name="Archived", development_block_id=1, active=False),
        ]


class DrillSpreadsheetExportTests(unittest.TestCase):
    def test_exports_active_drills_with_labels_formatting_and_safe_text(self):
        with tempfile.TemporaryDirectory() as folder:
            filename = Path(folder) / "export.xlsx"
            exported = export_spreadsheet(filename, _Repository())

            self.assertEqual(exported, 1)
            workbook = load_workbook(filename, data_only=False)
            worksheet = workbook["Active Drills"]
            self.assertEqual(
                tuple(cell.value for cell in worksheet[1]), EXPORT_HEADERS
            )
            self.assertEqual(worksheet.max_row, 2)
            self.assertEqual(worksheet["B2"].value, "Receiving & Passing")
            self.assertEqual(worksheet["C2"].value, "First Touch")
            self.assertEqual(worksheet["E2"].value, "'=unsafe formula text")
            self.assertEqual(worksheet["M2"].value, "Balls | Cones")
            self.assertEqual(worksheet.freeze_panes, "A2")
            self.assertEqual(worksheet.auto_filter.ref, "A1:Q2")


if __name__ == "__main__":
    unittest.main()
