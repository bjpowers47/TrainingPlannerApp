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
from app.config import ROOT
from app.database import Database
from app.repositories.development_block_repository import DevelopmentBlockRepository


class RepositoryManager:
    """Container for application repositories."""

    def __init__(self):
        database = Database(ROOT / "data" / "coach_training.db")
        self.drills = DrillRepository(database)
        self.technical_focuses = TechnicalFocusRepository()
        self.development_blocks = DevelopmentBlockRepository(database)
