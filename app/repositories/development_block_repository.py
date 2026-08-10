"""Repository for Development Blocks."""

from __future__ import annotations

import sqlite3
from contextlib import closing

from app.database import Database
from app.models.development_block import DevelopmentBlock


class DevelopmentBlockRepository:
    """Reads Development Blocks from the database."""

    def __init__(self, database: Database):
        self.database = database

    def list_active(self) -> list[DevelopmentBlock]:
        """Return all active Development Blocks in display order."""
        self.database.initialize()
        with closing(self.database.connect()) as connection:
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

    def list_all(self):
        return self.list_active()

    def get_by_id(self, block_id: int):
        return next((block for block in self.list_active() if block.id == block_id), None)

    def get_by_name(self, name: str):
        return next((block for block in self.list_active() if block.name == name), None)

    def create(self, name: str) -> None:
        self.database.initialize()
        with closing(self.database.connect()) as connection, connection:
            order = connection.execute("SELECT COALESCE(MAX(display_order), 0) + 1 FROM development_blocks").fetchone()[0]
            candidate = name
            suffix = 2
            while connection.execute("SELECT 1 FROM development_blocks WHERE name=?", (candidate,)).fetchone():
                candidate = f"{name} {suffix}"
                suffix += 1
            connection.execute("INSERT INTO development_blocks (name, display_order) VALUES (?, ?)", (candidate, order))

    def rename(self, block_id: int, name: str) -> None:
        name = name.strip()
        if not name:
            raise ValueError("Block name cannot be empty.")

        with closing(self.database.connect()) as connection, connection:
            duplicate = connection.execute(
                """
                SELECT id, is_active
                FROM development_blocks
                WHERE name = ? COLLATE NOCASE AND id != ?
                """,
                (name, block_id),
            ).fetchone()
            if duplicate and duplicate["is_active"]:
                raise ValueError(f'A block named "{name}" already exists.')
            if duplicate:
                try:
                    # Older versions hid deleted blocks instead of removing
                    # them, leaving their UNIQUE names reserved forever.
                    connection.execute(
                        "DELETE FROM development_blocks WHERE id=?",
                        (duplicate["id"],),
                    )
                except sqlite3.IntegrityError:
                    # Preserve a referenced archived block by restoring it in
                    # place of the unused placeholder being renamed.
                    current = connection.execute(
                        "SELECT display_order FROM development_blocks WHERE id=?",
                        (block_id,),
                    ).fetchone()
                    try:
                        connection.execute(
                            "DELETE FROM development_blocks WHERE id=?",
                            (block_id,),
                        )
                    except sqlite3.IntegrityError as error:
                        raise ValueError(
                            f'The archived block named "{name}" is used by saved data and cannot replace this block.'
                        ) from error
                    connection.execute(
                        """
                        UPDATE development_blocks
                        SET name=?, is_active=1, display_order=?, updated_at=CURRENT_TIMESTAMP
                        WHERE id=?
                        """,
                        (name, current["display_order"], duplicate["id"]),
                    )
                    return
            connection.execute("UPDATE development_blocks SET name=?, updated_at=CURRENT_TIMESTAMP WHERE id=?", (name, block_id))

    def delete(self, block_id: int) -> None:
        with closing(self.database.connect()) as connection, connection:
            count = connection.execute(
                "SELECT COUNT(*) FROM drills WHERE development_block_id=? AND is_active=1",
                (block_id,),
            ).fetchone()[0]
            if count:
                raise ValueError(f"This block has {count} drill(s). Reassign them before deleting it.")
            try:
                # Drill deletion in the UI is an archive operation. Once the
                # parent block is explicitly deleted, those hidden drill rows
                # and its focus rows no longer serve a purpose and would
                # otherwise prevent the block from being removed.
                connection.execute(
                    "DELETE FROM drills WHERE development_block_id=? AND is_active=0",
                    (block_id,),
                )
                connection.execute(
                    "DELETE FROM technical_focuses WHERE development_block_id=?",
                    (block_id,),
                )
                # A soft-deleted row keeps its UNIQUE name and prevents the user
                # from creating another block with that name. Remove unused
                # blocks so their names are genuinely available again.
                connection.execute("DELETE FROM development_blocks WHERE id=?", (block_id,))
            except sqlite3.IntegrityError as error:
                raise ValueError(
                    "This block is used by saved development or practice data and cannot be deleted."
                ) from error
