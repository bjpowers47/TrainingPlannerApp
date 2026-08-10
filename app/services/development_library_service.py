"""
Coach's Training Manager
------------------------

Module:
    development_library_service.py

Purpose:
    Coordinates access to the Development Library.

Responsibilities:
    - Provide drill information to the UI.
    - Hide repository details from the UI.
"""

from app.repositories.drill_repository import DrillRepository
from collections import defaultdict


class DevelopmentLibraryService:
    """Service layer for the Development Library."""
    
    def get_drills_by_block(self):
        """Return active drills grouped by development block ID."""

        grouped = defaultdict(list)

        drills = self.get_all_drills()

        for drill in drills:
            grouped[drill.development_block_id].append(drill)

        return grouped

    def __init__(self, drill_repository: DrillRepository):
        self._drill_repository = drill_repository

    def get_all_drills(self):
        """Return all active drills."""
        return self._drill_repository.get_all()

    def get_drill(self, drill_id: int):
        """Return one drill."""
        return self._drill_repository.get_by_id(drill_id)

    def get_drills_for_block(self, block_id: int):
        """Return drills for a Development Block."""
        return self._drill_repository.get_by_development_block(block_id)

    def get_drills_for_focus(self, focus_id: int):
        """Return drills for a Technical Focus."""
        return self._drill_repository.get_by_technical_focus(focus_id)

    def delete_drill(self, drill_id: int) -> bool:
        """Permanently remove a drill from the Development Library."""
        return self._drill_repository.delete(drill_id)
