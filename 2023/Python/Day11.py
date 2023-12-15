import numpy as np
from sys import exit
import grid

class GalaxyGrid:
    def __init__(self, values):
        self.grid = grid.Grid.from_text(values)
        self.empty_cols = self.find_empty_cols()
        self.empty_rows = self.find_empty_rows()
        self.stars = self.find_stars()

    def find_empty_cols(self):
        empty_cols = []
        for x in self.grid.x_range():
            if sum(0 if self.grid[x, y] == "." else 1 for y in self.grid.y_range()) == 0:
                empty_cols.append(x)
        return empty_cols

    def find_empty_rows(self):
        empty_rows = []
        for y in self.grid.y_range():
            if sum(0 if self.grid[x, y] == "." else 1 for x in self.grid.x_range()) == 0:
                empty_rows.append(y)
        return empty_rows

    def find_stars(self):
        stars = []
        for (x, y), val in self.grid.grid.items():
            if val == "#":
                stars.append((x, y))
        return stars

class CosmicCalculator:
    def __init__(self, galaxy_grid):
        self.galaxy_grid = galaxy_grid

    def calculate_distance(self, mode):
        ret = 0
        stars = self.galaxy_grid.stars
        empty_cols = self.galaxy_grid.empty_cols
        empty_rows = self.galaxy_grid.empty_rows

        for i in range(len(stars)):
            for j in range(i + 1, len(stars)):
                ax, ay = stars[i]
                bx, by = stars[j]

                ax, bx = min(ax, bx), max(ax, bx)
                ay, by = min(ay, by), max(ay, by)

                count = self.calculate_path(ax, bx, ay, by, empty_cols, empty_rows, mode)
                ret += count
        return ret

    def calculate_path(self, ax, bx, ay, by, empty_cols, empty_rows, mode):
        count = 0
        count -= 1
        for x in range(ax, bx + 1):
            if x in empty_cols:
                count += 1 if mode == 1 else (1000000 - 1)
            count += 1
        count -= 1
        for y in range(ay, by + 1):
            if y in empty_rows:
                count += 1 if mode == 1 else (1000000 - 1)
            count += 1
        return count

if __name__ == "__main__":
    import os
    puzzleinput = "day11.txt"
    with open(puzzleinput) as f:
        values = [line.strip() for line in f.readlines()]
        galaxy_grid = GalaxyGrid(values)
    cosmic_calculator = CosmicCalculator(galaxy_grid)
    print(cosmic_calculator.calculate_distance(1))  # Part 1
    print(cosmic_calculator.calculate_distance(2))  # Part 2