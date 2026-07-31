"""
Unit tests for player_development.py
"""

import unittest

from app.models.player_development import (
    DEVELOPMENT_BLOCKS,
    get_display_name,
    get_block_by_id,
    get_block_by_name,
    get_block_names,
)


class TestPlayerDevelopment(unittest.TestCase):

    def test_phase_count(self):
        """There should be six development phases."""
        self.assertEqual(len(DEVELOPMENT_BLOCKS), 6)

    def test_get_block_names(self):
        """Verify the phase names are returned in order."""
        expected = [
            "Ball Mastery",
            "Receiving & Passing",
            "1v1 Moves",
            "Speed",
            "Finishing",
            "Group Play",
        ]
        self.assertEqual(get_block_names(), expected)

    def test_get_block_by_id(self):
        """Verify a phase can be retrieved by ID."""
        phase = get_block_by_id(1)
        self.assertEqual(phase.name, "Ball Mastery")
        self.assertEqual(phase.icon, "⚽")

    def test_get_block_by_name(self):
        """Verify a phase can be retrieved by name."""
        phase = get_block_by_name("Speed")
        self.assertEqual(phase.id, 4)
        self.assertEqual(phase.icon, "⚡")

    def test_get_display_name(self):
        """Verify the display name includes the icon."""
        self.assertEqual(
            get_display_name("Finishing"),
            "🥅 Finishing",
        )

    def test_invalid_phase_id(self):
        """Invalid IDs should raise ValueError."""
        with self.assertRaises(ValueError):
            get_block_by_id(999)

    def test_invalid_phase_name(self):
        """Invalid names should raise ValueError."""
        with self.assertRaises(ValueError):
            get_block_by_name("Goalkeeping")


if __name__ == "__main__":
    unittest.main()