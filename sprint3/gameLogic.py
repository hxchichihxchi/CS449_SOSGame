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
    
    def sosCheck(self):
        # Return True when first SOS is formed
        # Horizontal Check
        for r in range(self.size):          # for each row
            for c in range(self.size - 2):  # stop 2 before the end
                if self.board[r][c] == "S" and \
                self.board[r][c+1] == "O" and \
                self.board[r][c+2] == "S":
                    print('Horizontal SOS Found')
                    return True
        # Vertical Check
        for c in range(self.size):          # for each column
            for r in range(self.size - 2): # stop 2 before the end
                if self.board[r][c] == "S" and \
                self.board[r+1][c] == "O" and \
                self.board[r+2][c] == "S":
                    print('Vertical SOS Found')
                    return True
        # Diagonal Check (\ - Top Left to Bottom Right)
        for r in range(self.size - 2):          # for each row
            for c in range(self.size - 2):  # stop 2 before the end
                if self.board[r][c] == "S" and \
                self.board[r+1][c+1] == "O" and \
                self.board[r+2][c+2] == "S":
                    print("Diagonal TL-BR SOS Found")
                    return True
        # Diagonal Check (/ - Bottom Left to Top Right)
        for r in range(self.size - 2):          # for each row
            for c in range(2, self.size):  # stop 2 before the end
                if self.board[r][c] == "S" and \
                self.board[r+1][c-1] == "O" and \
                self.board[r+2][c-2] == "S":
                    print("Diagonal BL-TR SOS Found")
                    return True
                
    def gameOver(self):
        return self.sosCheck()

class GeneralGame():
    def __init__(self, size):
        # Added for sizing tests
        self.size = size
        self.current_player = "p1"
        self.board = [["" for _ in range(size)] for _ in range(size)]
        self.found = set()  # Records old SOS sequences
        self.p1_score = 0
        self.p2_score = 0

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
    
    def sosCheck(self):
        # Return True when first SOS is formed
        # Horizontal Check
        count = 0
        for r in range(self.size):          # for each row
            for c in range(self.size - 2):  # stop 2 before the end
                if self.board[r][c] == "S" and \
                self.board[r][c+1] == "O" and \
                self.board[r][c+2] == "S":
                    sos_id = ('H',r, c)     # Sequence Attributes
                    if sos_id not in self.found:
                        print('Horizontal SOS Found')
                        self.found.add(sos_id)
                        count += 1

        # Vertical Check
        for c in range(self.size):          # for each column
            for r in range(self.size - 2): # stop 2 before the end
                if self.board[r][c] == "S" and \
                self.board[r+1][c] == "O" and \
                self.board[r+2][c] == "S":
                    sos_id = ('V',r, c)     # Sequence Attributes
                    if sos_id not in self.found:
                        print('Vertical SOS Found')
                        self.found.add(sos_id)
                        count += 1

        # Diagonal Check (\ - Top Left to Bottom Right)
        for r in range(self.size - 2):          # for each row
            for c in range(self.size - 2):  # stop 2 before the end
                if self.board[r][c] == "S" and \
                self.board[r+1][c+1] == "O" and \
                self.board[r+2][c+2] == "S":
                    sos_id = ('D1',r, c)     # Sequence Attributes
                    if sos_id not in self.found:
                        print("Diagonal TL-BR SOS Found")
                        self.found.add(sos_id)
                        count += 1

        # Diagonal Check (/ - Bottom Left to Top Right)
        for r in range(self.size - 2):          # for each row
            for c in range(2, self.size):  # stop 2 before the end
                if self.board[r][c] == "S" and \
                self.board[r+1][c-1] == "O" and \
                self.board[r+2][c-2] == "S":
                    sos_id = ('D2',r, c)     # Sequence Attributes
                    if sos_id not in self.found:
                        print("Diagonal BL-TR SOS Found")
                        self.found.add(sos_id)
                        count += 1
        if count > 0:
            if self.current_player == "p1":
                self.p1_score += count
            else:
                self.p2_score += count
        return count
    
    def gameOver(self):
        sos_count = self.sosCheck()
        board_full = all(cell != "" for row in self.board for cell in row)
        return board_full, sos_count

# # Testing SOS Found w/o GUI
# if __name__ == "__main__":
#     g = SimpleGame(3)
#     g.place_letter(0,0,'S')
#     g.place_letter(0,1,'O')
#     g.place_letter(0,2,'S')
#     print("Checking gameOver...")
#     g.gameOver()
