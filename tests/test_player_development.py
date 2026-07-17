"""
Unit tests for player_development.py
"""

import unittest

from app.constants.player_development import (
    DEVELOPMENT_PHASES,
    get_display_name,
    get_phase_by_id,
    get_phase_by_name,
    get_phase_names,
)


class TestPlayerDevelopment(unittest.TestCase):

    def test_phase_count(self):
        """There should be six development phases."""
        self.assertEqual(len(DEVELOPMENT_PHASES), 6)

    def test_get_phase_names(self):
        """Verify the phase names are returned in order."""
        expected = [
            "Ball Mastery",
            "Receiving & Passing",
            "1v1 Moves",
            "Speed",
            "Finishing",
            "Group Play",
        ]
        self.assertEqual(get_phase_names(), expected)

    def test_get_phase_by_id(self):
        """Verify a phase can be retrieved by ID."""
        phase = get_phase_by_id(1)
        self.assertEqual(phase.name, "Ball Mastery")
        self.assertEqual(phase.icon, "⚽")

    def test_get_phase_by_name(self):
        """Verify a phase can be retrieved by name."""
        phase = get_phase_by_name("Speed")
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
            get_phase_by_id(999)

    def test_invalid_phase_name(self):
        """Invalid names should raise ValueError."""
        with self.assertRaises(ValueError):
            get_phase_by_name("Goalkeeping")


if __name__ == "__main__":
    unittest.main()