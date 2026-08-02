"""
Coach's Training Manager
------------------------

Module:
    development_blocks.py

Purpose:
    Defines the Pyramid of Player Development.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class DevelopmentBlock:
    """Represents one phase of the Pyramid of Player Development."""

    id: int
    name: str
    icon: str
    description: str

BALL_MASTERY = DevelopmentBlock(
id=1,
name="Ball Mastery",
icon="⚽",
description=(
    "The non-negotiable foundation. High-repetition "
    "exercises (1 player, 1 ball) using both feet to "
    "develop a soft first touch and elite control."
),
)
DEVELOPMENT_BLOCKS = [
    BALL_MASTERY,
]