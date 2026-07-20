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
def get_phase_names() -> list[str]:
    """Return the names of all development phases."""
    return [phase.name for phase in DEVELOPMENT_PHASES]


def get_phase_by_id(phase_id: int) -> DevelopmentPhase:
    """Return a development phase by its ID."""
    for phase in DEVELOPMENT_PHASES:
        if phase.id == phase_id:
            return phase
    raise ValueError(f"Unknown development phase ID: {phase_id}")


def get_phase_by_name(name: str):
    """Return a DevelopmentPhase by its display name."""
    print(f"get_phase_by_name() called with: {name}")
    # Remove the icon if present
    clean_name = name.replace("⚽ ", "").replace("🎯 ", "").strip()
    print(f"Cleaned name: {clean_name}")
    for phase in DEVELOPMENT_PHASES:
        if phase.name == clean_name:
            return phase

    return None

def get_display_name(name: str) -> str:
    """Return the icon and name for display in the UI."""
    phase = get_phase_by_name(name)
    return f"{phase.icon} {phase.name}"