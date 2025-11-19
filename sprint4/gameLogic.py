import random

# Constants
PLAYER_1 = "p1"
PLAYER_2 = "p2"
LETTER_S = "S"
LETTER_O = "O"
VALID_LETTERS = ["S", "O"]
MIN_BOARD_SIZE = 3
MAX_BOARD_SIZE = 15

# --- Player Class Hierarchy ---
class Player:
    """ Base class for player types """
    def make_move(self):
        raise NotImplementedError

class HumanPlayer(Player):
    """ Human player - moves handled by GUI """
    def make_move(self):
        return None

class ComputerPlayer(Player):
    def make_move(self, board, size, found, sos_checker):
        sos_move = self._find_sos_completing_move(board, size, found, sos_checker)
        if sos_move:
            return sos_move
        return self._play_random_move(board, size)
    
    def _find_sos_completing_move(self, board, size, found, sos_checker):
        """
        Searches for a move that will complete an SOS sequence.
        For every empty cell, tries placing 'S' and 'O' to see if it creates SOS.
        """
        for r in range(size):
            for c in range(size):
                if board[r][c] == "":
                    for letter in VALID_LETTERS:
                        board[r][c] = letter
                        if self._check_creates_new_sos(board, size, found, sos_checker):
                            board[r][c] = ""
                            print(f"SOS Candidate found: {letter} at {r},{c}")
                            return (r, c, letter)
                        board[r][c] = ""
        return None
    
    def _check_creates_new_sos(self, board, size, found, sos_checker):
        """ CPU check using shared pure scanner (prevnets duplication) """
        all_sos = sos_checker(board, size)
        for sos_id in all_sos:
            if sos_id not in found:
                return True
        return False
    
    def _play_random_move(self, board, size):
        """ Plays random letter in random empty cell if no SOS sequence can be formed """
        empty_cells = [(r, c) for r in range(size) for c in range(size) if board[r][c] == ""]
        
        if empty_cells:
            r, c = random.choice(empty_cells)
            letter = random.choice(VALID_LETTERS)
            print(f"No SOS found, randomly placing {letter} at {r},{c}")
            return (r, c, letter)
        return None

# --- Main Game Logic Controller ---
class GameLogic:
    """ Defines mode and method calls """
    def __init__(self, size, mode="simple", p1_type="human", p2_type="human"):
        if not isinstance(size, int) or size < MIN_BOARD_SIZE or size > MAX_BOARD_SIZE:
            raise ValueError(f"Board size must be between {MIN_BOARD_SIZE} and {MAX_BOARD_SIZE}")
        
        self.mode = mode
        self.p1 = HumanPlayer() if p1_type == "human" else ComputerPlayer()
        self.p2 = HumanPlayer() if p2_type == "human" else ComputerPlayer()
        if mode == 'simple':
            self.game_mode = SimpleGame(size)
        elif mode == 'general':
            self.game_mode = GeneralGame(size)
        else:
            raise ValueError(f"Invalid mode: {mode}")

    def place_letter(self, row, col, letter):
        return self.game_mode.place_letter(row, col, letter)
    
    def get_cpu_move(self):
        current_player_name = self.get_current_player()
        current_player_obj = self.p1 if current_player_name == PLAYER_1 else self.p2
        
        if isinstance(current_player_obj, ComputerPlayer):
            return current_player_obj.make_move(
                self.game_mode.get_board(),
                self.game_mode.get_size(),
                self.game_mode.get_found(),
                BaseGame._scan_sos_static
            )
        return None

    def switch_turn(self):
        self.game_mode.switch_turn()

    def get_current_player(self):
        return self.game_mode.get_current_player()

    def game_over(self):
        return self.game_mode.game_over()
    
    def get_scores(self):
        return self.game_mode.get_scores()

# --- Base Game Class ---
class BaseGame:
    """ Delegated to shared attributes and methods """
    def __init__(self, size):
        self._size = size
        self._board = [["" for _ in range(size)] for _ in range(size)]
        self._current_player = PLAYER_1
        self._found = set()
    
    def get_board(self):
        return self._board

    def get_size(self):
        return self._size

    def switch_turn(self):
        print("Switching Turn")
        self._current_player = PLAYER_2 if self._current_player == PLAYER_1 else PLAYER_1

    def get_current_player(self):
        return self._current_player
    
    def get_scores(self):
        return {PLAYER_1: 0, PLAYER_2: 0}
    
    def get_found(self):
        """Returns copy of found SOS sequences."""
        return self._found.copy()

    @staticmethod
    def _scan_sos_static(board, size):
        """ Simulates and scans for candidate SOS sequences """
        found_local = []
        for r in range(size):
            for c in range(size - 2):
                if board[r][c:c+3] == [LETTER_S, LETTER_O, LETTER_S]:
                    found_local.append(('H', r, c))
        for c in range(size):
            for r in range(size - 2):
                if [board[r+i][c] for i in range(3)] == [LETTER_S, LETTER_O, LETTER_S]:
                    found_local.append(('V', r, c))
        for r in range(size - 2):
            for c in range(size - 2):
                if [board[r+i][c+i] for i in range(3)] == [LETTER_S, LETTER_O, LETTER_S]:
                    found_local.append(('D1', r, c))
        for r in range(size - 2):
            for c in range(2, size):
                if [board[r+i][c-i] for i in range(3)] == [LETTER_S, LETTER_O, LETTER_S]:
                    found_local.append(('D2', r, c))
        return found_local

    def _sos_check(self):
        """ Finds new SOS sequences, updates _found, and returns their coordinates. """
        new_sos = []
        all_sos = BaseGame._scan_sos_static(self._board, self._size)

        for sos_id in all_sos:
            if sos_id not in self._found:
                self._found.add(sos_id)
                direction, r, c = sos_id

                if direction == 'H':
                    new_sos.append([(r, c), (r, c+1), (r, c+2)])
                elif direction == 'V':
                    new_sos.append([(r, c), (r+1, c), (r+2, c)])
                elif direction == 'D1':
                    new_sos.append([(r, c), (r+1, c+1), (r+2, c+2)])
                else:
                    new_sos.append([(r, c), (r+1, c-1), (r+2, c-2)])

        return new_sos

    def is_valid_move(self, row, col):
        if not (0 <= row < self._size and 0 <= col < self._size):
            raise ValueError(f"Position ({row}, {col}) out of bounds")
        return self._board[row][col] == ""
    
    def update_board(self, row, col, letter):
        if letter not in VALID_LETTERS:
            raise ValueError(f"Invalid letter: {letter}. Must be 'S' or 'O'")
        self._board[row][col] = letter
    
    def is_board_full(self):
        return all(cell != "" for row in self._board for cell in row)

# --- Simple Game ---
class SimpleGame(BaseGame):
    def __init__(self, size):
        super().__init__(size)

    def place_letter(self, row, col, letter):
        try:
            if self.is_valid_move(row, col):
                self.update_board(row, col, letter)
                sos_list = self._sos_check()
                board_full = self.is_board_full()

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
        except ValueError:
            pass
        
        return {"valid": False, "sos_found": 0, "game_over": False, "winner": None, "sos_list": []}

    def game_over(self):
        return bool(self._found)

# --- General Game ---
class GeneralGame(BaseGame):
    def __init__(self, size):
        super().__init__(size)
        self._p1_score = 0
        self._p2_score = 0
    
    def get_scores(self):
        return {PLAYER_1: self._p1_score, PLAYER_2: self._p2_score}

    def place_letter(self, row, col, letter):
        try:
            if not self.is_valid_move(row, col):
                return {"valid": False, "sos_found": 0, "game_over": False, "winner": None, "sos_list": []}

            self.update_board(row, col, letter)
            sos_list = self._sos_check()

            if self.get_current_player() == PLAYER_1:
                self._p1_score += len(sos_list)
            else:
                self._p2_score += len(sos_list)

            board_full = self.is_board_full()

            winner = None
            if board_full:
                winner = self.get_winner()

            if not sos_list:
                self.switch_turn()

            return {"valid": True, "sos_found": len(sos_list), "game_over": board_full, "winner": winner, "sos_list": sos_list}
        except ValueError:
            return {"valid": False, "sos_found": 0, "game_over": False, "winner": None, "sos_list": []}

    def get_winner(self):
        if self._p1_score > self._p2_score:
            return PLAYER_1
        elif self._p2_score > self._p1_score:
            return PLAYER_2
        else:
            return "draw"

    def game_over(self):
        return self.is_board_full()