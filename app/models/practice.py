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

    def get_activities(self, phase: str):
        """Return all activities for a phase."""

        return self.activities[phase]
    def activity_count(self) -> int:
        """Return the total number of activities in the practice."""

        total = 0

        for activities in self.activities.values():
            total += len(activities)

        return total