import heapq
import itertools
import time
import tracemalloc
from elements.Board import Board
from .additional_logic import heuristic, reconstruct_path

class GreedySearch:
    def __init__(self, board):
        self.board = board
        self.counter = itertools.count()

    def solve(self):
        start_time = time.time()
        tracemalloc.start()

        open_set = []
        visited = set()
        heapq.heappush(open_set, (heuristic(self.board), next(self.counter), self.board))
        came_from = {}

        steps = 0
        max_open_set_size = 0
        while open_set:
            steps += 1
            max_open_set_size = max(max_open_set_size, len(open_set))

            _, _, current = heapq.heappop(open_set)

            state_key = current.board_to_key()
            if state_key in visited:
                continue
            visited.add(state_key)

            if Board.is_win_position(current):
                end_time = time.time()
                current_memory, peak_memory = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                solution_path = reconstruct_path(came_from, current)
                print("Solution found!")
                print(f"Time taken: {end_time - start_time:.2f} seconds")
                print(f"Steps taken: {steps}")
                print(f"Visited states: {len(visited)}")
                print(f"Max open set size: {max_open_set_size}")
                print(f"Current memory usage: {current_memory / 1024:.2f} KB")
                print(f"Peak memory usage: {peak_memory / 1024:.2f} KB")
                print(f"Solution path length: {len(solution_path)}")
                return solution_path

            for neighbor, action in Board.get_neighbors(current):
                neighbor_key = neighbor.board_to_key()
                if neighbor_key in visited:
                    continue

                f_score = heuristic(neighbor)
                heapq.heappush(open_set, (f_score, next(self.counter), neighbor))
                came_from[neighbor] = (current, action)

        end_time = time.time()
        current_memory, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print("No solution found!")
        print(f"Time taken: {end_time - start_time:.2f} seconds")
        print(f"Steps taken: {steps}")
        print(f"Visited states: {len(visited)}")
        print(f"Current memory usage: {current_memory / 1024:.2f} KB")
        print(f"Peak memory usage: {peak_memory / 1024:.2f} KB")
        return None
