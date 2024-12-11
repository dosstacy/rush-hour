from gui.game_controller import RushHourGame
import tkinter as tk

##TODO: win
##TODO: кнопка "повернути назад до рівнів"?
##TODO: фото замість прямокутників?
##TODO: розділити клас RushHourGame на декілька частин

def run_game():
    root = tk.Tk()
    RushHourGame(root)
    root.mainloop()


if __name__ == '__main__':
    run_game()
