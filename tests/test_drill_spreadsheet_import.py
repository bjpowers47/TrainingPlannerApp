import tempfile
import unittest
from pathlib import Path

from openpyxl import Workbook

from app.database import Database
from app.repositories.drill_repository import DrillRepository
from app.services.drill_spreadsheet_service import (
    EXPORT_HEADERS,
    HEADERS,
    create_template,
    import_spreadsheet,
)


class DrillSpreadsheetImportTests(unittest.TestCase):
    def make_repository(self, folder):
        database = Database(Path(folder) / "test.db")
        database.initialize()
        with database.connect() as connection:
            connection.execute("PRAGMA foreign_keys = OFF")
            connection.execute("UPDATE development_blocks SET id = 103 WHERE name = '1v1 Moves'")
            connection.execute("UPDATE development_blocks SET id = 104 WHERE name = 'Speed & Agility'")
            connection.execute("PRAGMA foreign_keys = ON")
            connection.execute(
                "INSERT INTO technical_focuses "
                "(id, development_block_id, name, display_order) VALUES (221, 103, 'Scissors', 1)"
            )
        return DrillRepository(database)

    def save_workbook(self, filename, title, headers, row):
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = title
        sheet.append(headers)
        sheet.append(row)
        workbook.save(filename)

    def test_new_blank_complete_template_imports_without_errors(self):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as folder:
            repository = self.make_repository(folder)
            filename = Path(folder) / "template.xlsx"
            create_template(filename)

            report = import_spreadsheet(filename, repository)

            self.assertEqual(report.imported, 0)
            self.assertEqual(report.duplicates, [])
            self.assertEqual(report.errors, [])

    def test_imports_legacy_export_using_database_ids_and_aliases(self):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as folder:
            repository = self.make_repository(folder)
            filename = Path(folder) / "legacy.xlsx"
            self.save_workbook(filename, "Active Drills", EXPORT_HEADERS, (
                999, "1v1", "Scissors", "Escape Move", "Beat a defender", 12,
                "6", "Yes", 3, 5, 30, 15, "Balls | Cones",
                "Attack space | Accelerate", "Add defender", "Weak foot", "",
            ))

            report = import_spreadsheet(filename, repository)

            self.assertEqual(report.errors, [])
            self.assertEqual(report.imported, 1)
            drill = repository.get_all()[0]
            self.assertEqual(drill.development_block_id, 103)
            self.assertEqual(drill.technical_focus_id, 221)
            self.assertEqual(drill.equipment, ["Balls", "Cones"])
            self.assertEqual((drill.sets, drill.reps, drill.work_seconds, drill.rest_seconds),
                             (3, 5, 30, 15))

    def test_preserves_template_import_and_resolves_speed_alias(self):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as folder:
            repository = self.make_repository(folder)
            filename = Path(folder) / "template.xlsx"
            self.save_workbook(filename, "Drills", HEADERS, (
                "Speed", "Reaction Race", "React quickly", 8, "Any",
                "Cones; balls", "Stay balanced; react", "Add a ball", "Teams", "",
            ))

            report = import_spreadsheet(filename, repository)

            self.assertEqual(report.errors, [])
            self.assertEqual(report.imported, 1)
            drill = repository.get_all()[0]
            self.assertEqual(drill.development_block_id, 104)
            self.assertEqual(drill.equipment, ["Cones", "balls"])


if __name__ == "__main__":
    unittest.main()
