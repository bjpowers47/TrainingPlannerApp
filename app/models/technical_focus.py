"""
Training Planner Ap
------------------------

Module:
    technical_focus.py

Purpose:
    Represents a specific skill or coaching emphasis inside a Development Block.
"""

from dataclasses import dataclass


@dataclass
class TechnicalFocus:
    """A specific focus area within a Development Block."""

    id: int
    development_block_id: int
    name: str
    description: str = ""
    active: bool = True

    def archive(self) -> None:
        """Archive the technical focus without deleting history."""
        self.active = False

    def restore(self) -> None:
        """Restore an archived technical focus."""
        self.active = True
