"""
Simple test for the TechnicalFocus class.
"""

from app.models.technical_focus import TechnicalFocus


def main():
    focus = TechnicalFocus(
        id=1,
        development_block_id=1,
        name="First Touch",
        description="Improve control with the first touch.",
    )

    print("Technical Focus")
    print("---------------")
    print(f"ID: {focus.id}")
    print(f"Development Block ID: {focus.development_block_id}")
    print(f"Name: {focus.name}")
    print(f"Description: {focus.description}")
    print(f"Active: {focus.active}")

    focus.archive()
    print(f"After archive: {focus.active}")

    focus.restore()
    print(f"After restore: {focus.active}")

    print("\nPASS")


if __name__ == "__main__":
    main()