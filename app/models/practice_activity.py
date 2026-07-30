"""
Coach's Training Manager
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

    manual_duration_minutes: int | None = None
    sets: int | None = None
    reps: str = ""
    work_seconds: int | None = None
    rest_seconds: int | None = None

    coach_notes: str = ""

    @classmethod
    def from_drill(cls, drill: Drill) -> "PracticeActivity":
        """
        Create a practice activity using the drill's execution defaults.

        After creation, the values can be edited independently without
        modifying the original drill.
        """

        return cls(
            drill=drill,
            manual_duration_minutes=drill.duration_minutes,
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
        """
        Return the activity duration in seconds.

        Interval activities are calculated from sets, work, and rest.
        There is no rest period after the final set.

        Activities without interval values use the manually entered duration.
        """

        sets = self.sets or 0
        work_seconds = self.work_seconds or 0
        rest_seconds = self.rest_seconds or 0

        if sets > 0 and work_seconds > 0:
            total_work = sets * work_seconds
            total_rest = max(sets - 1, 0) * rest_seconds

            return total_work + total_rest

        return (self.manual_duration_minutes or 0) * 60


    def calculated_duration_minutes(self) -> float:
        """Return the calculated duration in minutes."""

        return self.duration_seconds() / 60