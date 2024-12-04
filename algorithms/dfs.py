import heapq
import itertools

class RushHourSolverDFS:
        def __init__(self, board):
            self.initial_state = board

        def is_goal(self, state):
            for car_name, car in state.cars.items():
                if car_name == "A":  # Цільова машина
                    for x, y in car.positions:
                        if y == state.grid_size - 1:  # Досягла виходу
                            return True
            return False

        def get_neighbors(self, state):
            neighbors = []
            for car_name, car in state.cars.items():
                for direction in ["up", "down", "left", "right"]:
                    if state.is_valid_move(car, direction):
                        new_state = state.copy()
                        new_state.move_car(new_state.cars[car_name], direction)
                        neighbors.append((new_state, (car_name, direction)))  # Зберігаємо пару
            return neighbors

        def solve(self):
            stack = [(self.initial_state, [])]
            visited = set()

            while stack:
                current, path = stack.pop()

                state_key = current.board_to_key()
                if state_key in visited:
                    continue
                visited.add(state_key)

                if self.is_goal(current):
                    print("Solution found!")
                    print(f"Solution found in {len(path)} steps.")
                    return path

                for neighbor, action in self.get_neighbors(current):
                    stack.append((neighbor, path + [action]))

            print("No solution found!")
            return None
