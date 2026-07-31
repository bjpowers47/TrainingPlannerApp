"""
Soccer Training Manager
-----------------------

Module:
    coaching_library.py

Coaching Library Version:
    1.0

Purpose:
    Defines the built-in Coaching Focus library for Soccer Training Manager.

    The application uses the class name TechnicalFocus internally, while
    coaches see the friendlier term "Coaching Focus" in the user interface.

Library Structure:
    Development Phase
        -> Coaching Focus
            -> Drill
"""

from app.models.technical_focus import TechnicalFocus


COACHING_LIBRARY_VERSION = "1.0"


COACHING_FOCUSES = [
    # ================================================================
    # Phase 1: Ball Mastery
    # ================================================================

    TechnicalFocus(
        id=1,
        development_block_id=1,
        name="Close Control",
        description=(
            "Keep the ball within playing distance while moving at "
            "different speeds."
        ),
    ),
    TechnicalFocus(
        id=2,
        development_block_id=1,
        name="Soft Touch",
        description=(
            "Develop light, controlled touches using different surfaces "
            "of both feet."
        ),
    ),
    TechnicalFocus(
        id=3,
        development_block_id=1,
        name="Ball Familiarity",
        description=(
            "Become comfortable stopping, moving, rolling, and manipulating "
            "the ball."
        ),
    ),
    TechnicalFocus(
        id=4,
        development_block_id=1,
        name="Head Up Dribbling",
        description=(
            "Scan the playing area while maintaining control of the ball."
        ),
    ),
    TechnicalFocus(
        id=5,
        development_block_id=1,
        name="Change of Direction",
        description=(
            "Use controlled turns to move away from pressure or into space."
        ),
    ),
    TechnicalFocus(
        id=6,
        development_block_id=1,
        name="Change of Speed",
        description=(
            "Use changes of pace to create space and move away from opponents."
        ),
    ),
    TechnicalFocus(
        id=7,
        development_block_id=1,
        name="Shielding",
        description=(
            "Protect the ball through body position, balance, and awareness."
        ),
    ),
    TechnicalFocus(
        id=8,
        development_block_id=1,
        name="Weak Foot Confidence",
        description=(
            "Develop comfort and control with the non-dominant foot."
        ),
    ),
    TechnicalFocus(
        id=9,
        development_block_id=1,
        name="Tight Space Control",
        description=(
            "Maintain possession using small touches in crowded areas."
        ),
    ),
    TechnicalFocus(
        id=10,
        development_block_id=1,
        name="Ball Confidence",
        description=(
            "Encourage creativity, experimentation, and confidence in "
            "possession."
        ),
    ),

    # ================================================================
    # Phase 2: Receiving & Passing
    # ================================================================

    TechnicalFocus(
        id=11,
        development_block_id=2,
        name="First Touch",
        description=(
            "Use the first touch to prepare the ball for the next action."
        ),
    ),
    TechnicalFocus(
        id=12,
        development_block_id=2,
        name="Receiving Across the Body",
        description=(
            "Receive the ball with the foot farther from the passer and move "
            "away from pressure."
        ),
    ),
    TechnicalFocus(
        id=13,
        development_block_id=2,
        name="Receiving on the Back Foot",
        description=(
            "Receive with an open body position so the player can see and "
            "play forward."
        ),
    ),
    TechnicalFocus(
        id=14,
        development_block_id=2,
        name="Short Passing",
        description=(
            "Develop accurate and properly weighted passes over short "
            "distances."
        ),
    ),
    TechnicalFocus(
        id=15,
        development_block_id=2,
        name="Long Passing",
        description=(
            "Deliver controlled passes over greater distances to change the "
            "point of attack."
        ),
    ),
    TechnicalFocus(
        id=16,
        development_block_id=2,
        name="One-Touch Passing",
        description=(
            "Move the ball quickly and accurately without taking an "
            "additional controlling touch."
        ),
    ),
    TechnicalFocus(
        id=17,
        development_block_id=2,
        name="Passing Accuracy",
        description=(
            "Consistently deliver the ball to the correct foot or space."
        ),
    ),
    TechnicalFocus(
        id=18,
        development_block_id=2,
        name="Weight of Pass",
        description=(
            "Match the speed and strength of a pass to the distance and "
            "situation."
        ),
    ),
    TechnicalFocus(
        id=19,
        development_block_id=2,
        name="Vision Before Receiving",
        description=(
            "Scan for teammates, opponents, and available space before the "
            "ball arrives."
        ),
    ),
    TechnicalFocus(
        id=20,
        development_block_id=2,
        name="Receiving Under Pressure",
        description=(
            "Maintain control and make effective decisions while being "
            "challenged."
        ),
    ),

    # ================================================================
    # Phase 3: 1v1 Moves
    # ================================================================

    TechnicalFocus(
        id=21,
        development_block_id=3,
        name="Body Feints",
        description=(
            "Use body movement to deceive and unbalance an opponent."
        ),
    ),
    TechnicalFocus(
        id=22,
        development_block_id=3,
        name="Scissors",
        description=(
            "Use a circular foot movement around the ball to disguise the "
            "direction of attack."
        ),
    ),
    TechnicalFocus(
        id=23,
        development_block_id=3,
        name="Stepovers",
        description=(
            "Use stepovers to create hesitation and space against a defender."
        ),
    ),
    TechnicalFocus(
        id=24,
        development_block_id=3,
        name="Matthews Move",
        description=(
            "Use inside and outside touches to shift a defender and escape "
            "into space."
        ),
    ),
    TechnicalFocus(
        id=25,
        development_block_id=3,
        name="Cruyff Turn",
        description=(
            "Use the Cruyff turn to change direction and move away from "
            "pressure."
        ),
    ),
    TechnicalFocus(
        id=26,
        development_block_id=3,
        name="Drag Back Turn",
        description=(
            "Use the sole of the foot to pull the ball away and change "
            "direction."
        ),
    ),
    TechnicalFocus(
        id=27,
        development_block_id=3,
        name="Explosive Exit",
        description=(
            "Accelerate immediately after executing a move or beating an "
            "opponent."
        ),
    ),
    TechnicalFocus(
        id=28,
        development_block_id=3,
        name="Protecting Possession",
        description=(
            "Retain the ball during physical pressure and individual duels."
        ),
    ),
    TechnicalFocus(
        id=29,
        development_block_id=3,
        name="Attacking the Defender",
        description=(
            "Approach and commit defenders with purpose and confidence."
        ),
    ),
    TechnicalFocus(
        id=30,
        development_block_id=3,
        name="Creativity",
        description=(
            "Encourage players to improvise and select moves appropriate to "
            "the situation."
        ),
    ),

    # ================================================================
    # Phase 4: Speed
    # ================================================================

    TechnicalFocus(
        id=31,
        development_block_id=4,
        name="First-Step Quickness",
        description=(
            "React and move explosively with the first step."
        ),
    ),
    TechnicalFocus(
        id=32,
        development_block_id=4,
        name="Acceleration",
        description=(
            "Reach an effective playing speed quickly and under control."
        ),
    ),
    TechnicalFocus(
        id=33,
        development_block_id=4,
        name="Deceleration",
        description=(
            "Reduce speed while maintaining balance and control."
        ),
    ),
    TechnicalFocus(
        id=34,
        development_block_id=4,
        name="Agility",
        description=(
            "Change direction efficiently while maintaining balance."
        ),
    ),
    TechnicalFocus(
        id=35,
        development_block_id=4,
        name="Reaction Speed",
        description=(
            "Respond quickly to visual, verbal, or game-related cues."
        ),
    ),
    TechnicalFocus(
        id=36,
        development_block_id=4,
        name="Speed with the Ball",
        description=(
            "Move at pace while keeping the ball under effective control."
        ),
    ),
    TechnicalFocus(
        id=37,
        development_block_id=4,
        name="Speed without the Ball",
        description=(
            "Use purposeful movement to support play, create space, or "
            "defend."
        ),
    ),
    TechnicalFocus(
        id=38,
        development_block_id=4,
        name="Transition Speed",
        description=(
            "React immediately when possession changes."
        ),
    ),
    TechnicalFocus(
        id=39,
        development_block_id=4,
        name="Recovery Runs",
        description=(
            "Recover defensively with urgency and awareness."
        ),
    ),
    TechnicalFocus(
        id=40,
        development_block_id=4,
        name="Speed of Play",
        description=(
            "Recognize situations and make effective decisions more quickly."
        ),
    ),

    # ================================================================
    # Phase 5: Finishing
    # ================================================================

    TechnicalFocus(
        id=41,
        development_block_id=5,
        name="Placement",
        description=(
            "Finish accurately by selecting an appropriate target area."
        ),
    ),
    TechnicalFocus(
        id=42,
        development_block_id=5,
        name="Power Finishing",
        description=(
            "Generate controlled shooting power using sound striking "
            "technique."
        ),
    ),
    TechnicalFocus(
        id=43,
        development_block_id=5,
        name="First-Time Finishing",
        description=(
            "Finish an opportunity without taking an unnecessary controlling "
            "touch."
        ),
    ),
    TechnicalFocus(
        id=44,
        development_block_id=5,
        name="Volleys",
        description=(
            "Strike an airborne ball with control and proper technique."
        ),
    ),
    TechnicalFocus(
        id=45,
        development_block_id=5,
        name="Half Volleys",
        description=(
            "Strike the ball effectively immediately after it bounces."
        ),
    ),
    TechnicalFocus(
        id=46,
        development_block_id=5,
        name="Heading",
        description=(
            "Direct aerial balls toward goal using safe and age-appropriate "
            "technique."
        ),
    ),
    TechnicalFocus(
        id=47,
        development_block_id=5,
        name="Composure",
        description=(
            "Remain calm and select an effective finish in front of goal."
        ),
    ),
    TechnicalFocus(
        id=48,
        development_block_id=5,
        name="Finishing Under Pressure",
        description=(
            "Finish effectively while being challenged by defenders or a "
            "goalkeeper."
        ),
    ),
    TechnicalFocus(
        id=49,
        development_block_id=5,
        name="Rebounds",
        description=(
            "React quickly and finish second-chance opportunities."
        ),
    ),
    TechnicalFocus(
        id=50,
        development_block_id=5,
        name="Finishing Angles",
        description=(
            "Recognize and select near-post, far-post, or across-goal "
            "finishing options."
        ),
    ),

    # ================================================================
    # Phase 6: Group Play
    # ================================================================

    TechnicalFocus(
        id=51,
        development_block_id=6,
        name="Give and Go",
        description=(
            "Combine with a teammate using a pass followed by an immediate "
            "supporting run."
        ),
    ),
    TechnicalFocus(
        id=52,
        development_block_id=6,
        name="Overlapping Runs",
        description=(
            "Support the player in possession by running around and beyond "
            "them."
        ),
    ),
    TechnicalFocus(
        id=53,
        development_block_id=6,
        name="Third-Player Runs",
        description=(
            "Use the movement of a third player to create a new passing "
            "option."
        ),
    ),
    TechnicalFocus(
        id=54,
        development_block_id=6,
        name="Width",
        description=(
            "Use wide positions to stretch the opposition and create space."
        ),
    ),
    TechnicalFocus(
        id=55,
        development_block_id=6,
        name="Depth",
        description=(
            "Provide options in front of and behind the ball."
        ),
    ),
    TechnicalFocus(
        id=56,
        development_block_id=6,
        name="Switching Play",
        description=(
            "Move the ball from one side of the field to the other to exploit "
            "space."
        ),
    ),
    TechnicalFocus(
        id=57,
        development_block_id=6,
        name="Support Angles",
        description=(
            "Create useful passing lanes through proper distance and angle "
            "of support."
        ),
    ),
    TechnicalFocus(
        id=58,
        development_block_id=6,
        name="Possession",
        description=(
            "Maintain the ball through movement, support, passing, and "
            "decision-making."
        ),
    ),
    TechnicalFocus(
        id=59,
        development_block_id=6,
        name="Communication",
        description=(
            "Use clear verbal and visual information to help teammates."
        ),
    ),
    TechnicalFocus(
        id=60,
        development_block_id=6,
        name="Decision Making",
        description=(
            "Recognize available options and choose an effective action under "
            "pressure."
        ),
    ),
]


def load_coaching_library(repository) -> None:
    """
    Load the built-in Coaching Focuses into a repository.

    The repository's save method handles both new and existing records,
    allowing this function to be called safely during application startup.
    """

    for coaching_focus in COACHING_FOCUSES:
        repository.save(coaching_focus)


def get_all_coaching_focuses() -> list[TechnicalFocus]:
    """Return a copy of every built-in Coaching Focus."""

    return list(COACHING_FOCUSES)


def get_coaching_focuses_by_block(
    development_block_id: int,
) -> list[TechnicalFocus]:
    """Return the Coaching Focuses belonging to one Development Phase."""

    return [
        coaching_focus
        for coaching_focus in COACHING_FOCUSES
        if coaching_focus.development_block_id == development_block_id
        and coaching_focus.active
    ]
def get_coaching_focus_names_by_block(
    development_build_id: int,
) -> list[str]:
    """
    Return the active Coaching Focus names for one Development Phase.

    The names are returned in the same order they appear in the
    Coaching Library.
    """

    return [
        coaching_focus.name
        for coaching_focus in get_coaching_focuses_by_block(
            development_build_id
        )
    ]

def get_coaching_focus_id_by_name(
    name: str,
    development_block_id: int,
) -> int | None:
    """
    Return the ID of a Coaching Focus selected by name.

    The Development Phase ID prevents a focus from accidentally being
    matched to the wrong block.
    """

    coaching_focus = get_coaching_focus_by_name(
        name=name,
        development_block_id=development_block_id,
    )

    if coaching_focus is None:
        return None

    return coaching_focus.id

def get_coaching_focus_by_id(
    coaching_focus_id: int,
) -> TechnicalFocus | None:
    """Find one Coaching Focus by ID."""

    for coaching_focus in COACHING_FOCUSES:
        if coaching_focus.id == coaching_focus_id:
            return coaching_focus

    return None


def get_coaching_focus_by_name(
    name: str,
    development_block_id: int | None = None,
) -> TechnicalFocus | None:
    """
    Find an active Coaching Focus by name.

    When a Development Phase ID is provided, the lookup is restricted
    to that block.
    """

    cleaned_name = name.strip().casefold()

    for coaching_focus in COACHING_FOCUSES:
        if not coaching_focus.active:
            continue

        if (
            development_block_id is not None
            and coaching_focus.development_block_id
            != development_block_id
        ):
            continue

        if coaching_focus.name.strip().casefold() == cleaned_name:
            return coaching_focus

    return None
def get_coaching_focus_names_by_block(
    development_block_id: int,
) -> list[str]:
    """
    Return only the names of Coaching Focuses
    for one Development Phase.
    """

    return sorted(
        [
            focus.name
            for focus in get_coaching_focuses_by_block(
                development_block_id
            )
        ]
    )