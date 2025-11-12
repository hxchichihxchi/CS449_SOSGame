class GameLogic:
    """ Defines mode and method calls """
    def __init__(self, size, mode="simple"):
        if not isinstance(size, int) or size < 3 or size > 15:
            raise ValueError("Board size must be between 3 and 15")
        self.mode = mode

        if mode == 'simple':
            self.game_mode = SimpleGame(size)
        elif mode == 'general':
            self.game_mode = GeneralGame(size)
        else:
            raise ValueError("Invalid Mode")

    def place_letter(self, row, col, letter):
        return self.game_mode.place_letter(row, col, letter)

    def switch_turn(self):
        self.game_mode.switch_turn()

    def get_current_player(self):
        return self.game_mode.get_current_player()

    def gameOver(self):
        return self.game_mode.gameOver()
    
    def get_scores(self):
        """Get scores for general game mode."""
        if hasattr(self.game_mode, 'get_scores'):
            return self.game_mode.get_scores()
        return {"p1": 0, "p2": 0}
    
class BaseGame:
    """ Delegated to shared attributes and methods """
    def __init__(self, size):
        self._size = size
        self._board = [["" for _ in range(size)] for _ in range(size)]
        self._current_player = "p1"
        self._found = set()
    
    def get_board(self):
        return self._board

    def get_size(self):
        return self._size

    def switch_turn(self):
        self._current_player = "p2" if self._current_player == "p1" else "p1"

    def get_current_player(self):
        return self._current_player
    
    def _sosCheck(self):
        sos_list = []
        # Horizontal
        for r in range(self._size):
            for c in range(self._size - 2):
                if self._board[r][c:c+3] == ["S", "O", "S"]:
                    sos_id = ('H', r, c)
                    if sos_id not in self._found:
                        self._found.add(sos_id)
                        sos_list.append([(r,c),(r,c+1),(r,c+2)])

        # Vertical
        for c in range(self._size):
            for r in range(self._size - 2):
                if [self._board[r+i][c] for i in range(3)] == ["S", "O", "S"]:
                    sos_id = ('V', r, c)
                    if sos_id not in self._found:
                        self._found.add(sos_id)
                        sos_list.append([(r,c),(r+1,c),(r+2,c)])

        # Diagonal TL-BR
        for r in range(self._size - 2):
            for c in range(self._size - 2):
                if [self._board[r+i][c+i] for i in range(3)] == ["S", "O", "S"]:
                    sos_id = ('D1', r, c)
                    if sos_id not in self._found:
                        self._found.add(sos_id)
                        sos_list.append([(r,c),(r+1,c+1),(r+2,c+2)])

        # Diagonal BL-TR
        for r in range(self._size - 2):
            for c in range(2, self._size):
                if [self._board[r+i][c-i] for i in range(3)] == ["S", "O", "S"]:
                    sos_id = ('D2', r, c)
                    if sos_id not in self._found:
                        self._found.add(sos_id)
                        sos_list.append([(r,c),(r+1,c-1),(r+2,c-2)])

        return sos_list
    
    def is_valid_move(self, row, col):
        """Return True if the cell at (row, col) is empty."""
        return self._board[row][col] == ""
    
    def update_board(self, row, col, letter):
        """Place the letter on the board."""
        self._board[row][col] = letter

""" SimpleGame and GeneralGame Classes delegated to define rulesets """

class SimpleGame(BaseGame):
    def __init__(self, size):
        super().__init__(size)  # Referenes BaseGame/shared parameters

    def place_letter(self, row, col, letter):
        if self.is_valid_move(row, col):
            self.update_board(row, col, letter)
            sos_list = self.sosCheck()
            board_full = all(cell != "" for row in self._board for cell in row)

            winner = None
            if sos_list:
                winner = self.get_current_player()
            elif board_full:
                winner = "draw"

            if winner is None:
                self.switch_turn()

            return {
                "valid": True,
                "sos_found": len(sos_list),
                "game_over": board_full or winner is not None,
                "winner": winner,
                "sos_list": sos_list
            }
        return {"valid": False, "sos_found": 0, "game_over": False, "winner": None, "sos_list": []}

    def sosCheck(self):
        return self._sosCheck()

    def gameOver(self):
        # SOS Found; True, game ends.
        return bool(self._found)

class GeneralGame(BaseGame):
    def __init__(self, size):
        super().__init__(size)  # Referenes BaseGame/shared parameters

        self._p1_score = 0
        self._p2_score = 0
    
    def get_scores(self):
        return {"p1": self._p1_score, "p2": self._p2_score}

    def place_letter(self, row, col, letter):
        if self._board[row][col] != "":
            return {"valid": False, "sos_found": 0, "game_over": False, "winner": None, "sos_list": []}

        self._board[row][col] = letter
        sos_list = self.sosCheck()

        if self.get_current_player() == "p1":
            self._p1_score += len(sos_list)
        else:
            self._p2_score += len(sos_list)

        board_full = all(cell != "" for row in self._board for cell in row)
        
        # Determine winner if game is over
        winner = None
        if board_full:
            winner = self.get_winner()

        if not sos_list:
            self.switch_turn()

        return {"valid": True, "sos_found": len(sos_list), "game_over": board_full, "winner": winner, "sos_list": sos_list}

    def sosCheck(self):
        return self._sosCheck()

    def get_winner(self):
        """Returns 'p1', 'p2', or 'draw' based on scores."""
        if self._p1_score > self._p2_score:
            return "p1"
        elif self._p2_score > self._p1_score:
            return "p2"
        else:
            return "draw"

    def gameOver(self):
        # False: nothing, True: Game Ends
        return all(cell != "" for row in self._board for cell in row)

# Debugging for refactor
if __name__ == "__main__":
    # Simple Mode Test
    print("=== Simple Mode Test ===")
    game = GameLogic(5, mode="simple")  # 5x5 board

    print("Initial player:", game.get_current_player())
    print("Placing S at (0,0):", game.place_letter(0, 0, "S"))
    print("Placing O at (0,1):", game.place_letter(0, 1, "O"))
    print("Placing S at (0,2):", game.place_letter(0, 2, "S"))

    print("Current player:", game.get_current_player())
    print("Is game over?", game.gameOver())

    # General Mode Test
    print("\n=== General Mode Test ===")
    game = GameLogic(5, mode="general")  # 5x5 board

    print("Initial player:", game.get_current_player())
    print("Placing S at (0,0):", game.place_letter(0, 0, "S"))
    print("Placing O at (0,1):", game.place_letter(0, 1, "O"))
    print("Placing S at (0,2):", game.place_letter(0, 2, "S"))

    print("Current player:", game.get_current_player())
    print("Is game over?", game.gameOver())
    print("Scores -> P1:", game.game_mode._p1_score, "P2:", game.game_mode._p2_score)
