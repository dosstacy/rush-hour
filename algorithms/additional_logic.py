from constants import WIN_X, WIN_Y, MAIN_CAR

def heuristic(state):
    car = state.cars.get(MAIN_CAR)
    if car:
        target_row, target_col = WIN_X, WIN_Y
        blocking_cars = 0

        for col in range(car.positions[0][1] + 1, target_col + 1):
            if state.grid[car.positions[0][0]][col] != ".":
                blocking_cars += 1

        return abs(car.positions[0][1] - target_col) + blocking_cars
    return float('inf')

def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        current, action = came_from[current]
        path.append(action)
    return path[::-1]