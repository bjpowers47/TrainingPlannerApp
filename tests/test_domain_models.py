"""
Simple domain model smoke test.

Run:
    python tests/test_domain_models.py
"""

from datetime import date
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.models import DevelopmentBlock, DevelopmentSnapshot, Drill, Player


def main():
    ball_mastery = DevelopmentBlock(
        id=1,
        name="Ball Mastery",
        description="Comfort and creativity with the ball.",
        display_order=1,
        icon="⚽",
    )

    player = Player(
        id=1,
        first_name="Emma",
        last_name="Johnson",
        birth_year=2014,
    )

    snapshot = DevelopmentSnapshot(
        id=1,
        player_id=player.id,
        development_block_id=ball_mastery.id,
        rating=3,
        snapshot_date=date.today(),
        notes="More comfortable using both feet under light pressure.",
    )

    player.add_snapshot(snapshot)
    player.add_observation("Opened her body before receiving several times today.")

    drill = Drill(
        id=1,
        name="Foundation Ball Mastery Circuit",
        development_block_id=ball_mastery.id,
        purpose="Build confidence and repetition with both feet.",
        duration_minutes=12,
    )

    drill.add_coaching_point("Small touches close to the body.")
    drill.add_coaching_point("Head up between repetitions.")

    print("Domain model smoke test")
    print("-----------------------")
    print(f"Development Block: {ball_mastery.label()}")
    print(f"Player: {player.full_name()}")
    print(f"Latest Rating: {player.latest_snapshot_for_block(ball_mastery.id).rating}")
    print(f"Observations: {len(player.observations)}")
    print(f"Drill: {drill.name}")
    print(f"Coaching Points: {len(drill.coaching_points)}")
    print("\nPASS")


if __name__ == "__main__":
    main()
