"""
Coach's Training Manager
------------------------

Module:
    drill.py

Purpose:
    Represents a reusable coaching activity in the Development Library.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Drill:
    """A reusable training activity."""

    id: int
    name: str
    development_block_id: int
    technical_focus_id: int | None = None
    purpose: str = ""
    duration_minutes: int = 0
    recommended_players: str = ""
    equipment: List[str] = field(default_factory=list)
    coaching_points: List[str] = field(default_factory=list)
    progressions: List[str] = field(default_factory=list)
    variations: List[str] = field(default_factory=list)
    notes: str = ""
    active: bool = True

    def add_coaching_point(self, point: str) -> None:
        """Add a coaching point if it is not blank."""
        clean_point = point.strip()

        if clean_point:
            self.coaching_points.append(clean_point)

    def add_progression(self, progression: str) -> None:
        """Add a progression if it is not blank."""
        clean_progression = progression.strip()

        if clean_progression:
            self.progressions.append(clean_progression)

    def add_variation(self, variation: str) -> None:
        """Add a variation if it is not blank."""
        clean_variation = variation.strip()

        if clean_variation:
            self.variations.append(clean_variation)

    def archive(self) -> None:
        """Archive the drill without deleting history."""
        self.active = False
