from .Car import Car
class Board:
    def __init__(self, grid):
        self.grid = grid
        self.cars = self._parse_cars()
        self.grid_size = len(grid)

    def _parse_cars(self):
        cars = {}
        for row_idx, row in enumerate(self.grid):
            for col_idx, cell in enumerate(row):
                if cell != '.':
                    if cell not in cars:
                        cars[cell] = Car(cell)
                    cars[cell].add_position(row_idx, col_idx)
        return cars

    def is_valid_move(self, car, direction):
        dx, dy = 0, 0
        if direction == "up" and car.orientation == "vertical":
            dx = -1
        elif direction == "down" and car.orientation == "vertical":
            dx = 1
        elif direction == "left" and car.orientation == "horizontal":
            dy = -1
        elif direction == "right" and car.orientation == "horizontal":
            dy = 1
        else:
            return False

        new_positions = [(x + dx, y + dy) for x, y in car.positions]

        if not all(0 <= x < len(self.grid) and 0 <= y < len(self.grid[0]) for x, y in new_positions):
            return False

        for x, y in new_positions:
            if self.grid[x][y] != "." and self.grid[x][y] != car.name:
                return False

        return True

    def move_car(self, car, direction):
        dx, dy = 0, 0
        if direction == "up":
            dx = -1
        elif direction == "down":
            dx = 1
        elif direction == "left":
            dy = -1
        elif direction == "right":
            dy = 1

        for x, y in car.positions:
            self.grid[x][y] = "."

        car.positions = [(x + dx, y + dy) for x, y in car.positions]

        for x, y in car.positions:
            self.grid[x][y] = car.name

    @staticmethod
    def init_board(file):
        grid = []
        with open(file, 'r') as f:
            for line in f:
                grid.append(line.strip().split())
        return grid

    def copy(self):
        new_board = Board([row[:] for row in self.grid])
        new_board.cars = {car_name: Car(car_name) for car_name in self.cars}
        for car_name, car in self.cars.items():
            new_car = new_board.cars[car_name]
            new_car.positions = car.positions[:]
            new_car.orientation = car.orientation
        return new_board

    def board_to_key(self):
        return ''.join(''.join(row) for row in self.grid)

    def __hash__(self):
        """Генерує хеш для стану дошки."""
        return hash(tuple(tuple(row) for row in self.grid))  # Унікальне представлення стану

    def __eq__(self, other):
        """Перевіряє еквівалентність двох станів."""
        if not isinstance(other, Board):
            return False
        return self.grid == other.grid
