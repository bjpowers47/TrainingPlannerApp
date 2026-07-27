"""
Coach's Training Manager
------------------------

Module:
    practice_activity.py

Purpose:
    Represents a drill as it is used in a specific practice.
"""

from dataclasses import dataclass

from app.models import drill
from app.models.drill import Drill


@dataclass
class PracticeActivity:
    """Represents a drill within a specific practice."""

    drill: Drill

    duration_override: int | None = None

    repetitions: int = 1

    rest_seconds: int = 30

    coach_notes: str = ""

    @property
    def duration_minutes(self) -> int:
        """Return the effective duration for this practice."""

        if self.duration_override is not None:
            return self.duration_override

        return self.drill.duration_minutes

    @property
    def name(self) -> str:
        """Return the drill name."""

        return self.drill.name
    def set_duration(
    self,
    minutes: int,
    ) -> None:
        """Override the drill duration."""

        self.duration_override = minutes

       