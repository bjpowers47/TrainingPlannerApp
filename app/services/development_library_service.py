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


class DevelopmentLibraryService:
    """Service layer for the Development Library."""

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