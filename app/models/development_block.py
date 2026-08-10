"""
Training Planner Ap
------------------------

Module:
    development_block.py

Purpose:
    Represents one of the six Development Blocks used throughout
    Training Planner Ap.

Responsibilities:
    • Store the Development Block information.
    • Store the display order.
    • Store the description.

Collaborates With:
    TechnicalFocus
    Drill

Author:
    Bob Powers
    OpenAI

Created:
    July 2026
"""

from dataclasses import dataclass


@dataclass
class DevelopmentBlock:
    """
    Represents a Development Block within the coaching model.
    """

    id: int
    name: str
    description: str
    display_order: int
    is_active: bool = True

    def __str__(self) -> str:
        """Return a friendly display name."""
        return self.name
