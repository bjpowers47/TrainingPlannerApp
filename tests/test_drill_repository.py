"""
Simple test for the DrillRepository class.
"""

from app.models.drill import Drill
from app.repositories.drill_repository import DrillRepository


def main():
    repository = DrillRepository()

    drill_1 = Drill(
        id=1,
        name="Triangle Passing",
        development_block_id=2,
        technical_focus_id=1,
        purpose="Improve first touch, passing angles, and movement after the pass.",
        duration_minutes=15,
        recommended_players="6-12",
        equipment=["Balls", "Cones"],
    )

    drill_2 = Drill(
        id=2,
        name="Toe Taps and Sole Rolls",
        development_block_id=1,
        technical_focus_id=2,
        purpose="Improve comfort and control on the ball.",
        duration_minutes=10,
        recommended_players="Any",
        equipment=["Balls"],
    )

    repository.save(drill_1)
    repository.save(drill_2)

    print("Drill Repository")
    print("----------------")
    print(f"All drills: {len(repository.get_all())}")
    print(f"Drill 1: {repository.get_by_id(1).name}")
    print(f"Development Block 1 drills: {len(repository.get_by_development_block(1))}")
    print(f"Technical Focus 1 drills: {len(repository.get_by_technical_focus(1))}")

    repository.archive(1)

    print(f"All active drills after archive: {len(repository.get_all())}")
    print(f"Drill 1 active: {repository.get_by_id(1).active}")

    print("\nPASS")


if __name__ == "__main__":
    main()