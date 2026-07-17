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