import tkinter as tk
from PIL import Image, ImageTk
from elements.Board import Board
from algorithms.dfs import Dfs
from algorithms.a_star import A_star
from algorithms.greedy_search import GreedySearch
import textwrap


class GameBoard:
    def __init__(self, game):
        self.game = game
        self.frame = tk.Frame(self.game.root)
        self.canvas = tk.Canvas(self.game.root, width=390, height=390)
        self.canvas_info = tk.Canvas(self.game.root, width=150, height=390)
        self.selected_car = None
        self.is_paused = False
        self.current_index = 0
        self.solution = []
        self.algo_info = ""
        self.car_colors = {}
        self.color_list = ["blue", "green", "yellow", "purple", "orange", "pink", "cyan", "magenta", "brown", "lime"]
        self.color_index = 0

    def start(self, level_file):
        self.frame.pack(fill="both", expand=True)
        background_image = Image.open("images/bg2.png")
        background_image = background_image.resize((800, 800))
        self.bg_photo2 = ImageTk.PhotoImage(background_image)
        self.bg_label = tk.Label(self.frame, image=self.bg_photo2)
        self.bg_label.place(relwidth=1, relheight=1)
        self.level_file = level_file
        self.board = Board(Board.init_board(level_file))
        self.canvas.place(relx=0.3, rely=0.5, anchor="center")
        self.canvas_info.place(relx=0.8, rely=0.5, anchor="center")
        self.create_buttons(self.game.root)
        self.draw_board()
        self.bind_keys()

    def create_buttons(self, root):
        self.buttons = []

        solve_button = tk.Button(root, text="DFS", font=("Helvetica", 12, "bold"), command=self.dfs_solve, height=2,
                                 width=10)
        solve_button.place(relx=0.12, rely=0.15, anchor="center")
        self.buttons.append(solve_button)

        a_star_button = tk.Button(root, text="A*", font=("Helvetica", 12, "bold"), command=self.a_star_solve, height=2,
                                  width=10)
        a_star_button.place(relx=0.29, rely=0.15, anchor="center")
        self.buttons.append(a_star_button)

        greedy_button = tk.Button(root, text="Greedy Search", font=("Helvetica", 12, "bold"), command=self.greedy_solve,
                                  height=2, width=11)
        greedy_button.place(relx=0.47, rely=0.15, anchor="center")
        self.buttons.append(greedy_button)

        restart_button = tk.Button(root, text="Restart", font=("Helvetica", 12, "bold"), command=self.restart_game,
                                   height=2, width=10)
        restart_button.place(relx=0.2, rely=0.84, anchor="center")
        self.buttons.append(restart_button)

        pause_button = tk.Button(root, text="Pause", font=("Helvetica", 12, "bold"), command=self.toggle_pause,
                                 height=2, width=10)
        pause_button.place(relx=0.38, rely=0.84, anchor="center")
        self.buttons.append(pause_button)

        return_button = tk.Button(root, text="Back to levels", font=("Helvetica", 9, "bold"),
                                  command=self.game.levels_back,
                                  height=1, width=12)
        return_button.place(relx=0.11, rely=0.05, anchor="center")
        self.buttons.append(return_button)

    def draw_board(self):
        self.canvas.delete("all")
        cell_size = 400 // self.board.grid_size

        for row_idx, row in enumerate(self.board.grid):
            for col_idx, cell in enumerate(row):
                x1, y1 = col_idx * cell_size, row_idx * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size

                if cell == ".":
                    color = "white"
                elif cell == "A":
                    color = "red"
                else:
                    if cell not in self.car_colors:
                        self.car_colors[cell] = self.color_list[self.color_index]
                        self.color_index = (self.color_index + 1) % len(self.color_list)
                    color = self.car_colors[cell]

                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

                if cell != ".":
                    self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=cell, font=("Arial", 10))
                    self.canvas.tag_bind(rect, "<Button-1>", lambda event, car_name=cell: self.select_car(car_name))

                text_label = tk.Label(self.frame, width=5, height=2, text="<- Exit", font=("Arial", 14, "bold"),
                                      bg="orange")
                text_label.place(relx=0.6, rely=0.46, anchor="center")

    def bind_keys(self):
        self.game.root.bind("<Up>", lambda event: self.check_position("up"))
        self.game.root.bind("<Down>", lambda event: self.check_position("down"))
        self.game.root.bind("<Left>", lambda event: self.check_position("left"))
        self.game.root.bind("<Right>", lambda event: self.check_position("right"))

    def check_position(self, direction):
        if self.selected_car is None:
            print("No car selected!")
            return
        car = self.board.cars[self.selected_car]
        if not self.board.is_valid_move(car, direction):
            print("Invalid move!")
            return
        self.board.move_car(car, direction)
        self.draw_board()
        if Board.is_win_position(self.board):
            self.show_win_text()

    def select_car(self, car_name):
        self.selected_car = car_name
        print(f"Selected car: {car_name}")

    def visualize_solution(self, solution):
        self.solution = solution
        self.current_index = 0
        self.is_paused = False
        self._perform_step()

    def _perform_step(self):
        if self.is_paused or self.current_index >= len(self.solution):
            return
        car_name, direction = self.solution[self.current_index]
        self.board.move_car(self.board.cars[car_name], direction)
        self.draw_board()
        self.current_index += 1
        if self.current_index < len(self.solution):
            self.game.root.after(500, self._perform_step)
        else:
            Board.is_win_position(self.board)
            self.show_win_text()

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if not self.is_paused:
            self._perform_step()

    def restart_game(self):
        self.board = Board(Board.init_board(self.level_file))
        self.selected_car = None
        self.update_board_view()
        self.algo_info = ""
        self.show_steps()

    def update_board_view(self):
        self.draw_board()

    def dfs_solve(self):
        solver = Dfs(self.board)
        solution = solver.solve()
        if solution:
            self.algo_info = f"The solution was found using the DFS algorithm in {len(solution)} steps."
            self.visualize_solution(solution)
        else:
            self.algo_info = "No solution found with DFS!"
        self.show_steps()

    def a_star_solve(self):
        print("Solving with A*...")
        solver = A_star(self.board)
        solution = solver.solve()
        if solution:
            self.algo_info = f"A* Solution found in {len(solution)} steps."
            self.visualize_solution(solution)
        else:
            self.algo_info = "No solution found with A*!"
        self.show_steps()

    def greedy_solve(self):
        print("Solving with Greedy Search...")
        solver = GreedySearch(self.board)
        solution = solver.solve()
        if solution:
            self.algo_info = f"Greedy Search solution found in {len(solution)} steps."
            self.visualize_solution(solution)
        else:
            self.algo_info = "No solution found with Greedy Search!"
        self.show_steps()

    def hide(self):
        self.frame.pack_forget()

    def hide_elements(self):
        for button in self.buttons:
            button.place_forget()
        self.canvas.place_forget()
        self.canvas_info.delete("all")
        self.canvas_info.place_forget()
        self.bg_label.place_forget()
        self.frame.pack_forget()

    def show_steps(self):
        self.canvas_info.delete("all")

        max_width = 17
        wrapped_text = textwrap.fill(self.algo_info, width=max_width)

        self.canvas_info.create_text(75, 120, text=wrapped_text, font=("Arial", 13), anchor="center")

    def show_win_text(self):
        max_width = 16
        wrapped_text = textwrap.fill("Congratulations! This is win position!", width=max_width)

        self.canvas_info.create_text(75, 200, text=wrapped_text, font=("Arial", 13, "bold"), anchor="center",
                                     fill="red")
