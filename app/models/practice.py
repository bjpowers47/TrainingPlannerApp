"""
Coach's Training Manager
------------------------

Module:
    practice.py

Purpose:
    Represents the practice currently being built.
"""

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from app.models.drill import Drill
from app.models.player_development import get_phase_names


@dataclass
class Practice:
    """Represents a single practice."""

    name: str = "Untitled Practice"
    practice_date: str = ""
    team_name: str = ""
    objective: str = ""

    activities: dict[str, list[Drill]] = field(
        default_factory=lambda: {
            phase_name: []
            for phase_name in get_phase_names()
        }
    )
    

    def add_activity(self, phase: str, activity) -> None:
        """Add an activity to a practice phase."""

        self.activities[phase].append(activity)

    def remove_activity(self, phase: str, activity) -> None:
        """Remove an activity from a practice phase."""

        if activity in self.activities[phase]:
            self.activities[phase].remove(activity)

    def get_activities(self, phase: str):
        """Return all activities for a phase."""

        return self.activities[phase]

    def get_phase_names(self) -> list[str]:
        """Return the practice phases in display order."""
        return get_phase_names()

    def has_activities(self, phase: str) -> bool:
        """Return True when a phase contains activities."""

        return len(self.activities[phase]) > 0

    def activity_count(self) -> int:
        """Return the total number of activities in the practice."""

        total = 0

        for activities in self.activities.values():
            total += len(activities)

        return total

    def total_duration(self) -> int:
        """Return the total estimated practice duration in minutes."""

        total = 0

        for activities in self.activities.values():
            for activity in activities:
                total += activity.duration_minutes

        return total

    def save_to_json(self, filename: str) -> None:
        """Save the practice to a JSON file."""

        file_path = Path(filename)

        practice_data = {
            "name": self.name,
            "practice_date": self.practice_date,
            "team_name": self.team_name,
            "objective": self.objective,
            "activities": {},
        }

        for phase, activities in self.activities.items():
            practice_data["activities"][phase] = []

            for activity in activities:
                practice_data["activities"][phase].append(
                    asdict(activity)
                )

        with file_path.open(
            "w",
            encoding="utf-8",
        ) as output_file:
            json.dump(
                practice_data,
                output_file,
                indent=4,
            )
    @classmethod
    def load_from_json(cls, filename: str):
        """Create a Practice from a saved JSON file."""

        file_path = Path(filename)

        with file_path.open(
            "r",
            encoding="utf-8",
        ) as input_file:
            practice_data = json.load(input_file)

        practice = cls(
            name=practice_data.get(
                "name",
                "Untitled Practice",
            ),
            practice_date=practice_data.get(
                "practice_date",
                "",
            ),
            team_name=practice_data.get(
                "team_name",
                "",
            ),
            objective=practice_data.get(
                "objective",
                "",
            ),
        )

        saved_activities = practice_data.get(
            "activities",
            {},
        )

        for phase in practice.get_phase_names():
            phase_activities = saved_activities.get(
                phase,
                [],
            )

            for activity_data in phase_activities:
                practice.add_activity(
                    phase,
                    Drill(**activity_data),
                )

        return practice