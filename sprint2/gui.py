import tkinter as tk

class SOSApp(tk.Tk):
    """Single-window SOS Game GUI with everything centered"""
    def __init__(self):
        super().__init__()
        self.title("SOS Game")
        self.geometry("600x600")

        # Store chosen settings
        self.mode = None
        self.grid_size = None
        self.turn = None

        # Create a frame to center everything
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(expand=True)  # centers the frame vertically & horizontally

        self.create_widgets()

    def create_widgets(self):
        # SOS title
        tk.Label(self.main_frame, text="SOS Game", font=("Arial", 24)).pack(pady=(0, 20))

        # Mode selection radial buttons
        def show_selection():
            print(f"Selected: {selected_option.get()}")

        selected_option = tk.StringVar()
        selected_option.set("single")   # default option
        radio1 = tk.Radiobutton(self.main_frame, text="Singleplayer (VS AI)", variable=selected_option, value="single", command=show_selection)
        radio2 = tk.Radiobutton(self.main_frame, text="Two Players", variable=selected_option, value="multi", command=show_selection)
        radio1.pack(pady=5)
        radio2.pack(pady=5)

        # Board size input
        tk.Label(self.main_frame, text="Enter Grid Size (e.g., 3, 5, 7):", font=("Arial", 16)).pack(pady=(20, 5))
        self.entry = tk.Entry(self.main_frame, width=10, font=("Arial", 14))
        self.entry.pack(pady=5)

        tk.Button(self.main_frame, text="Submit Grid Size", width=20, command=self.submit_grid_size).pack(pady=10)

    
    def select_mode(self, mode):
        self.mode = mode
        print(f"Mode selected: {mode}")

    def submit_grid_size(self):
        value = self.entry.get()
        try:
            size = int(value)
            if size < 1:
                raise ValueError("Grid size must be positive")
            self.grid_size = size
            print(f"Grid size selected: {size}")
        except ValueError:
            print("Invalid input! Please enter a positive integer.")


if __name__ == "__main__":
    app = SOSApp()
    app.mainloop()
