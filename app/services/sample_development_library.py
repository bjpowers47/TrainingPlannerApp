"""
Coach's Training Manager
------------------------

Module:
    sample_development_library.py

Purpose:
    Loads sample Development Library data for early Alpha testing.
"""

from app.models.drill import Drill


def load_sample_drills(repository_manager):
    """Load a small set of sample drills into the DrillRepository."""

    repository_manager.drills.save(
        Drill(
            id=1,
            name="Toe Taps and Sole Rolls",
            development_block_id=1,
            technical_focus_id=1,
            purpose="Improve comfort and control on the ball.",
            duration_minutes=10,
            recommended_players="Any",
            equipment=["Balls"],
        )
    )

    repository_manager.drills.save(
        Drill(
            id=2,
            name="Triangle Passing",
            development_block_id=2,
            technical_focus_id=2,
            purpose="Improve first touch, passing angles, and movement after the pass.",
            duration_minutes=15,
            recommended_players="6-12",
            equipment=["Balls", "Cones"],
        )
    )

    repository_manager.drills.save(
        Drill(
            id=3,
            name="1v1 Gate Attack",
            development_block_id=3,
            technical_focus_id=3,
            purpose="Encourage players to attack defenders with confidence.",
            duration_minutes=15,
            recommended_players="4-10",
            equipment=["Balls", "Cones"],
        )
    )