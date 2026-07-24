from dataclasses import dataclass, field
from datetime import date

from app.models.practice_drill import PracticeDrill


@dataclass
class PracticeSession:
    """A coach's planned training session."""

    id: int
    title: str
    session_date: date

    team_name: str = ""
    objective: str = ""

    drills: list[PracticeDrill] = field(default_factory=list)

    def add_drill(self, practice_drill: PracticeDrill):
        """Add a drill to the practice."""
        self.drills.append(practice_drill)

    def remove_drill(self, practice_drill: PracticeDrill):
        """Remove a drill from the practice."""
        self.drills.remove(practice_drill)
    def move_drill_up(self, index: int):
        """Move a drill one position earlier in the practice."""

        if 0 < index < len(self.drills):
            self.drills[index - 1], self.drills[index] = (
                self.drills[index],
                self.drills[index - 1],
            )

            self.drills[index - 1].order = index
            self.drills[index].order = index + 1


    def move_drill_down(self, index: int):
        """Move a drill one position later in the practice."""

        if 0 <= index < len(self.drills) - 1:
            self.drills[index], self.drills[index + 1] = (
                self.drills[index + 1],
                self.drills[index],
            )

            self.drills[index].order = index + 1
            self.drills[index + 1].order = index + 2