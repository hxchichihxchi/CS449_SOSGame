class GameLogic:
    def __init__(self, size):
        # Added for sizing tests
        if not isinstance(size, int):
            raise TypeError(f"Size must be an integer, not {type(size).__name__}")
        if size < 3 or size > 15:
            raise ValueError(f"Size must be between 3 and 15, got {size}")
        
        self.size = size
        self.current_player = "p1"
        self.board = [["" for _ in range(size)] for _ in range(size)]

    def place_letter(self, row, col, letter):
        # Places letter on the board if empty.
        if self.board[row][col] == "":
            self.board[row][col] = letter
            return True
        return False

    def switch_turn(self):
        # Player Turn Switching
        if self.current_player == "p1":
            self.current_player = "p2"
        else:
            self.current_player ="p1"

    def get_current_player(self):
        return self.current_player
