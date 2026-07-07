"""
Simple test for the DevelopmentBlock class.
"""

from app.models.development_block import DevelopmentBlock


def main():

    block = DevelopmentBlock(
        id=1,
        name="Ball Mastery",
        description="Develop confidence and control on the ball.",
        display_order=1,
    )

    print("Development Block")
    print("-----------------")
    print(f"ID: {block.id}")
    print(f"Name: {block}")
    print(f"Description: {block.description}")
    print(f"Display Order: {block.display_order}")

    print("\nPASS")


if __name__ == "__main__":
    main()