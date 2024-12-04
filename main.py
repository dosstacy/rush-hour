from gui.controller import RushHourGame
import tkinter as tk

def run_game():
    root = tk.Tk()
    RushHourGame(root, 'levels/level1.txt')
    root.mainloop()


if __name__ == '__main__':
    run_game()
