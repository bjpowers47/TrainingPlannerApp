"""
Coach's Training Manager
------------------------

Module:
    test_practice.py

Purpose:
    Tests the Practice model.
"""

from app.models.practice import Practice
from app.models.drill import Drill


def main():
    practice = Practice()

    drill = Drill(
        id=1,
        name="Toe Taps",
        development_block_id=1
    )

    practice.add_activity("Ball Mastery", drill)

    activities = practice.get_activities("Ball Mastery")

    assert len(activities) == 1
    assert activities[0].name == "Toe Taps"

    print("✓ Practice test passed")


if __name__ == "__main__":
    main()
