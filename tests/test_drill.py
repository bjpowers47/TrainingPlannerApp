"""
Simple test for the Drill class.
"""

from app.models.drill import Drill


def main():
    drill = Drill(
        id=1,
        name="Triangle Passing",
        development_block_id=2,
        technical_focus_id=1,
        purpose="Improve first touch, passing angles, and movement after the pass.",
        duration_minutes=15,
        recommended_players="6-12",
        equipment=["Balls", "Cones"],
        notes="Good early-session technical activity.",
    )

    drill.add_coaching_point("Receive across the body.")
    drill.add_coaching_point("Open hips before receiving.")
    drill.add_coaching_point(" ")

    drill.add_progression("Add one-touch passing.")
    drill.add_variation("Use two balls for advanced groups.")

    print("Drill")
    print("-----")
    print(f"ID: {drill.id}")
    print(f"Name: {drill.name}")
    print(f"Development Block ID: {drill.development_block_id}")
    print(f"Technical Focus ID: {drill.technical_focus_id}")
    print(f"Purpose: {drill.purpose}")
    print(f"Duration: {drill.duration_minutes} minutes")
    print(f"Recommended Players: {drill.recommended_players}")
    print(f"Equipment: {', '.join(drill.equipment)}")
    print(f"Coaching Points: {drill.coaching_points}")
    print(f"Progressions: {drill.progressions}")
    print(f"Variations: {drill.variations}")
    print(f"Active: {drill.active}")

    drill.archive()
    print(f"After archive: {drill.active}")

    print("\nPASS")


if __name__ == "__main__":
    main()