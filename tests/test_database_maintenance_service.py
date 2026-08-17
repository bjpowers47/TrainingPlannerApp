import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from app.services.database_maintenance_service import DatabaseMaintenanceService


class DatabaseMaintenanceServiceTests(unittest.TestCase):
    def test_health_backup_and_optimize(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            database_path = root / "test.db"
            with closing(sqlite3.connect(database_path)) as connection:
                connection.execute(
                    "CREATE TABLE drills (id INTEGER PRIMARY KEY, name TEXT)"
                )
                connection.execute("INSERT INTO drills (name) VALUES ('Passing')")
                connection.commit()

            service = DatabaseMaintenanceService(database_path, root / "backups")
            status = service.check_health()
            self.assertTrue(status.is_healthy)
            self.assertEqual(status.table_count, 1)

            backup_path = service.create_backup()
            self.assertTrue(backup_path.is_file())
            with closing(sqlite3.connect(backup_path)) as connection:
                name = connection.execute("SELECT name FROM drills").fetchone()[0]
            self.assertEqual(name, "Passing")

            self.assertGreaterEqual(service.optimize(), 0)
            self.assertTrue(service.check_health().is_healthy)

    def test_missing_database_is_reported(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            service = DatabaseMaintenanceService(
                root / "missing.db", root / "backups"
            )
            with self.assertRaisesRegex(FileNotFoundError, "Database not found"):
                service.check_health()

    def test_restore_validates_and_preserves_current_database(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            database_path = root / "current.db"
            backup_path = root / "selected.db"

            for path, drill_name in (
                (database_path, "Current Drill"),
                (backup_path, "Restored Drill"),
            ):
                with closing(sqlite3.connect(path)) as connection:
                    connection.execute("CREATE TABLE development_blocks (id INTEGER)")
                    connection.execute("CREATE TABLE drills (name TEXT)")
                    connection.execute("INSERT INTO drills VALUES (?)", (drill_name,))
                    connection.commit()

            service = DatabaseMaintenanceService(database_path, root / "backups")
            safety_backup = service.restore_backup(backup_path)

            with closing(sqlite3.connect(database_path)) as connection:
                restored = connection.execute("SELECT name FROM drills").fetchone()[0]
            with closing(sqlite3.connect(safety_backup)) as connection:
                preserved = connection.execute("SELECT name FROM drills").fetchone()[0]
            self.assertEqual(restored, "Restored Drill")
            self.assertEqual(preserved, "Current Drill")

    def test_restore_removes_records_not_present_in_backup(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            current = root / "current.db"
            backup = root / "selected.db"
            for path in (current, backup):
                with closing(sqlite3.connect(path)) as connection:
                    connection.execute("CREATE TABLE development_blocks (id INTEGER, name TEXT)")
                    connection.execute("CREATE TABLE drills (id INTEGER, name TEXT)")
                    connection.execute("INSERT INTO development_blocks VALUES (1, 'Restored Block')")
                    connection.execute("INSERT INTO drills VALUES (1, 'Restored Drill')")
                    connection.commit()
            with closing(sqlite3.connect(current)) as connection:
                connection.execute("INSERT INTO development_blocks VALUES (2, 'Current Extra Block')")
                connection.execute("INSERT INTO drills VALUES (2, 'Current Extra Drill')")
                connection.commit()

            DatabaseMaintenanceService(current, root / "backups").restore_backup(backup)

            with closing(sqlite3.connect(current)) as connection:
                blocks = connection.execute("SELECT name FROM development_blocks").fetchall()
                drills = connection.execute("SELECT name FROM drills").fetchall()
            self.assertEqual(blocks, [("Restored Block",)])
            self.assertEqual(drills, [("Restored Drill",)])

    def test_restore_rejects_unrelated_database(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            database_path = root / "current.db"
            invalid_path = root / "invalid.db"
            for path in (database_path, invalid_path):
                with closing(sqlite3.connect(path)) as connection:
                    connection.execute("CREATE TABLE unrelated (id INTEGER)")
                    connection.commit()

            service = DatabaseMaintenanceService(database_path, root / "backups")
            with self.assertRaisesRegex(sqlite3.DatabaseError, "not a Training Manager"):
                service.restore_backup(invalid_path)


if __name__ == "__main__":
    unittest.main()
