"""
Coach's Training Manager
------------------------

Module:
    drill_repository.py

Purpose:
    Provides storage and retrieval operations for Drill objects.

Responsibilities:
    - Store Drill objects in memory for now.
    - Retrieve drills by ID.
    - Retrieve drills by Development Block.
    - Retrieve drills by Technical Focus.
    - Archive drills without deleting history.

Notes:
    This is an in-memory repository for Sprint Alpha.
    Later, this same interface will be backed by SQLite.
"""

from app.models.drill import Drill


class DrillRepository:
    """Repository for working with Drill objects."""

    def __init__(self):
        self._drills = {}

    def save(self, drill: Drill) -> None:
        """Save or update a drill."""
        self._drills[drill.id] = drill

    def get_all(self) -> list[Drill]:
        """Return all active drills."""
        drills = []

        for drill in self._drills.values():
            if drill.active:
                drills.append(drill)

        return drills

    def get_by_id(self, drill_id: int) -> Drill | None:
        """Return a drill by ID."""
        return self._drills.get(drill_id)

    def get_by_development_block(self, development_block_id: int) -> list[Drill]:
        """Return active drills for a Development Block."""
        drills = []

        for drill in self._drills.values():
            if drill.active and drill.development_block_id == development_block_id:
                drills.append(drill)

        return drills

    def get_by_technical_focus(self, technical_focus_id: int) -> list[Drill]:
        """Return active drills for a Technical Focus."""
        drills = []

        for drill in self._drills.values():
            if drill.active and drill.technical_focus_id == technical_focus_id:
                drills.append(drill)

        return drills

    def archive(self, drill_id: int) -> bool:
        """Archive a drill by ID."""
        drill = self.get_by_id(drill_id)

        if drill is None:
            return False

        drill.archive()
        return True