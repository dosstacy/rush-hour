import tkinter as tk
from elements.Board import Board
from algorithms.dfs import RushHourSolverDFS
from algorithms.a_star import A_star
import threading

class RushHourGame:
    def __init__(self, root, level_file):
        self.root = root
        self.level_file = level_file
        self.board = Board(Board.init_board(level_file))
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()

        # Кнопки керування
        self.solve_button = tk.Button(root, text="DFS", command=self.auto_solve)
        self.solve_button.pack(side=tk.LEFT)

        self.restart_button = tk.Button(root, text="Restart", command=self.restart_game)
        self.restart_button.pack(side=tk.LEFT)

        self.a_star_button = tk.Button(root, text="A*", command=self.a_star_solve)
        self.a_star_button.pack(side=tk.LEFT)

        self.selected_car = None

        self.draw_board()

        # Зв'язування клавіш для руху машинок
        self.root.bind("<Up>", lambda event: self.move_car("up"))
        self.root.bind("<Down>", lambda event: self.move_car("down"))
        self.root.bind("<Left>", lambda event: self.move_car("left"))
        self.root.bind("<Right>", lambda event: self.move_car("right"))

    def draw_board(self):
        """Відображення ігрового поля на Canvas."""
        self.canvas.delete("all")
        cell_size = 400 // self.board.grid_size

        for row_idx, row in enumerate(self.board.grid):
            for col_idx, cell in enumerate(row):
                x1, y1 = col_idx * cell_size, row_idx * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size
                color = "white" if cell == "." else "lightblue"
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                if cell != ".":
                    self.canvas.create_text(
                        (x1 + x2) // 2, (y1 + y2) // 2, text=cell, font=("Arial", 14)
                    )
                    # Обробник для вибору машинки
                    self.canvas.tag_bind(rect, "<Button-1>", lambda event, car_name=cell: self.select_car(car_name))

    def update_board_view(self):
        """Оновлення графічного інтерфейсу."""
        self.draw_board()

    def auto_solve(self):
        """Рішення задачі методом DFS."""
        solver = RushHourSolverDFS(self.board)
        solution = solver.solve()
        if solution:
            print(f"Solution found in {len(solution)} steps.")
            self.animate_solution(solution)
        else:
            print("No solution found!")

    def animate_solution(self, solution):
        """Відтворення рішення покроково."""
        def perform_step(index):
            if index >= len(solution):
                self.check_win()  # Перевіряємо виграш після завершення
                return
            car_name, direction = solution[index]
            self.board.move_car(self.board.cars[car_name], direction)
            self.update_board_view()
            self.root.after(500, perform_step, index + 1)

        perform_step(0)

    def move_car(self, direction):
        """Рух вибраної машинки за допомогою клавіш."""
        if self.selected_car is None:
            print("No car selected!")
            return

        car = self.board.cars[self.selected_car]
        if not self.board.is_valid_move(car, direction):
            print("Invalid move!")
            return

        self.board.move_car(car, direction)
        self.update_board_view()
        self.check_win()

    def check_win(self):
        """Перевіряє, чи виграв користувач."""
        car = self.board.cars.get("A")
        if car and any(y == self.board.grid_size - 1 for x, y in car.positions):
            print("You win!")
            self.root.quit()

    def select_car(self, car_name):
        """Вибір машинки користувачем."""
        self.selected_car = car_name
        print(f"Selected car: {car_name}")

    def restart_game(self):
        """Перезапуск гри."""
        print("Restarting the game...")
        self.board = Board(Board.init_board(self.level_file))
        self.selected_car = None
        self.update_board_view()

    def a_star_solve(self):
        """Рішення задачі алгоритмом A*."""
        def solve_and_animate():
            print("Solving with A*...")
            solver = A_star(self.board)
            solution = solver.solve()
            if solution:
                print(f"A* Solution found in {len(solution)} steps.")
                self.animate_solution(solution)
            else:
                print("No solution found with A*!")

        # Виконуємо алгоритм в окремому потоці
        threading.Thread(target=solve_and_animate).start()
