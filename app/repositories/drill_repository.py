"""SQLite-backed storage and retrieval for Development Library drills."""

from __future__ import annotations

import json

from app.database import Database
from app.models.drill import Drill


class DrillRepository:
    """Persist drills locally and open the database only when it is needed."""

    def __init__(self, database: Database | None = None):
        self._database = database or Database()
        self._initialized = False

    def _ensure_initialized(self) -> None:
        if self._initialized:
            return
        self._database.initialize()
        self._initialized = True

    @staticmethod
    def _encode(values: list[str]) -> str:
        return json.dumps(values)

    @staticmethod
    def _decode(value: str | None) -> list[str]:
        return json.loads(value) if value else []

    @classmethod
    def _to_drill(cls, row) -> Drill:
        return Drill(
            id=row["id"],
            name=row["name"],
            development_block_id=row["development_block_id"],
            technical_focus_id=row["technical_focus_id"],
            purpose=row["purpose"],
            duration_minutes=row["duration_minutes"],
            recommended_players=row["recommended_players"],
            use_execution_details=bool(row["use_execution_details"]),
            sets=row["sets"],
            reps=row["reps"],
            work_seconds=row["work_seconds"],
            rest_seconds=row["rest_seconds"],
            equipment=cls._decode(row["equipment"]),
            coaching_points=cls._decode(row["coaching_points"]),
            progressions=cls._decode(row["progressions"]),
            variations=cls._decode(row["variations"]),
            notes=row["notes"],
            active=bool(row["is_active"]),
        )

    def save(self, drill: Drill) -> None:
        self._ensure_initialized()
        values = (
            drill.development_block_id, drill.technical_focus_id, drill.name,
            drill.purpose, drill.duration_minutes, drill.recommended_players,
            int(drill.use_execution_details), drill.sets, drill.reps,
            drill.work_seconds, drill.rest_seconds, self._encode(drill.equipment),
            self._encode(drill.coaching_points), self._encode(drill.progressions),
            self._encode(drill.variations), drill.notes, int(drill.active), drill.id,
        )
        with self._database.connect() as connection:
            exists = connection.execute(
                "SELECT 1 FROM drills WHERE id = ?", (drill.id,)
            ).fetchone()
            if exists:
                connection.execute(
                    """UPDATE drills SET development_block_id=?, technical_focus_id=?,
                    name=?, purpose=?, duration_minutes=?, recommended_players=?,
                    use_execution_details=?, sets=?, reps=?, work_seconds=?, rest_seconds=?,
                    equipment=?, coaching_points=?, progressions=?, variations=?, notes=?,
                    is_active=? WHERE id=?""",
                    values,
                )
            else:
                connection.execute(
                    """INSERT INTO drills (id, development_block_id, technical_focus_id,
                    name, purpose, duration_minutes, recommended_players,
                    use_execution_details, sets, reps, work_seconds, rest_seconds,
                    equipment, coaching_points, progressions, variations, notes, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (drill.id,) + values[:-1],
                )

    def get_all(self) -> list[Drill]:
        self._ensure_initialized()
        with self._database.connect() as connection:
            rows = connection.execute(
                "SELECT * FROM drills WHERE is_active = 1 ORDER BY development_block_id, name"
            ).fetchall()
        return [self._to_drill(row) for row in rows]

    def get_by_id(self, drill_id: int) -> Drill | None:
        self._ensure_initialized()
        with self._database.connect() as connection:
            row = connection.execute("SELECT * FROM drills WHERE id = ?", (drill_id,)).fetchone()
        return self._to_drill(row) if row else None

    def get_by_development_block(self, development_block_id: int) -> list[Drill]:
        return [drill for drill in self.get_all() if drill.development_block_id == development_block_id]

    def get_by_technical_focus(self, technical_focus_id: int) -> list[Drill]:
        return [drill for drill in self.get_all() if drill.technical_focus_id == technical_focus_id]

    def archive(self, drill_id: int) -> bool:
        drill = self.get_by_id(drill_id)
        if drill is None:
            return False
        drill.archive()
        self.save(drill)
        return True
