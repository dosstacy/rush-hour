import tkinter as tk
from elements.Board import Board
from algorithms.dfs import Dfs
from algorithms.a_star import A_star
from algorithms.greedy_search import GreedySearch
from utils import is_win_position, MAIN_CAR
from tkinter import ttk
from PIL import Image, ImageTk

##TODO: змінити дизайн кнопок, розташувати кнопки з рівнями в 2-3 ряди, ігрове поле посередині (якщо можна, то з заокругленими кутами) + bg ззаду
##TODO: коли користувач обирає інший алгоритм - рестартнути поле, кнопка "повернути назад до рівнів"?
##TODO: фото замість прямокутників?
##TODO: розділити клас RushHourGame на декілька частин

class RushHourGame:
    def __init__(self, root):
        self.main_menu_frame = None
        self.root = root
        self.root.geometry("700x700")
        self.board = None
        self.canvas = None
        self.selected_car = None

        self.create_main_menu()

    def create_main_menu(self):
        self.main_menu_frame = tk.Frame(self.root)
        self.main_menu_frame.pack(fill="both", expand=True)

        background_image = Image.open("images/bg.png")
        background_image = background_image.resize((700, 700))
        self.bg_photo = ImageTk.PhotoImage(background_image)
        self.bg_label = tk.Label(self.main_menu_frame, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        play_button = ttk.Button(self.main_menu_frame, text="Play", command=self.show_level_menu)
        play_button.place(relx=0.5, rely=0.5, anchor="center")

    def show_level_menu(self):
        self.main_menu_frame.pack_forget()
        self.level_menu_frame = tk.Frame(self.root)
        self.level_menu_frame.pack(fill="both", expand=True)

        background_image = Image.open("images/bg2.png")
        background_image = background_image.resize((700, 700))
        self.bg_photo2 = ImageTk.PhotoImage(background_image)
        self.bg_label = tk.Label(self.level_menu_frame, image=self.bg_photo2)
        self.bg_label.place(relwidth=1, relheight=1)

        for i in range(1, 11):
            level_button = ttk.Button(self.level_menu_frame, text=f"Level {i}", command=lambda i=i: self.start_game(f"levels/level{i}.txt"))
            level_button.place(relx=0.5, rely=0.09 * i, anchor="center")

    def start_game(self, level_file):
        self.level_menu_frame.pack_forget()
        self.board = Board(Board.init_board(level_file))
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()
        self.create_buttons(self.root)
        self.draw_board()
        self.bind_keys()

    def create_buttons(self, root):
        solve_button = ttk.Button(root, text="DFS", command=self.dfs_solve)
        solve_button.pack(side=tk.LEFT)

        restart_button = ttk.Button(root, text="Restart", command=self.restart_game)
        restart_button.pack(side=tk.LEFT)

        a_star_button = ttk.Button(root, text="A*", command=self.a_star_solve)
        a_star_button.pack(side=tk.LEFT)

        greedy_button = ttk.Button(root, text="Greedy Search", command=self.greedy_solve)
        greedy_button.pack(side=tk.LEFT)

    def bind_keys(self):
        self.root.bind("<Up>", lambda event: self.move_car("up"))
        self.root.bind("<Down>", lambda event: self.move_car("down"))
        self.root.bind("<Left>", lambda event: self.move_car("left"))
        self.root.bind("<Right>", lambda event: self.move_car("right"))

    def draw_board(self):
        self.canvas.delete("all")
        cell_size = 400 // self.board.grid_size

        for row_idx, row in enumerate(self.board.grid):
            for col_idx, cell in enumerate(row):
                x1, y1 = col_idx * cell_size, row_idx * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size
                self.board.cars.get(MAIN_CAR)

                if cell == ".":
                    color = "white"
                else:
                    color = "red" if cell == "A" else "lightblue"

                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                if cell != ".":
                    self.canvas.create_text(
                        (x1 + x2) // 2, (y1 + y2) // 2, text=cell, font=("Arial", 14)
                    )

                    self.canvas.tag_bind(rect, "<Button-1>", lambda event, car_name=cell: self.select_car(car_name))

    def update_board_view(self):
        self.draw_board()

    def move_car(self, direction):
        if self.selected_car is None:
            print("No car selected!")
            return

        car = self.board.cars[self.selected_car]
        if not self.board.is_valid_move(car, direction):
            print("Invalid move!")
            return

        self.board.move_car(car, direction)
        self.update_board_view()

    def select_car(self, car_name):
        self.selected_car = car_name
        print(f"Selected car: {car_name}")

    def restart_game(self):
        print("Restarting the game...")
        self.board = Board(Board.init_board(self.level_file))
        self.selected_car = None
        self.update_board_view()

    def visualize_solution(self, solution):
        def perform_step(index):
            if index >= len(solution):
                is_win_position(self.board)
                return
            car_name, direction = solution[index]
            self.board.move_car(self.board.cars[car_name], direction)
            self.update_board_view()
            self.root.after(500, perform_step, index + 1)

        perform_step(0)

    ################################################## DFS #################################################################

    def dfs_solve(self):
        solver = Dfs(self.board)
        solution = solver.solve()
        if solution:
            print("Solution found!")
            print(f"Solution found in {len(solution)} steps.")
            self.visualize_solution(solution)
        else:
            print("No solution found!")

    ################################################## A STAR ##############################################################

    def a_star_solve(self):
        print("Solving with A*...")
        solver = A_star(self.board)
        solution = solver.solve()
        if solution:
            print("Solution found!")
            print(f"A* Solution found in {len(solution)} steps.")
            self.visualize_solution(solution)
        else:
            print("No solution found with A*!")

    ################################################## GREEDY SEARCH ##############################################################

    def greedy_solve(self):
        print("Solving with Greedy Search...")
        solver = GreedySearch(self.board)
        solution = solver.solve()
        if solution:
            print("Solution found!")
            print(f"Greedy Search solution found in {len(solution)} steps.")
            self.visualize_solution(solution)
        else:
            print("No solution found with Greedy Search!")
