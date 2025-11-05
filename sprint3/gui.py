import tkinter as tk
from gameLogic import GameLogic

class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Outer frame fills the whole parent
        self.pack_propagate(False)

        # Inner frame for widgets
        inner_frame = tk.Frame(self)
        inner_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Widgets
        tk.Label(inner_frame, text="SOS Game", font=("Arial", 24), fg="white").pack(pady=(0, 20))

        self.selected_option = tk.StringVar(value="simple")
        tk.Radiobutton(inner_frame, text="Simple Game", variable=self.selected_option, value="simple", fg="white").pack(pady=5)
        tk.Radiobutton(inner_frame, text="General Game", variable=self.selected_option, value="general", fg="white").pack(pady=5)

        tk.Label(inner_frame, text="Enter Grid Size (e.g., 3, 5, 7):", font=("Arial", 16), fg="white").pack(pady=(20, 5))
        self.entry = tk.Entry(inner_frame, width=10, font=("Arial", 14))
        self.entry.pack(pady=5)

        tk.Button(inner_frame, text="Start Game", command=self.start_game).pack(pady=10)

        # Alerts for invalid user-input parameters
        self.alert_label = tk.Label(inner_frame, text="", font=("Arial", 10), fg="white")
        self.alert_label.pack(pady=(20, 5))

    def start_game(self):
        value = self.entry.get()
        if not value:
            self.alert_label.config(text="Enter a value for board size.")
            return
        try:
            size = int(value)
            if size < 3 or size > 15:
                raise ValueError()
            mode = self.selected_option.get()
            if not mode:
                self.alert_label.config(text="Please select a game mode.")
                return

            self.controller.grid_size = size
            self.controller.mode = mode
            self.controller.show_frame("GamePage")
        except ValueError:
            self.alert_label.config(text="Gameboard dimensions must be size 3-15.")


class GamePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        main_container = tk.Frame(self)
        main_container.pack(expand=True, fill="both")
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=0)
        main_container.grid_columnconfigure(1, weight=1)
        main_container.grid_columnconfigure(2, weight=0)

        # Left panel
        self.left_frame = tk.Frame(main_container, width=200)
        self.left_frame.grid(row=0, column=0, sticky="ns")

        self.left_score_label = tk.Label(self.left_frame, text="0", fg="cyan", font=("Arial", 72))
        self.left_choice = tk.StringVar(value="S")
        self.left_name_label = tk.Label(self.left_frame, text="P1", fg="cyan", font=("Arial", 20)).pack(padx=10)
        tk.Radiobutton(self.left_frame, text="S", variable=self.left_choice, value="S", fg="white", font=("Arial", 20)).pack(pady=5)
        tk.Radiobutton(self.left_frame, text="O", variable=self.left_choice, value="O", fg="white", font=("Arial", 20)).pack(pady=5)

        # Board wrapper
        self.board_wrapper = tk.Frame(main_container)
        self.board_wrapper.grid(row=0, column=1, sticky="nsew")
        self.board_wrapper.grid_rowconfigure(1, weight=1)
        self.board_wrapper.grid_columnconfigure(0, weight=1)

        self.mode_label = tk.Label(self.board_wrapper, text="", fg="white", font=("Arial", 20))
        self.mode_label.grid(row=0, column=0, pady=10)

        self.board_frame = tk.Frame(self.board_wrapper, width=600, height=600)
        self.board_frame.grid(row=1, column=0)
        self.board_frame.grid_propagate(False)

        # Right panel
        self.right_frame = tk.Frame(main_container, width=200)
        self.right_frame.grid(row=0, column=2, sticky="ns")

        self.right_score_label = tk.Label(self.right_frame, text="0", fg="red", font=("Arial", 72))
        self.right_choice = tk.StringVar(value="S")
        tk.Label(self.right_frame, text="P2", fg="red", font=("Arial", 20)).pack(padx=10)
        tk.Radiobutton(self.right_frame, text="S", variable=self.right_choice, value="S", fg="white", font=("Arial", 20)).pack(pady=5)
        tk.Radiobutton(self.right_frame, text="O", variable=self.right_choice, value="O", fg="white", font=("Arial", 20)).pack(pady=5)

        # Bottom Frame
        self.bottom_frame = tk.Frame(main_container, width=200)
        self.bottom_frame.grid(row=1, column=1, sticky="nsew")
        self.turn_label = tk.Label(self.bottom_frame, text="Current Turn: P1", fg="white", font=("Arial", 20))
        self.turn_label.grid(row=0, column=0, sticky="n")
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.new_game_btn = tk.Button(self.bottom_frame, text="New Game", font=("Arial", 16), command=self.new_game)
        self.new_game_btn.grid(row=1, column=0, pady=(10, 0))

        self.btn_pixel = 0
        self.labels = []

    def set_logic(self, logic):
        self.logic = logic

    def update_mode_label(self):
        self.mode_label.config(text=f"{self.controller.mode.capitalize()} Game")

    def update_score_visibility(self):
        if self.controller.mode == "general":
            self.left_score_label.pack(padx=10)
            self.right_score_label.pack(padx=10)
        else:
            self.left_score_label.pack_forget()
            self.right_score_label.pack_forget()

    def create_board(self):
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        size = self.controller.grid_size
        board_pixel = 600
        self.btn_pixel = board_pixel // size

        self.labels = [[None for _ in range(size)] for _ in range(size)]

        for r in range(size):
            for c in range(size):
                lbl = tk.Label(self.board_frame, text="", font=("Arial", max(12, self.btn_pixel // 2)),
                               fg="black", bg="white", relief="solid", borderwidth=1)
                lbl.place(x=c * self.btn_pixel, y=r * self.btn_pixel, width=self.btn_pixel, height=self.btn_pixel)
                lbl.bind("<Button-1>", lambda e, row=r, col=c: self.handle_click(row, col))
                self.labels[r][c] = lbl

    def new_game(self):
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        self.turn_label.config(text="Current Turn: P1")
        self.left_score_label.config(text="0")
        self.right_score_label.config(text="0")
        self.controller.show_frame("MenuPage")

    def handle_click(self, row, col):
        lbl = self.labels[row][col]
        if lbl["text"] != "":
            return
        letter = self.left_choice.get() if self.logic.get_current_player() == "p1" else self.right_choice.get()
        result = self.logic.place_letter(row, col, letter)
        lbl.config(text=letter, fg="black")

        if result["sos_found"] > 0:
            color = "cyan" if self.logic.get_current_player() == "p1" else "red"
            for sequence in result["sos_list"]:
                r1, c1 = sequence[0]
                r2, c2 = sequence[2]
                self.draw_line(r1, c1, r2, c2, color)
            self.update_scores()

        if result["game_over"]:
            for r in range(self.controller.grid_size):
                for c in range(self.controller.grid_size):
                    self.labels[r][c].unbind("<Button-1>")
            if result["winner"]:
                if result["winner"] == "draw":
                    self.turn_label.config(text="Draw!")
                else:
                    self.turn_label.config(text=f"{result['winner'].upper()} Wins!")
            else:
                p1_score = self.logic.game_mode.p1_score
                p2_score = self.logic.game_mode.p2_score
                if p1_score > p2_score:
                    self.turn_label.config(text="P1 Wins!")
                elif p1_score < p2_score:
                    self.turn_label.config(text="P2 Wins!")
                else:
                    self.turn_label.config(text="Draw!")
        else:
            current = "P1" if self.logic.get_current_player() == "p1" else "P2"
            self.turn_label.config(text=f"Current Turn: {current}")


    def update_scores(self):
        if self.controller.mode == "general":
            self.left_score_label.config(text=str(self.logic.game_mode.p1_score))
            self.right_score_label.config(text=str(self.logic.game_mode.p2_score))

    def draw_line(self, r1, c1, r2, c2, color):
        dr = r2 - r1
        dc = c2 - c1

        if dr == 0 and abs(dc) == 2:
            positions = [(r1, c1), (r1, c1 + 1), (r1, c1 + 2)]
        elif dc == 0 and abs(dr) == 2:
            positions = [(r1, c1), (r1 + 1, c1), (r1 + 2, c1)]
        elif dr == 2 and dc == 2:
            positions = [(r1, c1), (r1 + 1, c1 + 1), (r1 + 2, c1 + 2)]
        elif dr == 2 and dc == -2:
            positions = [(r1, c1), (r1 + 1, c1 - 1), (r1 + 2, c1 - 2)]
        else:
            return

        for r, c in positions:
            self.labels[r][c].config(bg=color)

    def locateSOS(self, color):
        size = self.logic.game_mode.size
        board = self.logic.game_mode.board
        for r in range(size):
            for c in range(size - 2):
                if board[r][c:c+3] == ["S", "O", "S"]:
                    self.draw_line(r, c, r, c+2, color)

        for c in range(size):
            for r in range(size - 2):
                if [board[r+i][c] for i in range(3)] == ["S", "O", "S"]:
                    self.draw_line(r, c, r+2, c, color)

        for r in range(size - 2):
            for c in range(size - 2):
                if [board[r+i][c+i] for i in range(3)] == ["S", "O", "S"]:
                    self.draw_line(r, c, r+2, c+2, color)

        for r in range(size - 2):
            for c in range(2, size):
                if [board[r+i][c-i] for i in range(3)] == ["S", "O", "S"]:
                    self.draw_line(r, c, r+2, c-2, color)

class SOSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SOS Game")
        self.geometry("900x800")

        self.grid_size = None
        self.mode = None

        container = tk.Frame(self)
        container.pack(expand=True, fill="both")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MenuPage, GamePage):
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MenuPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if page_name == "GamePage":
            self.logic = GameLogic(self.grid_size, self.mode)
            frame.set_logic(self.logic)
            frame.update_mode_label()
            frame.update_score_visibility()
            frame.create_board()

if __name__ == "__main__":
    app = SOSApp()
    app.mainloop()
