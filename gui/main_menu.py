import tkinter as tk
from PIL import Image, ImageTk

class MainMenu:
    def __init__(self, game):
        self.game = game
        self.frame = tk.Frame(self.game.root)
        self.create_widgets()

    def create_widgets(self):
        background_image = Image.open("images/bg.png")
        background_image = background_image.resize((800, 800))
        self.bg_photo = ImageTk.PhotoImage(background_image)
        self.bg_label = tk.Label(self.frame, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)
        play_button = tk.Button(self.frame, text="Play", font=("Helvetica", 16, "bold"), command=self.game.show_level_menu, height=2, width=12)
        play_button.place(relx=0.5, rely=0.6, anchor="center")

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()