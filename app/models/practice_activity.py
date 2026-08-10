"""
Training Planner Ap
------------------------

Module:
    practice_activity.py

Purpose:
    Represents a drill as it is used in a specific practice.
"""

from dataclasses import dataclass

from app.models.drill import Drill


@dataclass
class PracticeActivity:
    """
    Represents one drill scheduled within a specific practice.

    The execution values belong to the practice activity, not to the
    Development Library drill. This allows a coach to change today's
    plan without changing the reusable drill defaults.
    """

    drill: Drill

    sets: int = 1
    reps: str = ""  # retained only for loading older practice files
    work_seconds: float | None = 0
    rest_seconds: float | None = 0

    coach_notes: str = ""
    print_details: bool = False
    duration_override: float | None = None

    @classmethod
    def from_drill(cls, drill: Drill) -> "PracticeActivity":
        """
        Create a practice activity using the drill's execution defaults.

        After creation, the values can be edited independently without
        modifying the original drill.
        """

        return cls(
            drill=drill,
            sets=drill.sets,
            reps=str(drill.reps) if drill.reps is not None else "",
            work_seconds=drill.work_seconds,
            rest_seconds=drill.rest_seconds,
        )

    @property
    def name(self) -> str:
        """Return the drill name."""

        return self.drill.name
    def duration_seconds(self) -> int:
        work_seconds = self.work_seconds or 0
        rest_seconds = self.rest_seconds or 0
        sets = self.sets or 1

        return sets * (work_seconds + rest_seconds)

    @property
    def work_minutes(self) -> float:
        return (self.work_seconds or 0) / 60

    @work_minutes.setter
    def work_minutes(self, value: float | None) -> None:
        self.work_seconds = None if value is None else value * 60

    @property
    def rest_minutes(self) -> float:
        return (self.rest_seconds or 0) / 60

    @rest_minutes.setter
    def rest_minutes(self, value: float | None) -> None:
        self.rest_seconds = None if value is None else value * 60

    def duration_minutes(self) -> float:
        if self.duration_override is not None:
            return max(0, float(self.duration_override))
        execution_minutes = self.duration_seconds() / 60
        return execution_minutes if execution_minutes > 0 else max(0, self.drill.duration_minutes)
