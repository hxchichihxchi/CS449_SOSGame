import unittest
from gameLogic import GameLogic, ComputerPlayer, HumanPlayer
from gui import MenuPage, GamePage, SOSApp

class TestBoardSetup(unittest.TestCase):
    """Tests for board size validation and game initialization"""
    
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

class TestGameCreate(unittest.TestCase):
    """Tests for starting games and GUI setup"""
    
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

class TestSimpleGame(unittest.TestCase):
    """Tests for Simple game mode logic"""
    
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

    def test_simple_game_win_cond(self):
        """AC 5.1 Test winning condition in simple mode."""
        logic = GameLogic(3, "simple")
        logic.place_letter(0, 0, "S")
        logic.place_letter(0, 1, "O")
        result = logic.place_letter(0, 2, "S")
        self.assertTrue(result["game_over"])
        self.assertEqual(result["winner"], "p1")

    def test_simple_game_tie_cond(self):
        """AC 5.2 Test tie condition in simple mode (board full)."""
        logic = GameLogic(3, "simple")
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

    def test_simple_highlighting(self):
        """Highlighting in Simple Game"""
        app = SOSApp()
        app.grid_size = 3
        app.mode = "simple"
        app.show_frame("GamePage")
        frame = app.frames["GamePage"]

        logic = frame.logic
        logic.place_letter(0, 0, "S")
        logic.place_letter(0, 1, "O")
        frame.create_board()
        frame.handle_click(0, 2)
        
        for c in range(3):
            self.assertNotEqual(frame.labels[0][c]["bg"], "white")

class TestGeneralGame(unittest.TestCase):
    """Tests for General game mode logic"""
    
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

    def test_general_game_scoring_extra_turn(self): 
        """AC 6.3 Test that a player gets an extra turn after forming SOS in general mode."""
        logic = GameLogic(3, "general")
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
        logic.place_letter(1, 0, "S")
        logic.place_letter(1, 1, "O")
        frame.create_board()
        frame.left_choice.set("S")
        frame.handle_click(1, 2)

        color = "cyan"
        for c in range(3):
            self.assertEqual(frame.labels[1][c]["bg"], color)

    def test_general_game_win_cond(self):
        """AC 7.2 Test winning condition in general mode based on scores."""
        logic = GameLogic(3, "general")
        moves = [
            (0, 0, "S"), (0, 1, "O"), (0, 2, "S"),
            (1, 0, "O"), (1, 1, "S"), (1, 2, "O"),
            (2, 0, "O"), (2, 1, "S"), (2, 2, "O")
        ]
        for r, c, letter in moves:
            logic.place_letter(r, c, letter)
        
        self.assertTrue(logic.game_mode.game_over())
        
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

class TestCPUPlayer(unittest.TestCase):
    """Tests for CPU player creation and initialization (User Story 8)"""
    
    def test_p1_cpu(self):
        """AC 8.1: Test creating a game with P1 as CPU"""
        logic = GameLogic(3, "simple", p1_type="computer", p2_type="human")
        self.assertIsInstance(logic.p1, ComputerPlayer)
        self.assertIsInstance(logic.p2, HumanPlayer)

    def test_p2_cpu(self):
        """AC 8.1: Test creating a game with P2 as CPU"""
        logic = GameLogic(3, "simple", p1_type="human", p2_type="computer")
        self.assertIsInstance(logic.p1, HumanPlayer)
        self.assertIsInstance(logic.p2, ComputerPlayer)

    def test_both_cpu(self):
        """AC 8.2: Test creating a game with both players as CPU"""
        logic = GameLogic(3, "general", p1_type="computer", p2_type="computer")
        self.assertIsInstance(logic.p1, ComputerPlayer)
        self.assertIsInstance(logic.p2, ComputerPlayer)

class TestCPUMove(unittest.TestCase):
    """Tests for CPU move generation and validation (User Story 9)"""
    
    def test_cpu_auto_move(self):
        """AC 9.1: Test that CPU automatically makes a move when it's their turn"""
        logic = GameLogic(3, "simple", p1_type="computer", p2_type="human")
        move = logic.get_cpu_move()
        self.assertIsNotNone(move)
        self.assertEqual(len(move), 3)
        row, col, letter = move
        self.assertIn(letter, ["S", "O"])
        self.assertTrue(0 <= row < 3)
        self.assertTrue(0 <= col < 3)

    def test_valid_cpu_move(self):
        """AC 9.2: Test that CPU only places moves in empty cells"""
        logic = GameLogic(3, "simple", p1_type="computer", p2_type="human")
        logic.place_letter(0, 0, "S")
        logic.place_letter(0, 1, "O")
        move = logic.get_cpu_move()
        row, col, letter = move
        self.assertEqual(logic.game_mode._board[row][col], "")
        result = logic.place_letter(row, col, letter)
        self.assertTrue(result["valid"])

    def test_invalid_cpu_move(self):
        """AC 9.3: Test that CPU's move generation only considers empty cells"""
        logic = GameLogic(3, "simple", p1_type="computer", p2_type="human")
        for r in range(3):
            for c in range(3):
                if not (r == 2 and c == 2):
                    logic.game_mode._board[r][c] = "S"
        move = logic.get_cpu_move()
        row, col, letter = move
        self.assertEqual((row, col), (2, 2))

    def test_complete_cpu_game(self):
        """AC 9.4: Test that CPU vs CPU game plays automatically to completion"""
        logic = GameLogic(3, "simple", p1_type="computer", p2_type="computer")
        max_moves = 9
        moves_made = 0
        while not logic.game_mode.game_over() and moves_made < max_moves:
            move = logic.get_cpu_move()
            self.assertIsNotNone(move)
            row, col, letter = move
            result = logic.place_letter(row, col, letter)
            if not result["sos_found"]:
                logic.switch_turn()
            moves_made += 1
        self.assertTrue(logic.game_mode.game_over() or moves_made == max_moves)

class TestCPULogic(unittest.TestCase):
    """Tests for CPU intelligence and strategy (User Story 10)"""

    """AC 10.1: Test that CPU completes SOS in all four directions"""
    def test_cpu_sos_recog_horizontal(self):
        logic = GameLogic(3, "simple", p1_type="computer", p2_type="human")
        logic.game_mode._board[0][0] = "S"
        logic.game_mode._board[0][1] = "O"
        move = logic.get_cpu_move()
        self.assertEqual(move, (0, 2, "S"))
        
    def test_cpu_sos_recog_vertical(self):
        logic = GameLogic(3, "simple", p1_type="computer", p2_type="human")
        logic.game_mode._board[0][0] = "S"
        logic.game_mode._board[1][0] = "O"
        move = logic.get_cpu_move()
        self.assertEqual(move, (2, 0, "S"))
        
    def test_cpu_sos_recog_tlbr(self):
        logic = GameLogic(3, "simple", p1_type="computer", p2_type="human")
        logic.game_mode._board[0][0] = "S"
        logic.game_mode._board[1][1] = "O"
        move = logic.get_cpu_move()
        self.assertEqual(move, (2, 2, "S"))
        
    def test_cpu_sos_recog_bltr(self):
        logic = GameLogic(3, "simple", p1_type="computer", p2_type="human")
        logic.game_mode._board[2][0] = "S"
        logic.game_mode._board[1][1] = "O"
        move = logic.get_cpu_move()
        self.assertEqual(move, (0, 2, "S"))

    def test_cpu_recognizes_middle_of_sos(self):    # Middle Placement
        logic = GameLogic(3, "simple", p1_type="computer", p2_type="human")
        logic.game_mode._board[0][0] = "S"
        logic.game_mode._board[0][2] = "S"
        move = logic.get_cpu_move()
        row, col, letter = move
        self.assertEqual((row, col, letter), (0, 1, "O"))

    def test_cpu_random_move(self):
        """AC 10.2: Test that CPU makes random move when no SOS can be completed"""
        logic = GameLogic(3, "simple", p1_type="computer", p2_type="human")
        move = logic.get_cpu_move()
        self.assertIsNotNone(move)
        row, col, letter = move
        self.assertTrue(0 <= row < 3)
        self.assertTrue(0 <= col < 3)
        self.assertIn(letter, ["S", "O"])
        self.assertEqual(logic.game_mode._board[row][col], "")

if __name__ == "__main__":
    unittest.main()