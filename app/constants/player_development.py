from dataclasses import dataclass


@dataclass(frozen=True)
class DevelopmentPhase:
    """Represents one level of the Pyramid of Player Development."""

    id: int
    name: str
    icon: str
    description: str


DEVELOPMENT_PHASES = [
    DevelopmentPhase(
        1,
        "Ball Mastery",
        "⚽",
        "Develop confidence, comfort and control with the ball.",
    ),
    DevelopmentPhase(
        2,
        "Receiving & Passing",
        "🎯",
        "Develop first touch, passing accuracy and teamwork.",
    ),
    DevelopmentPhase(
        3,
        "1v1 Moves",
        "🛡️",
        "Develop the ability to beat an opponent in individual situations.",
    ),
    DevelopmentPhase(
        4,
        "Speed",
        "⚡",
        "Develop both physical speed and speed of play.",
    ),
    DevelopmentPhase(
        5,
        "Finishing",
        "🥅",
        "Develop confidence and technique in front of goal.",
    ),
    DevelopmentPhase(
        6,
        "Group Play",
        "👥",
        "Combine all skills into realistic game situations.",
    ),
]


def get_phase_names():
    return [phase.name for phase in DEVELOPMENT_PHASES]


def get_phase_by_id(phase_id):
    for phase in DEVELOPMENT_PHASES:
        if phase.id == phase_id:
            return phase
    raise ValueError(f"Unknown development phase ID: {phase_id}")


def get_phase_by_name(name):
    for phase in DEVELOPMENT_PHASES:
        if phase.name == name:
            return phase
    raise ValueError(f"Unknown development phase: {name}")


def get_display_name(name):
    phase = get_phase_by_name(name)
    return f"{phase.icon} {phase.name}"