from time import time
import re
from collections import Counter
from math import prod


def extract_numbers(line):
    """Extract integers from a given line of text."""
    return list(map(int, re.findall(r"[-+]?\d+", line)))


def update_positions(x_positions, y_positions, velocities_x, velocities_y, width, height):
    """Update positions based on velocities, wrapping around the grid edges."""
    for i in range(len(x_positions)):
        x_positions[i] = (x_positions[i] + velocities_x[i]) % width
        y_positions[i] = (y_positions[i] + velocities_y[i]) % height


def check_christmas_tree(robot_positions):
    """Check if the robots form a Christmas tree pattern."""
    adjacent_tree_count = 0
    for (row, col) in robot_positions:
        if (
            (row + 1, col) in robot_positions and
            (row - 1, col) in robot_positions and
            (row, col + 1) in robot_positions and
            (row, col - 1) in robot_positions
        ):
            adjacent_tree_count += 1
            if adjacent_tree_count >= 10:
                return True
    return False


def display_tree(x_positions, y_positions, width, height):
    """Visualize the tree """
    grid = [["."] * width for _ in range(height)]
    for x, y in zip(x_positions, y_positions):
        grid[y][x] = "X"
    for row in grid:
        print("".join(row))


# Starting to solve
time_start = time()
INPUT_FILE = "day14_input.txt"
data = [line.rstrip("\n") for line in open(INPUT_FILE, "r")]

grid_width, grid_height = 101, 103
robot_count = len(data)
initial_x_positions, initial_y_positions, velocities_x, velocities_y = [], [], [], []

# Parse input
for line in data:
    start_x, start_y, vel_x, vel_y = extract_numbers(line)
    initial_x_positions.append(start_x)
    initial_y_positions.append(start_y)
    velocities_x.append(vel_x)
    velocities_y.append(vel_y)

# Part 1
current_x_positions = initial_x_positions.copy()
current_y_positions = initial_y_positions.copy()
for _ in range(100):
    update_positions(current_x_positions, current_y_positions, velocities_x, velocities_y, grid_width, grid_height)

quadrant_robot_counts = Counter()
for i in range(robot_count):
    if current_x_positions[i] != grid_width // 2 and current_y_positions[i] != grid_height // 2:
        quadrant_key = (
            0 if current_x_positions[i] < grid_width // 2 else 1,
            0 if current_y_positions[i] < grid_height // 2 else 1,
        )
        quadrant_robot_counts[quadrant_key] += 1

safety_factor = prod(quadrant_robot_counts.values())
print(f"Part 1: {safety_factor}  ({time() - time_start:.3f}s)")

# Part 2: Find time to form Christmas tree pattern
current_x_positions = initial_x_positions.copy()
current_y_positions = initial_y_positions.copy()
elapsed_seconds = 0
while True:
    elapsed_seconds += 1
    update_positions(current_x_positions, current_y_positions, velocities_x, velocities_y, grid_width, grid_height)
    robot_positions = {(current_x_positions[i], current_y_positions[i]) for i in range(robot_count)}
    if check_christmas_tree(robot_positions):
        # Displaying the grid for our advent cheer
        display_tree(current_x_positions, current_y_positions, grid_width, grid_height)
        break

print(f"Part 2: {elapsed_seconds}  ({time() - time_start:.3f}s)")
