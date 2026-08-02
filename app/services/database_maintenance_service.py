"""Safe maintenance operations for the application's SQLite database."""

from __future__ import annotations

import sqlite3
import os
from contextlib import closing
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class DatabaseStatus:
    integrity: str
    size_bytes: int
    table_count: int

    @property
    def is_healthy(self) -> bool:
        return self.integrity.lower() == "ok"


class DatabaseMaintenanceService:
    """Check, back up, and optimize a SQLite database."""

    def __init__(self, database_path: Path | str, backup_dir: Path | str):
        self.database_path = Path(database_path)
        self.backup_dir = Path(backup_dir)

    def check_health(self) -> DatabaseStatus:
        self._require_database()
        with closing(sqlite3.connect(self.database_path)) as connection:
            row = connection.execute("PRAGMA integrity_check;").fetchone()
            table_count = connection.execute(
                "SELECT COUNT(*) FROM sqlite_master "
                "WHERE type = 'table' AND name NOT LIKE 'sqlite_%';"
            ).fetchone()[0]
        return DatabaseStatus(str(row[0]), self.database_path.stat().st_size, int(table_count))

    def create_backup(self) -> Path:
        """Create a consistent backup using SQLite's online backup API."""
        self._require_database()
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        destination = self.backup_dir / f"coach_training_{timestamp}.db"
        with closing(sqlite3.connect(self.database_path)) as source:
            with closing(sqlite3.connect(destination)) as target:
                source.backup(target)
        return destination

    def optimize(self) -> int:
        """Compact the database and refresh query-planning data."""
        self._require_database()
        before = self.database_path.stat().st_size
        with closing(sqlite3.connect(self.database_path)) as connection:
            connection.execute("PRAGMA optimize;")
            connection.execute("VACUUM;")
        return max(0, before - self.database_path.stat().st_size)

    def validate_backup(self, backup_path: Path | str) -> DatabaseStatus:
        """Verify that a file is a healthy application database backup."""
        path = Path(backup_path)
        if not path.is_file():
            raise FileNotFoundError(f"Backup not found: {path}")

        uri = f"{path.resolve().as_uri()}?mode=ro"
        with closing(sqlite3.connect(uri, uri=True)) as connection:
            integrity = str(connection.execute("PRAGMA integrity_check;").fetchone()[0])
            tables = {
                row[0]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table';"
                )
            }
        required_tables = {"development_blocks", "drills"}
        missing = required_tables - tables
        if integrity.lower() != "ok":
            raise sqlite3.DatabaseError(f"Backup integrity check reported: {integrity}")
        if missing:
            raise sqlite3.DatabaseError(
                "The selected file is not a Training Manager backup."
            )
        return DatabaseStatus(integrity, path.stat().st_size, len(tables))

    def restore_backup(self, backup_path: Path | str) -> Path:
        """Preserve the current database and atomically restore a valid backup."""
        source_path = Path(backup_path)
        self.validate_backup(source_path)
        safety_backup = self.create_backup()
        temporary_path = self.database_path.with_suffix(".restore.tmp")

        try:
            if temporary_path.exists():
                temporary_path.unlink()
            with closing(sqlite3.connect(source_path)) as source:
                with closing(sqlite3.connect(temporary_path)) as target:
                    source.backup(target)
            os.replace(temporary_path, self.database_path)
        except Exception:
            if temporary_path.exists():
                temporary_path.unlink()
            raise
        return safety_backup

    def _require_database(self) -> None:
        if not self.database_path.is_file():
            raise FileNotFoundError(f"Database not found: {self.database_path}")
