import math
from time import time as perf_counter
from collections import defaultdict

# Constants
SHAPE_WIDTH = 7
PATTERN_LENGTH = 2022
TOTAL_ROCKS = 1000000000000

class TetrisSimulator:
    def __init__(self, pattern):
        self.data = set()
        self.top = 0
        self.current_shape_idx = 0
        self.shape_x = 2
        self.shape_y = 3
        self.settled = 0
        self.pattern = pattern
        self.pat_idx = 0

    def can_move_horizontal(self, direction):
        """
        Checks if the current shape can move horizontally in the given direction.
        """
        nx = self.shape_x + (-1 if direction == "<" else 1)

        if nx in [-1, SHAPE_WIDTH]:
            return False

        for y, l in enumerate(shapes[self.current_shape_idx]):
            for x, c in enumerate(l):
                if c == "#" and ((nx + x, self.shape_y + y) in self.data or nx + x >= SHAPE_WIDTH):
                    return False
        return True

    def can_move_down(self):
        """
        Checks if the current shape can move down.
        """
        ny = self.shape_y - 1

        if ny < 0:
            return False

        for y, l in enumerate(shapes[self.current_shape_idx]):
            for x, c in enumerate(l):
                if c == "#" and (self.shape_x + x, ny + y) in self.data:
                    return False
        return True

    def move(self):
        """
        Moves the shape according to the pattern.
        """
        direction = self.pattern[self.pat_idx % len(self.pattern)]
        self.pat_idx += 1

        if self.can_move_horizontal(direction):
            self.shape_x += -1 if direction == "<" else 1

        if self.can_move_down():
            self.shape_y -= 1
        else:
            return True

        return False

    def drop(self):
        """
        Drops the shape until it can't move down further.
        """
        while not self.move():
            pass
        self.draw()

    def get_top(self):
        """
        Returns the highest y-coordinate occupied by a block.
        """
        return max(c[1] for c in self.data)

    def draw(self):
        """
        Draws the current shape onto the grid.
        """
        for y, l in enumerate(shapes[self.current_shape_idx]):
            for x, c in enumerate(l):
                if c == "#":
                    self.data.add((self.shape_x + x, self.shape_y + y))

        self.settled += 1
        self.top = self.get_top()
        self.current_shape_idx = (self.current_shape_idx + 1) % len(shapes)
        self.shape_x = 2
        self.shape_y = self.top + 4

    def plot(self):
        """
        Plots the current state of the grid.
        """
        buff = []
        for y in range(100):
            st = "".join("#" if (x, y) in self.data else "." for x in range(SHAPE_WIDTH))
            buff.append(st)

        print("\n".join(buff[::-1]))

    def find_pattern(self):
        """
        Finds and returns the repeating pattern in the grid.
        """
        states = defaultdict(list)
        heights = {}

        while True:
            self.drop()
            top = self.get_top()

            heights[self.settled] = top + 1

            if all((x, top) in self.data for x in range(SHAPE_WIDTH)):
                s = (self.pat_idx % len(self.pattern), self.current_shape_idx)
                states[s].append(self.settled)
                if len(states[s]) == 2:
                    return states[s], heights


def profiler(method):
    """
    A decorator to measure the execution time of methods.
    """
    def wrapper_method(*args, **kwargs):
        t = perf_counter()
        ret = method(*args, **kwargs)
        print(f'Method {method.__name__} took : {perf_counter()-t:2.5f} sec')
        return ret
    return wrapper_method


@profiler
def part1():
    g = TetrisSimulator(open("input.txt").read())

    for _ in range(PATTERN_LENGTH):
        g.drop()

    print(g.get_top() + 1)


@profiler
def part2():
    g = TetrisSimulator(open("input.txt").read())

    pt, heights = g.find_pattern()

    extra_rocks = (TOTAL_ROCKS - max(pt)) % (max(pt) - min(pt))
    extra_height = heights[min(pt) + extra_rocks] - heights[min(pt)]

    cycles = (TOTAL_ROCKS - min(pt)) // (max(pt) - min(pt))
    cycle_height = heights[max(pt)] - heights[min(pt)]

    initial_height = heights[min(pt)]

    print(initial_height + cycles * cycle_height + extra_height)


if __name__ == "__main__":
    part1()
    part2()
