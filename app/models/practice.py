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
from app.models.practice_activity import PracticeActivity


@dataclass
class Practice:
    """Represents a single practice."""

    name: str = "Untitled Practice"
    practice_date: str = ""
    team_name: str = ""
    objective: str = ""

    activities: dict[str, list[PracticeActivity]] = field(
        default_factory=lambda: {
            phase_name: []
            for phase_name in get_phase_names()
        }
    )

    def add_activity(self, phase: str, drill: Drill) -> None:
        """Add a drill to a practice phase using the drill defaults."""

        activity = PracticeActivity.from_drill(drill)
        self.activities[phase].append(activity)

    def remove_activity(
        self,
        phase: str,
        activity_or_drill,
    ) -> None:
        """Remove an activity or its source drill from a practice phase."""

        activities = self.activities.get(phase, [])

        for activity in activities:
            if (
                activity == activity_or_drill
                or activity.drill == activity_or_drill
            ):
                activities.remove(activity)
                return

    def get_activities(self, phase: str) -> list[PracticeActivity]:
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

        return sum(
            len(activities)
            for activities in self.activities.values()
        )

    def activity_count_by_phase(self) -> dict[str, int]:
        """Return the number of activities in each practice phase."""

        return {
            phase: len(self.activities.get(phase, []))
            for phase in self.get_phase_names()
        }

    def total_duration(self) -> int:
        """Return the total planned practice duration in minutes."""

        total = 0

        for activities in self.activities.values():
            for activity in activities:
                total += activity.calculated_duration_minutes()

        return round(total)
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
            practice_data["activities"][phase] = [
                asdict(activity)
                for activity in activities
            ]

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
    def load_from_json(cls, filename: str) -> "Practice":
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

        for phase, phase_activities in saved_activities.items():

            if phase not in practice.activities:
                practice.activities[phase] = []

            for activity_data in phase_activities:

                if "drill" in activity_data:
                    drill = Drill(
                        **activity_data["drill"]
                    )

                    activity = PracticeActivity(
                        drill=drill,
                        manual_duration_minutes=activity_data.get(
                            "duration_minutes"
                        ),
                        sets=activity_data.get("sets"),
                        reps=activity_data.get(
                            "reps",
                            activity_data.get("repetitions"),
                        ),
                        work_seconds=activity_data.get(
                            "work_seconds"
                        ),
                        rest_seconds=activity_data.get(
                            "rest_seconds"
                        ),
                        coach_notes=activity_data.get(
                            "coach_notes",
                            "",
                        ),
                    )

                    if (
                        "duration_minutes" not in activity_data
                        and "duration_override" in activity_data
                    ):
                        duration_override = activity_data.get(
                            "duration_override"
                        )

                        if duration_override is None:
                            activity.manual_duration_minutes = (
                                drill.duration_minutes
                            )
                        else:
                            activity.manual_duration_minutes = (
                                duration_override
                            )

                else:
                    drill = Drill(**activity_data)
                    activity = PracticeActivity.from_drill(drill)

                practice.activities[phase].append(activity)

        return practice
