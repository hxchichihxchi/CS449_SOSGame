import unittest

from gameLogic import GameLogic
from gui import MenuPage, GamePage, SOSApp

class TestSOSGame(unittest.TestCase):

    def test_valid_board_sizes_range(self):
        """Test multiple valid board sizes."""
        # Modified to test multiple valid sizes.
        valid_sizes = [3, 5, 8, 10]
        for size in valid_sizes:
            with self.subTest(size=size):
                game = GameLogic(size)
                self.assertEqual(len(game.board), size)
                self.assertTrue(all(len(row) == size for row in game.board))

    def test_invalid_board_size_raises_error(self):
        """Bad inputs should raise errors."""
        bad_sizes = [0, -1, 1, "five", 16, None]    # Added upper limit fail case
        for size in bad_sizes:
            with self.subTest(size=size):
                with self.assertRaises((ValueError, TypeError)):
                    GameLogic(size)

    def test_start_simple_game(self):
        app = SOSApp()
        app.grid_size = 3
        app.mode = "simple"
        app.show_frame("GamePage")
        frame = app.frames["GamePage"]
        self.assertEqual(frame.mode_label['text'], "Mode: Simple")
        self.assertEqual(len(frame.board_frame.winfo_children()), 3*3)

    def test_start_general_game(self):
        app = SOSApp()
        app.grid_size = 3
        app.mode = "general"
        app.show_frame("GamePage")
        frame = app.frames["GamePage"]
        self.assertEqual(frame.mode_label['text'], "Mode: General")
        self.assertEqual(len(frame.board_frame.winfo_children()), 3*3)

    def test_start_no_mode_selected(self):
        class DummyController:
            def __init__(self):
                self.grid_size = 3
                self.mode = None
            def show_frame(self, page_name):
                self.frame_shown = page_name
        controller = DummyController()
        menu = MenuPage(None, controller)
        menu.entry.insert(0, '5')
        menu.selected_option.set("")
        menu.start_game()
        self.assertNotEqual(menu.alert_label['text'], "")

    def test_simple_valid_move(self):
        logic = GameLogic(3)
        logic.current_player = 'p1'
        self.assertTrue(logic.place_letter(0, 0, 'S'))
        self.assertEqual(logic.board[0][0], 'S')
    
    def test_general_valid_move(self):
        logic = GameLogic(3)
        logic.current_player = 'p2'
        self.assertTrue(logic.place_letter(1, 1, 'O'))
        self.assertEqual(logic.board[1][1], 'O')

    def test_simple_invalid_move(self):
        logic = GameLogic(3)
        logic.place_letter(0, 0, 'S')
        logic.current_player = 'p1'
        self.assertFalse(logic.place_letter(0, 0, 'O'))
        self.assertEqual(logic.board[0][0], 'S')
    
    def test_general_invalid_move(self):
        logic = GameLogic(3)
        logic.place_letter(1, 1, 'O')  # first valid move
        logic.current_player = 'p2'
        self.assertFalse(logic.place_letter(1, 1, 'S'))  # invalid, already occupied
        self.assertEqual(logic.board[1][1], 'O')

if __name__ == "__main__":
    unittest.main()