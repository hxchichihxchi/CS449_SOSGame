class GameLogic:
    def __init__(self, size, mode):
        # Added for sizing tests
        if mode == 'simple':
            self.game_mode = SimpleGame(size)
        else:
            self.game_mode = GeneralGame(size)

    def place_letter(self, row, col, letter):
        # Places letter on the board if empty.
        return self.game_mode.place_letter(row, col, letter)

    def switch_turn(self):
        # Player Turn Switching
        self.game_mode.switch_turn()

    def get_current_player(self):
        return self.game_mode.get_current_player()
    
    def gameOver(self):
        return self.game_mode.gameOver()

class SimpleGame():
    def __init__(self, size):
        # Added for sizing tests
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
    
    def gameOver(self):
        # Return True when first SOS is formed
        pass

class GeneralGame():
    def __init__(self, size):
        # Added for sizing tests
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
    
    def gameOver(self):
        # Return True when first SOS is formed
        pass