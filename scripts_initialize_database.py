"""Initialize the Coach's Training Manager SQLite database.

Run from the project root:

    python scripts_initialize_database.py
"""

from app.database import Database
from app.repositories.development_block_repository import DevelopmentBlockRepository


def main() -> None:
    database = Database()
    database.initialize()

    repository = DevelopmentBlockRepository(database)
    development_blocks = repository.list_active()

    print("Database initialized.")
    print()
    print("Development Blocks")
    print("------------------")

    for block in development_blocks:
        print(f"{block.display_order}. {block.name}")


if __name__ == "__main__":
    main()
