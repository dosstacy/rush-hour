from .main_menu import MainMenu
from .level_menu import LevelMenu
from .game_board import GameBoard

class RushHourGame:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x750")
        self.main_menu = MainMenu(self)
        self.level_menu = LevelMenu(self)
        self.game_board = GameBoard(self)
        self.show_main_menu()

    def show_main_menu(self):
        self.level_menu.hide()
        self.game_board.hide()
        self.main_menu.show()

    def show_level_menu(self):
        self.main_menu.hide()
        self.game_board.hide()
        self.level_menu.show()

    def start_game(self, level_file):
        self.main_menu.hide()
        self.level_menu.hide()
        self.game_board.start(level_file)