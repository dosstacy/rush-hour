from elements.Board import Board

class Dfs:
        def __init__(self, board):
            self.board = board

        def solve(self):
            stack = [(self.board, [])]
            visited = set()

            while stack:
                current, path = stack.pop()

                state_key = current.board_to_key()
                if state_key in visited:
                    continue
                visited.add(state_key)

                if Board.is_win_position(current):
                    return path

                for neighbor, action in Board.get_neighbors(current):
                    stack.append((neighbor, path + [action]))

            print("No solution found!")
            return None