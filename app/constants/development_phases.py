"""
Coach's Training Manager
------------------------

Module:
    development_phases.py

Purpose:
    Defines the Pyramid of Player Development.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class DevelopmentPhase:
    """Represents one phase of the Pyramid of Player Development."""

    id: int
    name: str
    icon: str
    description: str

BALL_MASTERY = DevelopmentPhase(
id=1,
name="Ball Mastery",
icon="⚽",
description=(
    "The non-negotiable foundation. High-repetition "
    "exercises (1 player, 1 ball) using both feet to "
    "develop a soft first touch and elite control."
),
)
DEVELOPMENT_PHASES = [
    BALL_MASTERY,
]