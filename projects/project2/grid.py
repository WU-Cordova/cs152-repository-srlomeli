from __future__ import annotations
from projects.project2.cell import Cell
from datastructures.array2d import Array2D
import random

class Grid:
    def __init__(self, rows: int = 10, cols: int = 10):
        self.grid: Array2D[Cell] = Array2D.empty(rows, cols, data_type=Cell)
        self.rows = rows
        self.cols = cols

        for row in range(rows):
            for col in range(cols):
                self.grid[row][col] = Cell(random.choice([True, False]))

    def random_start(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col].is_alive = random.choice([True, False])

    def read_config(self, filename: str):
        with open(filename, 'r') as file:
            lines = file.readlines()
            # Skip lines that start with a '#' (comments)
            lines = [line.strip() for line in lines if not line.strip().startswith('#')]
            self.rows = int(lines[0])
            self.cols = int(lines[1])
            self.grid = Array2D.empty(self.rows, self.cols, data_type=Cell)

            for row in range(self.rows):
                for col, char in enumerate(lines[row + 2]):  # Start reading from line 3
                    self.grid[row][col].is_alive = (char == 'X')

    def display(self) -> None:
        separator = '-' * (self.cols * 2 - 1)  # Separator line based on the number of columns
        print(separator)
        for row in range(self.rows):
            for col in range(self.cols):
                print('🦠' if self.grid[row][col].is_alive else ' ', end=" ")
            print()
        print(separator)

    def get_neighbors(self, row: int, col: int) -> int:
        count = 0
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),         (0, 1),
                      (1, -1),  (1, 0),  (1, 1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c].is_alive:
                count += 1

        return count

    def next_gen(self) -> Grid:
        next_grid = Grid(self.rows, self.cols)
        for row in range(self.rows):
            for col in range(self.cols):
                num_neighbors = self.get_neighbors(row, col)
                next_state = self.grid[row][col].next_state(num_neighbors)
                next_grid.grid[row][col].is_alive = next_state
        return next_grid

    def __eq__(self, value):
        if isinstance(value, Grid) and self.rows == value.rows and self.cols == value.cols:
            return self.grid == value.grid
        return False
