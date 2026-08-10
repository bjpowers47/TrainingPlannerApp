"""
Training Planner Ap
------------------------

Module:
    observation.py

Purpose:
    Represents a coach's note about a player, practice, drill, or team.
"""

from dataclasses import dataclass
from datetime import date


@dataclass
class Observation:
    """A coaching observation recorded over time."""

    id: int
    note_date: date
    note: str
    player_id: int | None = None
    team_id: int | None = None
    practice_id: int | None = None
    development_block_id: int | None = None

    def has_context(self) -> bool:
        """Return True when the note is linked to at least one coaching object."""
        return any([
            self.player_id,
            self.team_id,
            self.practice_id,
            self.development_block_id,
        ])
