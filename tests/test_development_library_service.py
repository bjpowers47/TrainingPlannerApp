"""
Simple test for the DevelopmentLibraryService.
"""

from app.models.drill import Drill
from app.repositories.drill_repository import DrillRepository
from app.services.development_library_service import DevelopmentLibraryService


def main():

    repository = DrillRepository()

    repository.save(
        Drill(
            id=1,
            name="Triangle Passing",
            development_block_id=2,
            technical_focus_id=1,
            purpose="Improve passing.",
        )
    )

    repository.save(
        Drill(
            id=2,
            name="Toe Taps",
            development_block_id=1,
            technical_focus_id=2,
            purpose="Improve ball mastery.",
        )
    )

    service = DevelopmentLibraryService(repository)

    print("Development Library Service")
    print("---------------------------")

    print(f"Total Drills: {len(service.get_all_drills())}")

    print(
        f"Ball Mastery Drills: "
        f"{len(service.get_drills_for_block(1))}"
    )

    print(
        f"Passing Drills: "
        f"{len(service.get_drills_for_block(2))}"
    )

    print("\nPASS")


if __name__ == "__main__":
    main()