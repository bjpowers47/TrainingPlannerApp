"""
Wildcat Training Planner
------------------------

Module:
    development_snapshot.py

Purpose:
    Represents a periodic coaching assessment of a player's development.

Design Note:
    A snapshot is not a grade and not a target. It is a coach's view of where a
    player is at one moment in time. Snapshots are preserved so progress can be
    seen over time.
"""

from dataclasses import dataclass
from datetime import date


@dataclass
class DevelopmentSnapshot:
    """A player development snapshot for one Development Block."""

    id: int
    player_id: int
    development_block_id: int
    rating: int
    snapshot_date: date
    notes: str = ""

    def is_valid_rating(self) -> bool:
        """Return True when the rating is within the supported 1-5 scale."""
        return 1 <= self.rating <= 5
