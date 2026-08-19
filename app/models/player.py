"""
Wildcat Training Planner
------------------------

Module:
    player.py

Purpose:
    Represents a player and the player's development history.
"""

from dataclasses import dataclass, field
from datetime import date
from typing import List

from .development_snapshot import DevelopmentSnapshot
from .observation import Observation


@dataclass
class Player:
    """A player being coached over time."""

    id: int
    first_name: str
    last_name: str
    birth_year: int | None = None
    active: bool = True
    snapshots: List[DevelopmentSnapshot] = field(default_factory=list)
    observations: List[Observation] = field(default_factory=list)

    def full_name(self) -> str:
        """Return the player's display name."""
        return f"{self.first_name} {self.last_name}".strip()

    def add_snapshot(self, snapshot: DevelopmentSnapshot) -> None:
        """Add a development snapshot to the player's history."""
        if not snapshot.is_valid_rating():
            raise ValueError("Development snapshot rating must be between 1 and 5.")

        self.snapshots.append(snapshot)

    def add_observation(self, note: str, note_date: date | None = None) -> Observation:
        """Create and attach a coaching observation."""
        observation = Observation(
            id=0,
            player_id=self.id,
            note_date=note_date or date.today(),
            note=note,
        )

        self.observations.append(observation)

        return observation

    def latest_snapshot_for_block(self, development_block_id: int) -> DevelopmentSnapshot | None:
        """Return the most recent snapshot for a Development Block."""
        matching_snapshots = []

        for snapshot in self.snapshots:
            if snapshot.development_block_id == development_block_id:
                matching_snapshots.append(snapshot)

        if not matching_snapshots:
            return None

        matching_snapshots.sort(key=lambda snapshot: snapshot.snapshot_date)

        return matching_snapshots[-1]

    def archive(self) -> None:
        """Mark the player inactive without deleting history."""
        self.active = False
