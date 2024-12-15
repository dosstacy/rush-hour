import time
import tracemalloc
from elements.Board import Board

class Dfs:
    def __init__(self, board):
        self.board = board

    def solve(self):
        start_time = time.time()
        tracemalloc.start()

        stack = [(self.board, [])]
        visited = set()
        steps = 0

        while stack:
            current, path = stack.pop()
            steps += 1

            state_key = current.board_to_key()
            if state_key in visited:
                continue
            visited.add(state_key)

            if Board.is_win_position(current):
                end_time = time.time()
                current_memory, peak_memory = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                print("Solution found!")
                print(f"Time taken: {end_time - start_time:.2f} seconds")
                print(f"Steps taken: {steps}")
                print(f"Visited states: {len(visited)}")
                print(f"Current memory usage: {current_memory / 1024:.2f} KB")
                print(f"Peak memory usage: {peak_memory / 1024:.2f} KB")
                print(f"Solution path length: {len(path)}")
                return path

            for neighbor, action in Board.get_neighbors(current):
                stack.append((neighbor, path + [action]))

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
