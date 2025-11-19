import tkinter as tk
from gameLogic import GameLogic, PLAYER_1, PLAYER_2

DEF_FONT_SIZE = 20
DEF_FONT = "Arial"
SMALL_FONT_SIZE = 10
ENTRY_WIDTH = 10
TITLE_BOTTOM_PADDING = 20
SECTION_TOP_PADDING = 20
SECTION_BOTTOM_PADDING = 5
BUTTON_PADDING = 10
ALERT_TOP_PADDING = 20
PANEL_WIDTH = 200
BOARD_SIZE = 600
SCORE_SIZE = 72
P1_COLOR = "cyan"
P2_COLOR = "red"
CPU_MOVE_DELAY = 250

class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.pack_propagate(False)
        self.create_inner_frame()
        self.create_title()
        self.create_game_mode_selector()
        self.create_grid_size_input()
        self.create_cpu_toggle()
        self.create_start_button()
        self.create_alert_label()

    def create_inner_frame(self):
        self.inner_frame = tk.Frame(self)
        self.inner_frame.place(relx=0.5, rely=0.5, anchor="center")

    def create_title(self):
        title_label = tk.Label(self.inner_frame, text="SOS Game", font=(DEF_FONT, DEF_FONT_SIZE), fg="white")
        title_label.pack(pady=(0, TITLE_BOTTOM_PADDING))

    def create_game_mode_selector(self):
        self.selected_option = tk.StringVar(value="simple")
        game_modes = [("Simple Game", "simple"), ("General Game", "general")]
        for text, value in game_modes:
            rb = tk.Radiobutton(self.inner_frame, text=text, variable=self.selected_option, value=value, fg="white")
            rb.pack(pady=5)

    def create_grid_size_input(self):
        grid_label = tk.Label(self.inner_frame, text="Enter Grid Size (e.g., 3, 5, 7):", font=(DEF_FONT, SMALL_FONT_SIZE), fg="white")
        grid_label.pack(pady=(SECTION_TOP_PADDING, SECTION_BOTTOM_PADDING))
        self.entry = tk.Entry(self.inner_frame, width=ENTRY_WIDTH, font=(DEF_FONT, SMALL_FONT_SIZE))
        self.entry.pack(pady=5)

    def create_cpu_toggle(self):
        cpu_label = tk.Label(self.inner_frame, text="CPU Player Toggle", font=(DEF_FONT, SMALL_FONT_SIZE), fg="white")
        cpu_label.pack()
        self.cpu1_toggle = tk.IntVar(value=0)
        self.cpu2_toggle = tk.IntVar(value=0)
        self.create_cpu_checkbuttons()

    def create_cpu_checkbuttons(self):
        self.cpu_p1 = tk.Checkbutton(self.inner_frame, text="P1", font=(DEF_FONT, SMALL_FONT_SIZE), fg="white", variable=self.cpu1_toggle)
        self.cpu_p1.pack()
        self.cpu_p2 = tk.Checkbutton(self.inner_frame, text="P2", font=(DEF_FONT, SMALL_FONT_SIZE), fg="white", variable=self.cpu2_toggle)
        self.cpu_p2.pack()

    def create_start_button(self):
        start_button = tk.Button(self.inner_frame, text="Start Game", command=self.start_game)
        start_button.pack(pady=BUTTON_PADDING)

    def create_alert_label(self):
        self.alert_label = tk.Label(self.inner_frame, text="", font=(DEF_FONT, SMALL_FONT_SIZE), fg="white")
        self.alert_label.pack(pady=(ALERT_TOP_PADDING, SECTION_BOTTOM_PADDING))

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
            self.controller.set_game_config(size, mode, self.cpu1_toggle.get(), self.cpu2_toggle.get())
            self.controller.show_frame("GamePage")
            print(f"CPU Toggles - P1:{self.controller.p1_cpu_toggle} P2:{self.controller.p2_cpu_toggle}")
        except ValueError:
            self.alert_label.config(text="Gameboard dimensions must be size 3-15.")

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

            self.controller.set_game_config(size, mode, self.cpu1_toggle.get(), self.cpu2_toggle.get())
            self.controller.show_frame("GamePage")
            print(f"CPU Toggles - P1:{self.controller.p1_cpu_toggle} P2:{self.controller.p2_cpu_toggle}")

        except ValueError:
            self.alert_label.config(text="Gameboard dimensions must be size 3-15.")

class GamePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.game_active = False

        self.btn_pixel = 0
        self.labels = []

        self._main_layout()
        self._left_panel()
        self._board_panel()
        self._right_panel()
        self._bottom_panel()

    def _main_layout(self):
        self.main_container = tk.Frame(self)
        self.main_container.pack(expand=True, fill="both")
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=0)
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(2, weight=0)

    # P1/P2 Widgets
    def _player_widgets(self, parent, player_name, player_color):
        # Score/Points
        score_label = tk.Label(parent, text="0", fg=player_color, font=(DEF_FONT, SCORE_SIZE))
        score_label.pack(padx=BUTTON_PADDING)

        # Player Label for UI
        tk.Label(parent, text=player_name, fg=player_color, font=(DEF_FONT, DEF_FONT_SIZE)).pack(padx=BUTTON_PADDING)

        # S/O Selection
        selection = tk.StringVar(value = "S")
        s_button = tk.Radiobutton(parent, text="S", variable=selection, value="S", fg="white", font=(DEF_FONT, DEF_FONT_SIZE))
        o_button = tk.Radiobutton(parent, text="O", variable=selection, value="O", fg="white", font=(DEF_FONT, DEF_FONT_SIZE))

        cpu_label = tk.Label(parent, text="[CPU]", fg=player_color, font=(DEF_FONT, DEF_FONT_SIZE))

        return score_label, selection, cpu_label, s_button, o_button
    
    # Left panel
    def _left_panel(self):
        self.left_frame = tk.Frame(self.main_container, width=PANEL_WIDTH)
        self.left_frame.grid(row=0, column=0, sticky="ns")

        self.left_score_label, self.left_choice, self.left_cpu_label, self.left_s_button, self.left_o_button = self._player_widgets(parent = self.left_frame, player_name="P1", player_color=P1_COLOR)

    # Right panel
    def _right_panel(self):
        self.right_frame = tk.Frame(self.main_container, width=PANEL_WIDTH)
        self.right_frame.grid(row=0, column=2, sticky="ns")

        self.right_score_label, self.right_choice, self.right_cpu_label, self.right_s_button, self.right_o_button = self._player_widgets(parent = self.right_frame, player_name="P2", player_color=P2_COLOR)

    # Board wrapper
    def _board_panel(self):
        self.board_wrapper = tk.Frame(self.main_container)
        self.board_wrapper.grid(row=0, column=1, sticky="nsew")
        self.board_wrapper.grid_rowconfigure(1, weight=1)
        self.board_wrapper.grid_columnconfigure(0, weight=1)

        self.mode_label = tk.Label(self.board_wrapper, text="", fg="white", font=(DEF_FONT, DEF_FONT_SIZE))
        self.mode_label.grid(row=0, column=0, pady=BUTTON_PADDING)

        self.board_frame = tk.Frame(self.board_wrapper, width=BOARD_SIZE, height=BOARD_SIZE)
        self.board_frame.grid(row=1, column=0)
        self.board_frame.grid_propagate(False)

    # Bottom Frame
    def _bottom_panel(self):
        self.bottom_frame = tk.Frame(self.main_container, width=PANEL_WIDTH)
        self.bottom_frame.grid(row=1, column=1, sticky="nsew")

        self.turn_label = tk.Label(self.bottom_frame, text="Current Turn: P1", fg="white", font=(DEF_FONT, DEF_FONT_SIZE))
        self.turn_label.grid(row=0, column=0, sticky="n")

        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.new_game_btn = tk.Button(self.bottom_frame, text="New Game", font=(DEF_FONT, DEF_FONT_SIZE), command=self.new_game)
        self.new_game_btn.grid(row=1, column=0, pady=(BUTTON_PADDING, 0))

    def set_logic(self, logic):
        self.logic = logic

    def update_mode_label(self):
        self.mode_label.config(text=f"{self.controller.mode.capitalize()} Game")

    def update_score_visibility(self):
        if self.controller.mode == "general":
            self.left_score_label.pack(padx=BUTTON_PADDING, before=self.left_frame.winfo_children()[1])
            self.right_score_label.pack(padx=BUTTON_PADDING, before=self.right_frame.winfo_children()[1])
        else:
            self.left_score_label.pack_forget()
            self.right_score_label.pack_forget()
    
    def cpu_visibility(self):
        """ If CPU for either P1/P2 is enabled, it shows indicator and hides radio buttons.
            If CPU for either P1/P2 is disabled, it hides CPU indicator, shows radio buttons.
        """
        if self.controller.p1_cpu_toggle == 1:
            print("CPU P1: Enabled, hide P1 S/O selection")
            self.left_cpu_label.pack()
            self.left_s_button.pack_forget()
            self.left_o_button.pack_forget()
        else:
            print("CPU P1: Disabled")
            self.left_cpu_label.pack_forget()
            self.left_s_button.pack(pady=5)
            self.left_o_button.pack(pady=5)
        if self.controller.p2_cpu_toggle == 1:
            print("CPU P2: Enabled, hide P2 S/O selection")
            self.right_cpu_label.pack()
            self.right_s_button.pack_forget()
            self.right_o_button.pack_forget()
        else:
            print("CPU P2: Disabled, show P2 S/O selection")
            self.right_cpu_label.pack_forget()
            self.right_s_button.pack(pady=5)
            self.right_o_button.pack(pady=5)
  
    def create_board(self):
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        size = self.controller.grid_size
        board_pixel = BOARD_SIZE
        self.btn_pixel = board_pixel // size

        self.labels = [[None for _ in range(size)] for _ in range(size)]

        for r in range(size):
            for c in range(size):
                lbl = tk.Label(self.board_frame, text="", font=("Arial", max(12, self.btn_pixel // 2)),
                               fg="black", bg="white", relief="solid", borderwidth=1)
                lbl.place(x=c * self.btn_pixel, y=r * self.btn_pixel, width=self.btn_pixel, height=self.btn_pixel)
                # Enables clicking only when it's human turn
                if self.controller.p1_cpu_toggle == 0 or self.controller.p2_cpu_toggle == 0:
                    lbl.bind("<Button-1>", lambda e, row=r, col=c: self.handle_click(row, col))
                self.labels[r][c] = lbl

    def new_game(self):
        self.game_active = False
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        self.turn_label.config(text="Current Turn: P1")

        self.left_score_label.config(text="0")
        self.right_score_label.config(text="0")

        self.controller.show_frame("MenuPage")

    def handle_click(self, row, col, letter=None):
        if not self._is_valid_move(row, col):
            return
        if letter is None:
            letter = self._get_player_letter()
       
        result = self.logic.place_letter(row, col, letter)
        self._update_cell(row, col, letter)
        self._process_result(result)

    def _is_valid_move(self, row, col):
        return self.labels[row][col]["text"] == ""

    def _get_player_letter(self):
        current_player = self.logic.get_current_player()
        if current_player == PLAYER_1:
            return self.left_choice.get()
        else:
            return self.right_choice.get()

    def _update_cell(self, row, col, letter):
        self.labels[row][col].config(text=letter, fg="black")

    def _cpu_check_and_play(self):
        if not self.game_active:
            return
        cpu_move = self.logic.get_cpu_move()
        if cpu_move:
            print(f"CPU move result: {cpu_move}")
            row, col, letter = cpu_move
            self.after(CPU_MOVE_DELAY, lambda: self._execute_cpu_move(row, col, letter))
    
    def _execute_cpu_move(self, row, col, letter):
        if not self.game_active:
            return
        self.handle_click(row, col, letter)

    def _process_result(self, result):
        if result["sos_found"] > 0:
            self._draw_sos_sequences(result["sos_list"])
            self._update_scores()

        if result["game_over"]:
            self._handle_game_over(result)
        else:
            self._update_turn_label()
            self._cpu_check_and_play()
            
    def _draw_sos_sequences(self, sos_list):
        color = P1_COLOR if self.logic.get_current_player() == PLAYER_1 else P2_COLOR
        for sequence in sos_list:
            r1, c1 = sequence[0]
            r2, c2 = sequence[2]
            self._draw_line(r1, c1, r2, c2, color)

    def _handle_game_over(self, result):
        self.game_active = False
        self._disable_board()
        winner_text = self._get_winner_text(result)
        self.turn_label.config(text=winner_text)

    def _disable_board(self):
        for r in range(self.controller.grid_size):
            for c in range(self.controller.grid_size):
                self.labels[r][c].unbind("<Button-1>")

    def _get_winner_text(self, result):
        if result["winner"]:
            if result["winner"] == "draw":
                return "Draw!"
            else:
                return f"{result['winner'].upper()} Wins!"
        else:
            scores = self.logic.get_scores()
            if scores[PLAYER_1] > scores[PLAYER_2]:
                return "P1 Wins!"
            elif scores[PLAYER_1] < scores[PLAYER_2]:
                return "P2 Wins!"
            else:
                return "Draw!"

    def _update_turn_label(self):
        current = "P1" if self.logic.get_current_player() == PLAYER_1 else "P2"
        self.turn_label.config(text=f"Current Turn: {current}")

    def _update_scores(self):
        if self.controller.mode == "general":
            scores = self.logic.get_scores()
            self.left_score_label.config(text=str(scores[PLAYER_1]))
            self.right_score_label.config(text=str(scores[PLAYER_2]))

    def _draw_line(self, r1, c1, r2, c2, color):
        positions = self._get_line_positions(r1, c1, r2, c2)
        for r, c in positions:
            self.labels[r][c].config(bg=color)

    def _get_line_positions(self, r1, c1, r2, c2):
        dr = r2 - r1
        dc = c2 - c1

        if dr == 0 and abs(dc) == 2:
            return [(r1, c1), (r1, c1 + 1), (r1, c1 + 2)]
        elif dc == 0 and abs(dr) == 2:
            return [(r1, c1), (r1 + 1, c1), (r1 + 2, c1)]
        elif dr == 2 and dc == 2:
            return [(r1, c1), (r1 + 1, c1 + 1), (r1 + 2, c1 + 2)]
        elif dr == 2 and dc == -2:
            return [(r1, c1), (r1 + 1, c1 - 1), (r1 + 2, c1 - 2)]
        else:
            print(f"Warning: Invalid line positions ({r1},{c1}) to ({r2},{c2})")
            return []

class SOSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SOS Game")
        self.geometry("900x800")

        self.grid_size = None
        self.mode = None
        self.p1_cpu_toggle = False
        self.p2_cpu_toggle = False

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

    def set_game_config(self, grid_size, mode, p1_cpu, p2_cpu):
        self.grid_size = grid_size
        self.mode = mode
        self.p1_cpu_toggle = p1_cpu
        self.p2_cpu_toggle = p2_cpu

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if page_name == "GamePage":
           
            p1_type = "computer" if self.p1_cpu_toggle == 1 else "human"
            p2_type = "computer" if self.p2_cpu_toggle == 1 else "human"
            self.logic = GameLogic(self.grid_size, self.mode, p1_type, p2_type)

            frame.set_logic(self.logic)
            frame.update_mode_label()
            frame.update_score_visibility()
            frame.cpu_visibility()
            frame.create_board()
            frame.game_active = True

            # P1 plays first, checks if CPU plays
            frame._cpu_check_and_play()

if __name__ == "__main__":
    app = SOSApp()
    app.mainloop()