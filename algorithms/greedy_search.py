import heapq
import itertools
from elements.Board import Board
from .additional_logic import heuristic, reconstruct_path

class GreedySearch:
    def __init__(self, board):
        self.board = board
        self.counter = itertools.count()

    def solve(self):
        open_set = []
        visited = set()
        heapq.heappush(open_set, (heuristic(self.board), next(self.counter), self.board))
        came_from = {}

        steps = 0
        while open_set:
            steps += 1
            if steps % 1000 == 0:
                print(f"Steps processed: {steps}, Open set size: {len(open_set)}")

            _, _, current = heapq.heappop(open_set)
            if Board.is_win_position(current):
                return reconstruct_path(came_from, current)

            visited.add(hash(current))
            for neighbor, action in Board.get_neighbors(current):
                if hash(neighbor) in visited:
                    continue

                f_score = heuristic(neighbor)

                heapq.heappush(open_set, (f_score, next(self.counter), neighbor))
                came_from[neighbor] = (current, action)

        print("No solution found!")
        return None
