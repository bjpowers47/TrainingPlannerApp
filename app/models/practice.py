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
from app.models.player_development import get_block_names
from app.models.practice_activity import PracticeActivity


@dataclass
class Practice:
    """Represents a single practice."""

    name: str = ""
    practice_date: str = ""
    team_name: str = ""
    objective: str = ""
    warm_up_minutes: float = 0
    selected_blocks: list[str] = field(default_factory=list)
    block_coaches: dict[str, list[str]] = field(default_factory=dict)
    head_coach: str = ""
    configured_blocks: list[str] = field(default_factory=list, repr=False)

    activities: dict[str, list[PracticeActivity]] = field(
        default_factory=lambda: {
            block_name: []
            for block_name in get_block_names()
        }
    )

    def add_activity(self, block: str, drill: Drill) -> None:
        """Add a drill to a practice block using the drill defaults."""

        activity = PracticeActivity.from_drill(drill)
        self.activities.setdefault(block, []).append(activity)

    def remove_activity(
        self,
        block: str,
        activity_or_drill,
    ) -> None:
        """Remove an activity or its source drill from a practice block."""

        activities = self.activities.get(block, [])

        for activity in activities:
            if (
                activity == activity_or_drill
                or activity.drill == activity_or_drill
            ):
                activities.remove(activity)
                return

    def get_activities(self, block: str) -> list[PracticeActivity]:
        """Return all activities for a block."""

        return self.activities.setdefault(block, [])

    def get_block_names(self) -> list[str]:
        """Return the practice blocks in display order."""

        return self.configured_blocks or list(self.activities)

    def has_activities(self, block: str) -> bool:
        """Return True when a block contains activities."""

        return len(self.activities.get(block, [])) > 0

    def activity_count(self) -> int:
        """Return the total number of activities in the practice."""

        return sum(
            len(activities)
            for activities in self.activities.values()
        )

    def activity_count_by_block(self) -> dict[str, int]:
        """Return the number of activities in each practice block."""

        return {
            block: len(self.activities.get(block, []))
            for block in self.get_block_names()
        }

    def total_duration(self) -> int:
        """Return the total planned practice duration in minutes."""

        total = max(0, self.warm_up_minutes)

        for activities in self.activities.values():
            for activity in activities:
                total += activity.duration_minutes()

        return round(total * 2) / 2
    def save_to_json(self, filename: str) -> None:
        """Save the practice to a JSON file."""

        file_path = Path(filename)

        practice_data = {
            "name": self.name,
            "practice_date": self.practice_date,
            "team_name": self.team_name,
            "objective": self.objective,
            "warm_up_minutes": self.warm_up_minutes,
            "selected_blocks": self.selected_blocks,
            "block_coaches": self.block_coaches,
            "head_coach": self.head_coach,
            "activities": {},
        }

        for block, activities in self.activities.items():
            practice_data["activities"][block] = [
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
                "",
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
            warm_up_minutes=max(0, float(practice_data.get("warm_up_minutes", 0) or 0)),
            selected_blocks=practice_data.get("selected_blocks", []),
            block_coaches=practice_data.get("block_coaches", {}),
            head_coach=practice_data.get("head_coach", ""),
        )

        saved_activities = practice_data.get(
            "activities",
            {},
        )

        for block, block_activities in saved_activities.items():

            if block not in practice.activities:
                practice.activities[block] = []

            for activity_data in block_activities:

                if "drill" in activity_data:
                    drill = Drill(
                        **activity_data["drill"]
                    )

                    activity = PracticeActivity(
                        drill=drill,
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
                        print_details=bool(activity_data.get("print_details", False)),
                    )

                else:
                    drill = Drill(**activity_data)
                    activity = PracticeActivity.from_drill(drill)

                practice.activities[block].append(activity)

        return practice
