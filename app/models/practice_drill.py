from dataclasses import dataclass

from app.models.drill import Drill


@dataclass
class PracticeDrill:
    """A drill configured for use in a specific practice session."""

    drill: Drill
    order: int

    repetitions: int = 1
    work_seconds: int = 120
    rest_seconds: int = 30

    coach_notes: str = ""