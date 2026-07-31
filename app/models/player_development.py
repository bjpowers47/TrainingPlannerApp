from dataclasses import dataclass


@dataclass(frozen=True)
class DevelopmentBlock:
    """Represents one level of the Pyramid of Player Development."""

    id: int
    name: str
    icon: str
    description: str


DEVELOPMENT_BLOCKS = [
    DevelopmentBlock(
        1,
        "Ball Mastery",
        "⚽",
        "Develop confidence, comfort and control with the ball.",
    ),
    DevelopmentBlock(
        2,
        "Receiving & Passing",
        "🎯",
        "Develop first touch, passing accuracy and teamwork.",
    ),
    DevelopmentBlock(
        3,
        "1v1 Moves",
        "🕺",
        "Develop the ability to beat an opponent in individual situations.",
    ),
    DevelopmentBlock(
        4,
        "Speed",
        "⚡",
        "Develop both physical speed and speed of play.",
    ),
    DevelopmentBlock(
        5,
        "Finishing",
        "🥅",
        "Develop confidence and technique in front of goal.",
    ),
    DevelopmentBlock(
        6,
        "Group Play",
        "👥",
        "Combine all skills into realistic game situations.",
    ),
]

def get_block_names() -> list[str]:
    return [block.name for block in DEVELOPMENT_BLOCKS]


def get_block_by_id(block_id: int) -> DevelopmentBlock:
    for block in DEVELOPMENT_BLOCKS:
        if block.id == block_id:
            return block

    raise ValueError(
        f"Unknown development block ID: {block_id}"
    )


def get_block_by_name(name: str) -> DevelopmentBlock | None:
    """Find a development block by its plain or display name."""

    clean_name = name.strip()

    for block in DEVELOPMENT_BLOCKS:
        display_name = f"{block.icon} {block.name}"

        if clean_name.casefold() in {
            block.name.casefold(),
            display_name.casefold(),
        }:
            return block

    return None


def get_display_name(name: str) -> str:
    """Return the icon and name used by the user interface."""

    block = get_block_by_name(name)

    if block is None:
        raise ValueError(f"Unknown development block: {name}")

    return f"{block.icon} {block.name}"