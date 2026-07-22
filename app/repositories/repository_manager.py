"""
Coach's Training Manager
------------------------

Module:
    repository_manager.py

Purpose:
    Provides one place to access application repositories.
"""

from app.repositories.drill_repository import DrillRepository
from app.repositories.technical_focus_repository import (
    TechnicalFocusRepository,
)


class RepositoryManager:
    """Container for application repositories."""

    def __init__(self):
        self.drills = DrillRepository()
        self.technical_focuses = TechnicalFocusRepository()