"""
SQLite database initialization for Training Planner Ap.

This module owns the physical database connection and schema creation.
Other parts of the application should access data through repositories.
"""

from __future__ import annotations

import sqlite3
from contextlib import closing
from pathlib import Path


DEFAULT_DATABASE_PATH = Path("data") / "coach_training.db"


class Database:
    """Manages the SQLite database connection and schema."""

    def __init__(self, database_path: Path | str = DEFAULT_DATABASE_PATH):
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)

    def connect(self) -> sqlite3.Connection:
        """Create a database connection with useful defaults."""
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON;")
        return connection

    def initialize(self) -> None:
        """Create all required database tables and seed base data."""
        with closing(self.connect()) as connection, connection:
            self._create_tables(connection)
            self._seed_development_blocks(connection)

    def _create_tables(self, connection: sqlite3.Connection) -> None:
        """Create database tables if they do not already exist."""
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS development_blocks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT NOT NULL DEFAULT '',
                display_order INTEGER NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS technical_focuses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                development_block_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                display_order INTEGER NOT NULL DEFAULT 0,
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (development_block_id)
                    REFERENCES development_blocks (id)
                    ON DELETE RESTRICT
            );

            CREATE TABLE IF NOT EXISTS drills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                development_block_id INTEGER NOT NULL,
                technical_focus_id INTEGER,
                coaching_focus TEXT NOT NULL DEFAULT '',
                name TEXT NOT NULL,
                purpose TEXT NOT NULL DEFAULT '',
                duration_minutes INTEGER NOT NULL DEFAULT 0,
                recommended_players TEXT NOT NULL DEFAULT '',
                use_execution_details INTEGER NOT NULL DEFAULT 0,
                sets INTEGER,
                reps INTEGER,
                work_seconds INTEGER,
                rest_seconds INTEGER,
                equipment TEXT NOT NULL DEFAULT '[]',
                coaching_points TEXT NOT NULL DEFAULT '',
                progressions TEXT NOT NULL DEFAULT '',
                variations TEXT NOT NULL DEFAULT '',
                notes TEXT NOT NULL DEFAULT '',
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (development_block_id)
                    REFERENCES development_blocks (id)
                    ON DELETE RESTRICT,
                FOREIGN KEY (technical_focus_id)
                    REFERENCES technical_focuses (id)
                    ON DELETE SET NULL
            );

            CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                season_name TEXT NOT NULL DEFAULT '',
                notes TEXT NOT NULL DEFAULT '',
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id INTEGER,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL DEFAULT '',
                birth_year INTEGER,
                jersey_number TEXT NOT NULL DEFAULT '',
                primary_position TEXT NOT NULL DEFAULT '',
                notes TEXT NOT NULL DEFAULT '',
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (team_id)
                    REFERENCES teams (id)
                    ON DELETE SET NULL
            );

            CREATE TABLE IF NOT EXISTS development_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_type TEXT NOT NULL,
                subject_id INTEGER NOT NULL,
                development_block_id INTEGER NOT NULL,
                rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
                snapshot_date TEXT NOT NULL,
                notes TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (development_block_id)
                    REFERENCES development_blocks (id)
                    ON DELETE RESTRICT
            );

            CREATE TABLE IF NOT EXISTS observations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_type TEXT NOT NULL,
                subject_id INTEGER NOT NULL,
                development_block_id INTEGER,
                observation_date TEXT NOT NULL,
                note TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (development_block_id)
                    REFERENCES development_blocks (id)
                    ON DELETE SET NULL
            );

            CREATE TABLE IF NOT EXISTS practice_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id INTEGER,
                practice_date TEXT NOT NULL,
                title TEXT NOT NULL,
                objective TEXT NOT NULL DEFAULT '',
                location TEXT NOT NULL DEFAULT '',
                duration_minutes INTEGER,
                reflection TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (team_id)
                    REFERENCES teams (id)
                    ON DELETE SET NULL
            );

            CREATE TABLE IF NOT EXISTS practice_blocks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                practice_session_id INTEGER NOT NULL,
                development_block_id INTEGER NOT NULL,
                drill_id INTEGER,
                display_order INTEGER NOT NULL DEFAULT 0,
                duration_minutes INTEGER,
                notes TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (practice_session_id)
                    REFERENCES practice_sessions (id)
                    ON DELETE CASCADE,
                FOREIGN KEY (development_block_id)
                    REFERENCES development_blocks (id)
                    ON DELETE RESTRICT,
                FOREIGN KEY (drill_id)
                    REFERENCES drills (id)
                    ON DELETE SET NULL
            );
            """
        )
        columns = {row[1] for row in connection.execute("PRAGMA table_info(drills)")}
        if "coaching_focus" not in columns:
            connection.execute("ALTER TABLE drills ADD COLUMN coaching_focus TEXT NOT NULL DEFAULT ''")

    def _seed_development_blocks(self, connection: sqlite3.Connection) -> None:
        """Seed the initial Development Blocks for a new database."""
        existing_count = connection.execute(
            "SELECT COUNT(*) FROM development_blocks"
        ).fetchone()[0]
        development_blocks = [
            ("Ball Mastery", "Confidence, creativity, and comfort with the ball.", 1),
            ("Receiving & Passing", "First touch, passing quality, and support play.", 2),
            ("1v1 Moves", "Confidence and skill to beat defenders.", 3),
            ("Speed & Agility", "Movement, coordination, acceleration, and agility.", 4),
            ("Finishing", "Composure and technique in front of goal.", 5),
            ("Group Play", "Decision-making, possession, transition, and teamwork.", 6),
        ]

        if existing_count:
            # Older releases re-seeded a default row after that block was
            # renamed. Remove only the resulting unreferenced duplicate that
            # shares the renamed block's original display position.
            for name, _description, display_order in development_blocks:
                connection.execute(
                    """
                    DELETE FROM development_blocks
                    WHERE name = ?
                      AND display_order = ?
                      AND EXISTS (
                          SELECT 1 FROM development_blocks replacement
                          WHERE replacement.display_order = ?
                            AND replacement.id != development_blocks.id
                      )
                      AND NOT EXISTS (
                          SELECT 1 FROM drills
                          WHERE development_block_id = development_blocks.id
                      )
                      AND NOT EXISTS (
                          SELECT 1 FROM technical_focuses
                          WHERE development_block_id = development_blocks.id
                      )
                      AND NOT EXISTS (
                          SELECT 1 FROM development_snapshots
                          WHERE development_block_id = development_blocks.id
                      )
                      AND NOT EXISTS (
                          SELECT 1 FROM observations
                          WHERE development_block_id = development_blocks.id
                      )
                      AND NOT EXISTS (
                          SELECT 1 FROM practice_blocks
                          WHERE development_block_id = development_blocks.id
                      )
                    """,
                    (name, display_order, display_order),
                )
            return

        for name, description, display_order in development_blocks:
            connection.execute(
                """
                INSERT OR IGNORE INTO development_blocks
                    (name, description, display_order)
                VALUES
                    (?, ?, ?);
                """,
                (name, description, display_order),
            )
