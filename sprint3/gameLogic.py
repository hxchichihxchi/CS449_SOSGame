class GameLogic:
    def __init__(self, size, mode="simple"):
        if not isinstance(size, int) or size < 3 or size > 15:
            raise ValueError("Board size must be between 3 and 15")
        self.size = size
        self.mode = mode
        self.board = [["" for _ in range(size)] for _ in range(size)]

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

class SimpleGame():
    def __init__(self, size):
        self.size = size
        self.current_player = "p1"
        self.board = [["" for _ in range(size)] for _ in range(size)]
        self.found = set()

    def place_letter(self, row, col, letter):
        if self.board[row][col] == "":
            self.board[row][col] = letter
            sos_list = self.sosCheck()
            board_full = all(cell != "" for row in self.board for cell in row)

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

    def switch_turn(self):
        self.current_player = "p2" if self.current_player == "p1" else "p1"

    def get_current_player(self):
        return self.current_player

    def sosCheck(self):
        sos_list = []

        # Horizontal
        for r in range(self.size):
            for c in range(self.size - 2):
                if self.board[r][c:c+3] == ["S", "O", "S"]:
                    sos_id = ('H', r, c)
                    if sos_id not in self.found:
                        self.found.add(sos_id)
                        sos_list.append([(r,c),(r,c+1),(r,c+2)])

        # Vertical
        for c in range(self.size):
            for r in range(self.size - 2):
                if [self.board[r+i][c] for i in range(3)] == ["S", "O", "S"]:
                    sos_id = ('V', r, c)
                    if sos_id not in self.found:
                        self.found.add(sos_id)
                        sos_list.append([(r,c),(r+1,c),(r+2,c)])

        # Diagonal TL-BR
        for r in range(self.size - 2):
            for c in range(self.size - 2):
                if [self.board[r+i][c+i] for i in range(3)] == ["S", "O", "S"]:
                    sos_id = ('D1', r, c)
                    if sos_id not in self.found:
                        self.found.add(sos_id)
                        sos_list.append([(r,c),(r+1,c+1),(r+2,c+2)])

        # Diagonal BL-TR
        for r in range(self.size - 2):
            for c in range(2, self.size):
                if [self.board[r+i][c-i] for i in range(3)] == ["S", "O", "S"]:
                    sos_id = ('D2', r, c)
                    if sos_id not in self.found:
                        self.found.add(sos_id)
                        sos_list.append([(r,c),(r+1,c-1),(r+2,c-2)])

        return sos_list

    def gameOver(self):
        return bool(self.sosCheck())

class GeneralGame():
    def __init__(self, size):
        self.size = size
        self.current_player = "p1"
        self.board = [["" for _ in range(size)] for _ in range(size)]
        self.found = set()
        self.p1_score = 0
        self.p2_score = 0

    def place_letter(self, row, col, letter):
        if self.board[row][col] != "":
            return {"valid": False, "sos_found": 0, "game_over": False, "winner": None, "sos_list": []}

        self.board[row][col] = letter
        sos_list = self.sosCheck()

        if self.get_current_player() == "p1":
            self.p1_score += len(sos_list)
        else:
            self.p2_score += len(sos_list)

        board_full = all(cell != "" for row in self.board for cell in row)
        
        # Determine winner if game is over
        winner = None
        if board_full:
            winner = self.get_winner()

        if not sos_list:
            self.switch_turn()

        return {"valid": True, "sos_found": len(sos_list), "game_over": board_full, "winner": winner, "sos_list": sos_list}
    
    def switch_turn(self):
        self.current_player = "p2" if self.current_player == "p1" else "p1"

    def get_current_player(self):
        return self.current_player

    def sosCheck(self):
        new_sequences = []
        # Horizontal
        for r in range(self.size):
            for c in range(self.size - 2):
                if self.board[r][c] == "S" and self.board[r][c+1] == "O" and self.board[r][c+2] == "S":
                    sos_id = ('H', r, c)
                    if sos_id not in self.found:
                        self.found.add(sos_id)
                        new_sequences.append([(r,c),(r,c+1),(r,c+2)])
        # Vertical
        for c in range(self.size):
            for r in range(self.size - 2):
                if self.board[r][c] == "S" and self.board[r+1][c] == "O" and self.board[r+2][c] == "S":
                    sos_id = ('V', r, c)
                    if sos_id not in self.found:
                        self.found.add(sos_id)
                        new_sequences.append([(r,c),(r+1,c),(r+2,c)])
        # Diagonal TL-BR
        for r in range(self.size-2):
            for c in range(self.size-2):
                if self.board[r][c] == "S" and self.board[r+1][c+1] == "O" and self.board[r+2][c+2] == "S":
                    sos_id = ('D1', r, c)
                    if sos_id not in self.found:
                        self.found.add(sos_id)
                        new_sequences.append([(r,c),(r+1,c+1),(r+2,c+2)])
        # Diagonal BL-TR
        for r in range(self.size-2):
            for c in range(2, self.size):
                if self.board[r][c] == "S" and self.board[r+1][c-1] == "O" and self.board[r+2][c-2] == "S":
                    sos_id = ('D2', r, c)
                    if sos_id not in self.found:
                        self.found.add(sos_id)
                        new_sequences.append([(r,c),(r+1,c-1),(r+2,c-2)])
        return new_sequences

    def get_winner(self):
        """Returns 'p1', 'p2', or 'draw' based on scores."""
        if self.p1_score > self.p2_score:
            return "p1"
        elif self.p2_score > self.p1_score:
            return "p2"
        else:
            return "draw"

    def gameOver(self):
        board_full = all(cell != "" for row in self.board for cell in row)
        return board_full