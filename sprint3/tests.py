import unittest
from gameLogic import GameLogic
from gui import MenuPage, GamePage, SOSApp

class TestSOSGame(unittest.TestCase):

    def test_valid_board_sizes_range(self):
        """Test multiple valid board sizes."""
        valid_sizes = [3, 5, 8, 10]
        for size in valid_sizes:
            with self.subTest(size=size):
                game = GameLogic(size, "simple")
                board = game.game_mode.board
                self.assertEqual(len(board), size)
                self.assertTrue(all(len(row) == size for row in board))

    def test_invalid_board_size_raises_error(self):
        """Bad inputs should raise errors."""
        bad_sizes = [0, -1, 1, "five", 16, None]
        for size in bad_sizes:
            with self.subTest(size=size):
                with self.assertRaises((ValueError, TypeError)):
                    GameLogic(size, "simple")

    def test_start_simple_game(self):
        app = SOSApp()
        app.grid_size = 3
        app.mode = "simple"
        app.show_frame("GamePage")
        frame = app.frames["GamePage"]
        self.assertEqual(frame.mode_label['text'], "Simple Game")
        self.assertEqual(len(frame.board_frame.winfo_children()), 3 * 3)

    def test_start_general_game(self):
        app = SOSApp()
        app.grid_size = 3
        app.mode = "general"
        app.show_frame("GamePage")
        frame = app.frames["GamePage"]
        self.assertEqual(frame.mode_label['text'], "General Game")
        self.assertEqual(len(frame.board_frame.winfo_children()), 3 * 3)

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
        logic = GameLogic(3, "simple")
        result = logic.place_letter(0, 0, "S")
        self.assertTrue(result["valid"])
        self.assertEqual(logic.game_mode.board[0][0], "S")

    def test_simple_invalid_move(self):
        logic = GameLogic(3, "simple")
        logic.place_letter(0, 0, "S")
        result = logic.place_letter(0, 0, "O")
        self.assertFalse(result["valid"])
        self.assertEqual(logic.game_mode.board[0][0], "S")

    def test_general_valid_move(self):
        logic = GameLogic(3, "general")
        result = logic.place_letter(1, 1, "O")
        self.assertTrue(result["valid"])
        self.assertEqual(logic.game_mode.board[1][1], "O")

    def test_general_invalid_move(self):
        logic = GameLogic(3, "general")
        logic.place_letter(1, 1, "O")
        result = logic.place_letter(1, 1, "S")
        self.assertFalse(result["valid"])
        self.assertEqual(logic.game_mode.board[1][1], "O")
    
    def test_simple_game_win_cond(self):
        logic = GameLogic(3, "simple")
        logic.game_mode.board = [
            ["S", "O", ""],
            ["", "", ""],
            ["", "", ""]
        ]
        logic.current_player = "p1"
        result = logic.place_letter(0, 2, "S")
        self.assertTrue(result["game_over"])
        self.assertEqual(result["winner"], "p1")

    def test_simple_game_tie_cond(self):
        logic = GameLogic(3, "simple")
        logic.game_mode.board = [
            ["S", "S", "O"],
            ["O", "O", "S"],
            ["S", "O", "S"]
        ]
        result = logic.game_mode.gameOver()
        self.assertTrue(result)

    def test_general_game_scoring_extra_turn(self): 
        logic = GameLogic(3, "general")
        logic.current_player = "p1"
        logic.game_mode.board = [
            ["S", "O", ""],
            ["", "", ""],
            ["", "", ""]
        ]
        result = logic.place_letter(0, 2, "S")
        self.assertTrue(result["valid"])
        self.assertEqual(result["sos_found"], 1)
        self.assertEqual(logic.current_player, "p1")

    def test_general_game_win_cond(self):
        logic = GameLogic(3, "general")
        logic.game_mode.board = [
            ["S", "O", "S"],
            ["O", "S", "O"],
            ["O", "S", "O"]
        ]
        logic.game_mode.scores = {"p1": 3, "p2": 2}
        game_over, winner = logic.game_mode.gameOver()
        self.assertTrue(game_over)
        self.assertEqual(winner, 1) 

    def test_general_game_tie_cond(self):
        logic = GameLogic(3, "general")
        logic.game_mode.board = [
            ["S", "O", "S"],
            ["O", "S", "O"],
            ["O", "S", "O"]
        ]
        logic.game_mode.scores = {"p1": 2, "p2": 2}
        game_over, winner = logic.game_mode.gameOver()
        self.assertTrue(game_over)
        self.assertEqual(winner, 1)


if __name__ == "__main__":
    unittest.main()
