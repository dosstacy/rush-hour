from utils import is_win_position, get_neighbors

class RushHourSolverDFS:
        def __init__(self, board):
            self.initial_state = board

        def solve(self):
            stack = [(self.initial_state, [])]
            visited = set()

            while stack:
                current, path = stack.pop()

                state_key = current.board_to_key()
                if state_key in visited:
                    continue
                visited.add(state_key)

                if is_win_position(current):
                    return path

                for neighbor, action in get_neighbors(current):
                    stack.append((neighbor, path + [action]))

            print("No solution found!")
            return None