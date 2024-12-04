DIRECTIONS = {
    "up": (-1, 0),
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1)
}

WIN_X = 2
WIN_Y = 5

def get_displacement(direction):
    return DIRECTIONS.get(direction, (0, 0))

def is_win_position(state):
    car = state.cars.get("A")
    if car and (WIN_X, WIN_Y) in car.positions:
        return True
    return False

def is_within_bounds(positions, grid_size):
    return all(0 <= x < grid_size and 0 <= y < grid_size for x, y in positions)

def is_valid_position(grid, positions, car_name):
    for x, y in positions:
        if grid[x][y] not in (".", car_name):
            return False
    return True
