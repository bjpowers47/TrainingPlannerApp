"""
Simple test for loading sample Development Library data.
"""

from app.repositories.repository_manager import RepositoryManager
from app.services.sample_development_library import load_sample_drills
from app.services.development_library_service import DevelopmentLibraryService


def main():
    repositories = RepositoryManager()
    load_sample_drills(repositories)

    service = DevelopmentLibraryService(repositories.drills)

    print("Sample Development Library")
    print("--------------------------")
    print(f"Total drills: {len(service.get_all_drills())}")
    print(f"Ball Mastery drills: {len(service.get_drills_for_block(1))}")
    print(f"Receiving & Passing drills: {len(service.get_drills_for_block(2))}")
    print(f"1v1 Moves drills: {len(service.get_drills_for_block(3))}")

    print("\nPASS")


if __name__ == "__main__":
    main()