import tempfile
import unittest
from pathlib import Path

from app.database import Database
from app.repositories.development_block_repository import DevelopmentBlockRepository


class DevelopmentBlockReorderingTests(unittest.TestCase):
    def test_move_changes_persisted_display_order(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = DevelopmentBlockRepository(Database(Path(folder) / "test.db"))
            before = repository.list_all()
            self.assertGreaterEqual(len(before), 2)

            self.assertTrue(repository.move(before[1].id, -1))

            after = repository.list_all()
            self.assertEqual(after[0].id, before[1].id)
            self.assertEqual(after[1].id, before[0].id)

    def test_first_and_last_blocks_cannot_move_past_boundaries(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = DevelopmentBlockRepository(Database(Path(folder) / "test.db"))
            blocks = repository.list_all()
            self.assertFalse(repository.move(blocks[0].id, -1))
            self.assertFalse(repository.move(blocks[-1].id, 1))

    def test_drag_style_reorder_moves_block_to_target_position(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = DevelopmentBlockRepository(Database(Path(folder) / "test.db"))
            before = repository.list_all()
            moved_id = before[-1].id
            target_id = before[1].id

            self.assertTrue(repository.reorder(moved_id, target_id))

            after = repository.list_all()
            self.assertEqual(after[1].id, moved_id)


if __name__ == "__main__":
    unittest.main()
