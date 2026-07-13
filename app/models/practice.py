"""
Coach's Training Manager
------------------------

Module:
    practice.py

Purpose:
    Represents the practice currently being built.
"""

from dataclasses import dataclass, field


@dataclass
class Practice:
    """Represents a single practice."""

    activities: dict = field(
        default_factory=lambda: {
            "Ball Mastery": [],
            "Movement": [],
            "1v1": [],
            "Small Group": [],
            "Match Application": [],
            "Review": [],
        }
    )

    def add_activity(self, phase: str, activity):
        """Add an activity to a practice phase."""

        self.activities[phase].append(activity)
    def get_phase_names(self):
        """Return the practice phases in display order."""

        return [
            "Ball Mastery",
            "Movement",
            "1v1",
            "Small Group",
            "Match Application",
            "Review",
        ]

    def has_activities(self, phase: str) -> bool:
        """Return True when a phase contains activities."""

        return len(self.activities[phase]) > 0

    def activity_count(self) -> int:
        """Return the total number of activities in the practice."""

        total = 0

        for activities in self.activities.values():
            total += len(activities)

        return total
    def remove_activity(self, phase: str, activity) -> None:
        """Remove an activity from a practice phase."""

        if activity in self.activities[phase]:
            self.activities[phase].remove(activity)
    def get_activities(self, phase: str):
        """Return all activities for a phase."""
    
        return self.activities[phase]
