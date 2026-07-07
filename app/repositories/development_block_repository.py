"""Repository for Development Blocks."""

from __future__ import annotations

from app.database import Database
from app.models.development_block import DevelopmentBlock


class DevelopmentBlockRepository:
    """Reads Development Blocks from the database."""

    def __init__(self, database: Database):
        self.database = database

    def list_active(self) -> list[DevelopmentBlock]:
        """Return all active Development Blocks in display order."""
        with self.database.connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    id,
                    name,
                    description,
                    display_order,
                    is_active
                FROM development_blocks
                WHERE is_active = 1
                ORDER BY display_order;
                """
            ).fetchall()

        blocks = []

        for row in rows:
            block = DevelopmentBlock(
                id=row["id"],
                name=row["name"],
                description=row["description"],
                display_order=row["display_order"],
                is_active=bool(row["is_active"]),
            )
            blocks.append(block)

        return blocks
