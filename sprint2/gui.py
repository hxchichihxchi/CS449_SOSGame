import tkinter as tk

class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Outer frame fills the whole parent
        self.pack_propagate(False)  # prevent shrinking  # optional background

        # Inner frame for widgets
        inner_frame = tk.Frame(self)
        inner_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Widgets
        tk.Label(inner_frame, text="SOS Game", font=("Arial", 24), fg="white").pack(pady=(0, 20))

        self.selected_option = tk.StringVar(value="single")
        tk.Radiobutton(inner_frame, text="Singleplayer (VS AI)", variable=self.selected_option, value="single", fg="white").pack(pady=5)
        tk.Radiobutton(inner_frame, text="Two Players", variable=self.selected_option, value="multi", fg="white").pack(pady=5)

        tk.Label(inner_frame, text="Enter Grid Size (e.g., 3, 5, 7):", font=("Arial", 16), fg="white").pack(pady=(20, 5))
        self.entry = tk.Entry(inner_frame, width=10, font=("Arial", 14))
        self.entry.pack(pady=5)

        tk.Button(inner_frame, text="Start Game", command=self.start_game).pack(pady=10)


    def start_game(self):
        try:
            size = int(self.entry.get())
            if size < 3:
                raise ValueError
            if size > 15:
                raise ValueError
            self.controller.grid_size = size
            self.controller.mode = self.selected_option.get()
            self.controller.show_frame("GamePage")
        except ValueError:
            print("Enter a positive integer less than 15 for grid size!")

class GamePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        main_container = tk.Frame(self)
        main_container.pack(expand=True, fill="both")
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=0)  # left panel
        main_container.grid_columnconfigure(1, weight=1)  # board
        main_container.grid_columnconfigure(2, weight=0)  

         # Left panel
        self.left_frame = tk.Frame(main_container, width=200)
        self.left_frame.grid(row=0, column=0, sticky="ns")
        # add widgets to left_frame
        tk.Label(self.left_frame, text="0", fg = "cyan", font=("Arial", 72)).pack(padx=10)
        tk.Label(self.left_frame, text="P1", fg = "cyan", font=("Arial", 20)).pack(padx=10)

        self.left_choice = tk.StringVar(value="S")
        tk.Radiobutton(self.left_frame, text="S", variable=self.left_choice, value = "S", fg="white", font=("Arial", 20)).pack(pady=5)
        tk.Radiobutton(self.left_frame, text="O", variable=self.left_choice, value = "O", fg="white", font=("Arial", 20)).pack(pady=5)


        # Center board
        self.board_frame = tk.Frame(main_container, bg="black")
        self.board_frame.grid(row=0, column=1, sticky="nsew")

        # Right panel
        self.right_frame = tk.Frame(main_container, width=200)
        self.right_frame.grid(row=0, column=2, sticky="ns")
        # add widgets to right_frame
        tk.Label(self.right_frame, text="0", fg = "red",font=("Arial", 72)).pack(padx=10)
        tk.Label(self.right_frame, text="P2", fg = "red", font=("Arial", 20)).pack(padx=10)

        self.right_choice = tk.StringVar(value="S")
        tk.Radiobutton(self.right_frame, text="S", variable=self.right_choice, value = "S", fg="white", font=("Arial", 20)).pack(pady=5)
        tk.Radiobutton(self.right_frame, text="O", variable=self.right_choice, value = "O", fg="white", font=("Arial", 20)).pack(pady=5)
        
    def create_board(self):
        # Clear previous widgets
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        size = self.controller.grid_size

        for r in range(size):
            self.board_frame.grid_rowconfigure(r, weight=1)
            self.board_frame.grid_columnconfigure(r, weight=1)

        for r in range(size):
            for c in range(size):
                btn = tk.Button(self.board_frame, text="", font=("Courier", 15), fg = "black")
                btn.grid(row=r, column=c, sticky="nsew")
        
        
class SOSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SOS Game")
        self.geometry("1280x720")

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
            frame.create_board()

if __name__ == "__main__":
    app = SOSApp()
    app.mainloop()

