import tkinter as tk
from PIL import Image, ImageTk

class LevelMenu:
    def __init__(self, game):
        self.game = game
        self.frame = tk.Frame(self.game.root)
        self.create_widgets()

    def create_widgets(self):
        background_image = Image.open("images/bg2.png")
        background_image = background_image.resize((800, 800))
        self.bg_photo2 = ImageTk.PhotoImage(background_image)
        self.bg_label = tk.Label(self.frame, image=self.bg_photo2)
        self.bg_label.place(relwidth=1, relheight=1)
        for i in range(1, 11):
            row = (i - 1) // 5
            col = (i - 1) % 5
            level_button = tk.Button(self.frame, text=f"Level {i}", height=3, width=10, font=("Helvetica", 11, "bold"), command=lambda i=i: self.game.start_game(f"levels/level{i}.txt"))
            level_button.place(relx=0.17 * (col + 1), rely=0.35 * (row + 1), anchor="center")

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()