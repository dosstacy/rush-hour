import heapq
import itertools
from utils import is_win_position, WIN_X, WIN_Y, get_neighbors, MAIN_CAR
from additional_logic import heuristic, reconstruct_path

class GreedySearch:
    def __init__(self, board):
        self.start_state = board
        self.counter = itertools.count()  # Унікальний індекс для кожного елемента

    def solve(self):
        open_set = []
        visited = set()  # Для уникнення дублювання станів
        heapq.heappush(open_set, (heuristic(self.start_state), next(self.counter), self.start_state))
        came_from = {}

        steps = 0
        while open_set:
            steps += 1
            if steps % 1000 == 0:
                print(f"Steps processed: {steps}, Open set size: {len(open_set)}")

            _, _, current = heapq.heappop(open_set)
            if is_win_position(current):
                # Повертає послідовність ходів для візуалізації
                return reconstruct_path(came_from, current)

            visited.add(hash(current))
            for neighbor, action in get_neighbors(current):
                if hash(neighbor) in visited:
                    continue

                # Обчислюємо тільки евристичну функцію для Greedy Search
                f_score = heuristic(neighbor)

                heapq.heappush(open_set, (f_score, next(self.counter), neighbor))
                came_from[neighbor] = (current, action)

        print("No solution found!")
        return None
