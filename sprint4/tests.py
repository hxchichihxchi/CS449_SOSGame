import unittest
from gameLogic import GameLogic
from gui import MenuPage, GamePage, SOSApp

class TestSOSGame(unittest.TestCase):

    def test_valid_board_sizes_range(self):
        """AC 1.1 Test multiple valid board sizes."""
        valid_sizes = [3, 5, 8, 10]
        for size in valid_sizes:
            with self.subTest(size=size):
                game = GameLogic(size, "simple")
                board = game.game_mode._board
                self.assertEqual(len(board), size)
                self.assertTrue(all(len(row) == size for row in board))

    def test_invalid_board_size_raises_error(self):
        """AC 1.2 Bad inputs should raise errors."""
        bad_sizes = [0, -1, 1, "five", 16, None]
        for size in bad_sizes:
            with self.subTest(size=size):
                with self.assertRaises((ValueError, TypeError)):
                    GameLogic(size, "simple")

    def test_start_simple_game(self):
        """AC 3.1 Test that the simple game GUI loads correctly."""
        app = SOSApp()
        app.grid_size = 3
        app.mode = "simple"
        app.show_frame("GamePage")
        frame = app.frames["GamePage"]
        self.assertEqual(frame.mode_label['text'], "Simple Game")
        self.assertEqual(len(frame.board_frame.winfo_children()), 3 * 3)

    def test_start_general_game(self):
        """AC 3.2 Test that the general game GUI loads correctly."""
        app = SOSApp()
        app.grid_size = 3
        app.mode = "general"
        app.show_frame("GamePage")
        frame = app.frames["GamePage"]
        self.assertEqual(frame.mode_label['text'], "General Game")
        self.assertEqual(len(frame.board_frame.winfo_children()), 3 * 3)

    def test_start_no_mode_selected(self):
        """AC 3.3 Test that starting a game without selecting a mode shows alert."""
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
        """AC 4.1 Test a valid move in simple mode."""
        logic = GameLogic(3, "simple")
        result = logic.place_letter(0, 0, "S")
        self.assertTrue(result["valid"])
        self.assertEqual(logic.game_mode._board[0][0], "S")

    def test_simple_invalid_move(self):
        """AC 4.2 Test that placing a letter in an occupied cell is invalid."""
        logic = GameLogic(3, "simple")
        logic.place_letter(0, 0, "S")
        result = logic.place_letter(0, 0, "O")
        self.assertFalse(result["valid"])
        self.assertEqual(logic.game_mode._board[0][0], "S")

    def test_general_valid_move(self):
        """AC 6.1 Test a valid move in general mode."""
        logic = GameLogic(3, "general")
        result = logic.place_letter(1, 1, "O")
        self.assertTrue(result["valid"])
        self.assertEqual(logic.game_mode._board[1][1], "O")

    def test_general_invalid_move(self):
        """AC 6.2 Test invalid move in general mode (occupied cell)."""
        logic = GameLogic(3, "general")
        logic.place_letter(1, 1, "O")
        result = logic.place_letter(1, 1, "S")
        self.assertFalse(result["valid"])
        self.assertEqual(logic.game_mode._board[1][1], "O")
    
    def test_simple_game_win_cond(self):
        """AC 5.1 Test winning condition in simple mode."""
        logic = GameLogic(3, "simple")
        # Place moves that will create SOS
        logic.place_letter(0, 0, "S")
        logic.place_letter(0, 1, "O")
        result = logic.place_letter(0, 2, "S")
        self.assertTrue(result["game_over"])
        self.assertEqual(result["winner"], "p1")

    def test_simple_game_tie_cond(self):
        """AC 5.2 Test tie condition in simple mode (board full)."""
        logic = GameLogic(3, "simple")
        # Fill board without making SOS
        moves = [
            (0, 0, "O"), (0, 1, "O"), (0, 2, "O"),
            (1, 0, "O"), (1, 1, "O"), (1, 2, "S"),
            (2, 0, "S"), (2, 1, "S")
        ]
        for r, c, letter in moves:
            logic.place_letter(r, c, letter)
        
        result = logic.place_letter(2, 2, "O")
        self.assertTrue(result["game_over"])
        self.assertEqual(result["winner"], "draw")

    def test_general_game_scoring_extra_turn(self): 
        """AC 6.3 Test that a player gets an extra turn after forming SOS in general mode."""
        logic = GameLogic(3, "general")
        # Place moves that will create SOS
        logic.place_letter(0, 0, "S")
        logic.place_letter(0, 1, "O")
        result = logic.place_letter(0, 2, "S")
        self.assertTrue(result["valid"])
        self.assertEqual(result["sos_found"], 1)
        self.assertEqual(logic.get_current_player(), "p1")
    
    def test_general_highlighting(self):
        """AC 7.1: Test that forming SOS highlights cells in general mode"""
        app = SOSApp()
        app.grid_size = 3
        app.mode = "general"
        app.show_frame("GamePage")
        frame = app.frames["GamePage"]

        logic = frame.logic
        # Place moves using the logic properly
        logic.place_letter(1, 0, "S")
        logic.place_letter(1, 1, "O")
        frame.create_board()

        frame.left_choice.set("S")
        frame.handle_click(1, 2)

        # Check that the cells forming SOS are highlighted in the correct color
        color = "cyan"
        for c in range(3):
            self.assertEqual(frame.labels[1][c]["bg"], color)

    def test_general_game_win_cond(self):
        """AC 7.2 Test winning condition in general mode based on scores."""
        logic = GameLogic(3, "general")
        # Fill board completely
        moves = [
            (0, 0, "S"), (0, 1, "O"), (0, 2, "S"),
            (1, 0, "O"), (1, 1, "S"), (1, 2, "O"),
            (2, 0, "O"), (2, 1, "S"), (2, 2, "O")
        ]
        for r, c, letter in moves:
            logic.place_letter(r, c, letter)
        
        # Check game is over
        self.assertTrue(logic.game_mode.game_over())
        
        # Get winner based on scores
        scores = logic.get_scores()
        winner = logic.game_mode.get_winner()
        if scores["p1"] > scores["p2"]:
            self.assertEqual(winner, "p1")
        elif scores["p2"] > scores["p1"]:
            self.assertEqual(winner, "p2")
        else:
            self.assertEqual(winner, "draw")

    def test_general_game_tie_cond(self):
        """AC 7.3 Test tie condition in general mode (scores equal)."""
        logic = GameLogic(3, "general")
        # Fill board without creating any SOS sequences
        moves = [
            (0, 0, "O"), (0, 1, "O"), (0, 2, "O"),
            (1, 0, "O"), (1, 1, "O"), (1, 2, "O"),
            (2, 0, "O"), (2, 1, "O"), (2, 2, "O")
        ]
        for r, c, letter in moves:
            logic.place_letter(r, c, letter)
        
        self.assertTrue(logic.game_mode.game_over())
        result = logic.game_mode.get_winner()
        self.assertEqual(result, "draw")
    
    def test_simple_highlighting(self):
        """Highlighting in Simple Game"""
        app = SOSApp()
        app.grid_size = 3
        app.mode = "simple"
        app.show_frame("GamePage")
        frame = app.frames["GamePage"]

        logic = frame.logic
        # Place moves properly through logic
        logic.place_letter(0, 0, "S")
        logic.place_letter(0, 1, "O")
        frame.create_board()

        frame.handle_click(0, 2)
        
        # Check that the cells forming SOS are highlighted
        for c in range(3):
            self.assertNotEqual(frame.labels[0][c]["bg"], "white")

if __name__ == "__main__":
    unittest.main()