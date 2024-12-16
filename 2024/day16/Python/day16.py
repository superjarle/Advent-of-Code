from time import time
from collections import defaultdict
from heapq import heappop, heappush

# Start the timer
start_time = time()

# Input file and data processing
INPUT_FILE = "day16_input.txt"
reindeer_maze = [list(line.rstrip("\n")) for line in open(INPUT_FILE, "r")]
rows, cols = len(reindeer_maze), len(reindeer_maze[0])

# Constants
INFINITY = 1 << 31
min_cost = INFINITY

# Locate the start and end points
start_row, start_col, end_row, end_col = 0, 0, 0, 0
start_direction_row, start_direction_col = 0, 1

for row in range(rows):
    for col in range(cols):
        if reindeer_maze[row][col] == "S":
            start_row, start_col = row, col
        if reindeer_maze[row][col] == "E":
            end_row, end_col = row, col

# Default distances and previous states
distances = defaultdict(lambda: INFINITY)
distances[start_row, start_col, start_direction_row, start_direction_col] = 0
previous_steps = defaultdict(set)
priority_queue = [(0, start_row, start_col, start_direction_row, start_direction_col)]

# Movement logic
while priority_queue:
    current_cost, current_row, current_col, dir_row, dir_col = heappop(priority_queue)

    if current_cost > distances[current_row, current_col, dir_row, dir_col]:
        continue

    if current_cost > min_cost:
        break

    if current_row == end_row and current_col == end_col:
        min_cost = current_cost

    # Explore possible moves
    for next_row, next_col, next_dir_row, next_dir_col, move_cost in [
        (current_row + dir_row, current_col + dir_col, dir_row, dir_col, 1),  # Move forward
        (current_row, current_col, dir_col, -dir_row, 1000),  # Rotate clockwise
        (current_row, current_col, -dir_col, dir_row, 1000),  # Rotate counterclockwise
    ]:
        if reindeer_maze[next_row][next_col] != "#":  # Check for walls
            next_distance = distances[next_row, next_col, next_dir_row, next_dir_col]
            if current_cost + move_cost < next_distance:
                heappush(priority_queue, (current_cost + move_cost, next_row, next_col, next_dir_row, next_dir_col))
                distances[next_row, next_col, next_dir_row, next_dir_col] = current_cost + move_cost
                previous_steps[next_row, next_col, next_dir_row, next_dir_col] = {
                    (current_row, current_col, dir_row, dir_col)
                }
            elif current_cost + move_cost == next_distance:
                previous_steps[next_row, next_col, next_dir_row, next_dir_col].add(
                    (current_row, current_col, dir_row, dir_col)
                )

# Part 1 result
print(f"Part 1: {min_cost}  ({time() - start_time:.3f}s)")

# Part 2: Find all best path tiles
visited_positions = {
    (end_row, end_col, 1, 0),
    (end_row, end_col, 0, 1),
    (end_row, end_col, -1, 0),
    (end_row, end_col, 0, -1),
}
backtrack_queue = [
    (end_row, end_col, 1, 0),
    (end_row, end_col, 0, 1),
    (end_row, end_col, -1, 0),
    (end_row, end_col, 0, -1),
]

while backtrack_queue:
    current_row, current_col, dir_row, dir_col = backtrack_queue.pop()
    for previous_row, previous_col, previous_dir_row, previous_dir_col in previous_steps[
        current_row, current_col, dir_row, dir_col
    ]:
        if (previous_row, previous_col, previous_dir_row, previous_dir_col) not in visited_positions:
            visited_positions.add((previous_row, previous_col, previous_dir_row, previous_dir_col))
            backtrack_queue.append((previous_row, previous_col, previous_dir_row, previous_dir_col))

# Solve part 2
best_path_tiles = len({(row, col) for row, col, _, _ in visited_positions})
print(f"Part 2: {best_path_tiles}  ({time() - start_time:.3f}s)")