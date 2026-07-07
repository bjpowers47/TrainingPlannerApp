"""
Coach's Training Manager
------------------------

Module:
    development_block.py

Purpose:
    Represents one of the core Coerver-inspired Development Blocks.

Design Note:
    Development Blocks are the foundation of the coaching model. They are
    intentionally simple and stable. The application may add technical focuses,
    drills, practices, and assessments around them, but these blocks remain the
    organizing language of the system.
"""

from dataclasses import dataclass


@dataclass
class DevelopmentBlock:
    """A major area of player development."""

    id: int
    name: str
    description: str
    display_order: int
    icon: str = ""
    active: bool = True

    def label(self) -> str:
        """Return the display label shown in the user interface."""
        if self.icon:
            return f"{self.icon} {self.name}"

        return self.name

    def archive(self) -> None:
        """Archive the block without deleting history."""
        self.active = False

    def restore(self) -> None:
        """Restore an archived block."""
        self.active = True
