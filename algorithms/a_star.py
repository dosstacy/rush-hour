import heapq
import itertools
from elements.Board import Board
from .additional_logic import heuristic, reconstruct_path

class A_star:
        def __init__(self, board):
            self.board = board
            self.counter = itertools.count()

        def solve(self):
            open_set = []
            visited = set()
            heapq.heappush(open_set, (0, next(self.counter), self.board))
            came_from = {}
            g_score = {self.board: 0}
            f_score = {self.board: heuristic(self.board)}

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

                    tentative_g_score = g_score[current] + 1
                    if tentative_g_score < g_score.get(neighbor, float('inf')):
                        came_from[neighbor] = (current, action)
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + heuristic(neighbor)
                        heapq.heappush(open_set, (f_score[neighbor], next(self.counter), neighbor))
            return None