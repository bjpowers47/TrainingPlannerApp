"""
Coach's Training Manager
------------------------

Module:
    test_practice.py

Purpose:
    Unit tests for the Practice model.
"""

from app.models.drill import Drill
from app.models.practice import Practice


def test_practice():

    practice = Practice()

    drill = Drill(
        id=1,
        name="Toe Taps",
        development_block_id=1,
        purpose="",
        duration_minutes=10,
        recommended_players="",
    )

    #
    # Add Activity
    #
    practice.add_activity(
        "Ball Mastery",
        drill,
    )

    assert practice.activity_count() == 1
    assert len(practice.get_activities("Ball Mastery")) == 1

    #
    # Total Duration
    #
    assert practice.total_duration() == 10

    #
    # Remove Activity
    #
    practice.remove_activity(
        "Ball Mastery",
        drill,
    )

    assert practice.activity_count() == 0
    assert len(practice.get_activities("Ball Mastery")) == 0

    #
    # Save to JSON
    #
    practice.name = "Tuesday Ball Mastery"

    practice.add_activity(
        "Ball Mastery",
        drill,
    )

    practice.save_to_json(
        "data/test_practice.json"
    )

    print("✓ Practice JSON saved")
    
    loaded_practice = Practice.load_from_json(
        "data/test_practice.json"
    )

    assert loaded_practice.name == "Tuesday Ball Mastery"
    assert loaded_practice.activity_count() == 1
    assert loaded_practice.total_duration() == 10

    loaded_activities = loaded_practice.get_activities(
        "Ball Mastery"
    )

    assert len(loaded_activities) == 1
    assert loaded_activities[0].name == "Toe Taps"

    print("✓ Practice JSON loaded")
    print("✓ Practice test passed")

if __name__ == "__main__":
    test_practice()
"""Tests for the Practice domain model."""

import tempfile
from pathlib import Path

from app.models.practice import Practice


def test_practice_information_is_saved_and_loaded():
    """Practice information should survive a JSON round trip."""

    practice = Practice(
        name="Tuesday Training",
        practice_date="2026-07-28",
        team_name="U12 Boys",
        objective="Improve first touch under pressure.",
    )

    with tempfile.TemporaryDirectory() as temporary_directory:
        filename = Path(temporary_directory) / "practice.json"

        practice.save_to_json(str(filename))
        restored_practice = Practice.load_from_json(str(filename))

    assert restored_practice.name == "Tuesday Training"
    assert restored_practice.practice_date == "2026-07-28"
    assert restored_practice.team_name == "U12 Boys"
    assert (
        restored_practice.objective
        == "Improve first touch under pressure."
    )
def test_practice_activity_is_saved_and_loaded():
    """A PracticeActivity should survive a JSON round trip."""

    drill = Drill(
        id=1,
        name="Ball Taps",
        development_block_id=1,
        technical_focus_id=None,
        purpose="Control",
        duration_minutes=10,
        recommended_players="1+",
    )

    practice = Practice()
    phase = practice.get_phase_names()[0]

    practice.add_activity(
        phase,
        drill,
    )

    with tempfile.TemporaryDirectory() as temporary_directory:
        filename = (
            Path(temporary_directory)
            / "practice.json"
        )

        practice.save_to_json(filename)

        loaded_practice = Practice.load_from_json(
            filename
        )

    loaded_activity = loaded_practice.get_activities(
        phase
    )[0]

    assert loaded_activity.name == "Ball Taps"
    assert loaded_activity.duration_minutes == 10
    assert loaded_activity.repetitions == 1
    assert loaded_activity.rest_seconds == 30

if __name__ == "__main__":
    test_practice()
    test_practice_information_is_saved_and_loaded()
    test_practice_activity_is_saved_and_loaded()

    print("All Practice tests passed.")