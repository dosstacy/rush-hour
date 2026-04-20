# Rush Hour Puzzle Game

An interactive "Rush Hour" puzzle game implemented in Python with a graphical interface based on Tkinter. The game allows players to move cars on a board so that the main car can escape from the traffic jam.

## Game Description

In the "Rush Hour" game, the player must move various cars on a 6×6 grid to free the main car (car "A"), which needs to reach the exit. Each car can only move horizontally or vertically depending on its orientation.

## Features

- 🎮 **Interactive GUI** - Play on the board using mouse and keyboard
- 🤖 **Multiple Solving Algorithms**:
  - A* Search - optimal search with heuristic
  - Depth-First Search (DFS) - depth-first search
  - Greedy Search - greedy search
- 📊 **10 Difficulty Levels** - from simple to complex puzzles
- 📈 **Analytics** - tracking moves, solving time, and comparing algorithms

## Project Structure

```
rush-hour/
├── main.py                    # Program entry point
├── constants.py               # Global constants (directions, exit position)
├── elements/
│   ├── Board.py              # Class for managing board and cars
│   └── Car.py                # Class for representing a car
├── algorithms/
│   ├── a_star.py             # A* algorithm implementation
│   ├── dfs.py                # DFS algorithm implementation
│   ├── greedy_search.py      # Greedy search implementation
│   └── additional_logic.py   # Helper logic for algorithms
├── gui/
│   ├── main_menu.py          # Main game menu
│   ├── level_menu.py         # Level selection menu
│   ├── game_board.py         # Game board visualization
│   └── game_controller.py    # Main game controller
├── levels/                    # Level configuration files (level1.txt - level10.txt)
└── images/                    # Graphics resources (if any)
```

## Requirements

- Python 3.7 or higher
- tkinter (usually included in the standard Python library)

## Installation and Running

### 1. Clone the Repository

```bash
git clone <repository-url>
cd rush-hour
```

### 2. Run the Game

```bash
python main.py
```

This will launch the main game menu with a graphical interface.

## How to Play

1. **Select a Level** - choose one of 10 available difficulty levels
2. **Move Cars** - click on a car and drag it in the desired direction
3. **Goal** - move car "A" to position (2, 5) to escape from the traffic jam
4. **Hints** - use one of three available solving algorithms to get a solution

## Solving Algorithms

The game implements three common search algorithms:

### A* Search
- **Description**: Informed search that uses a heuristic to estimate the best path
- **Advantages**: Optimal number of moves, efficient performance
- **File**: `algorithms/a_star.py`

### Depth-First Search (DFS)
- **Description**: Uninformed search that goes as deep as possible before backtracking
- **Advantages**: Simple implementation, uses minimal memory
- **File**: `algorithms/dfs.py`

### Greedy Search
- **Description**: Informed search that always selects the most promising state based on heuristic
- **Advantages**: Quickly finds a solution
- **File**: `algorithms/greedy_search.py`
