from time import time
from collections import deque

time_start = time()

INFINITY = float('inf')  # Santa's bag of infinite gifts
INPUT_FILE = "day20_input.txt" # input

def load_racetrack(file_path):
    with open(file_path, "r") as f:
        return [list(line.strip()) for line in f]

def find_position(grid, target):
    for row, line in enumerate(grid):
        for col, char in enumerate(line):
            if char == target:
                return row, col
    return -1, -1

def calculate_distances(grid, start_row, start_col):
    rows, cols = len(grid), len(grid[0])
    distances = [[INFINITY] * cols for _ in range(rows)]
    distances[start_row][start_col] = 0
    queue = deque([(start_row, start_col)])

    while queue:
        r, c = queue.popleft()
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#" and distances[nr][nc] == INFINITY:
                distances[nr][nc] = distances[r][c] + 1
                queue.append((nr, nc))

    return distances

def count_holiday_cheats(grid, max_cheat_distance, min_time_saved, no_cheats, dist_start, dist_end):
    cheat_count = 0
    rows, cols = len(grid), len(grid[0])

    # Trying to avoid repeat calculations
    cheat_ranges = {}
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "#":
                cheat_ranges[(r, c)] = [
                    (rn, cn)
                    for rn in range(max(0, r - max_cheat_distance), min(rows, r + max_cheat_distance + 1))
                    for cn in range(max(0, c - (max_cheat_distance - abs(r - rn))), min(cols, c + (max_cheat_distance - abs(r - rn)) + 1))
                    if grid[rn][cn] != "#"
                ]

    for (r, c), valid_cheats in cheat_ranges.items():
        for cheat_r, cheat_c in valid_cheats:
            cheat_step = abs(r - cheat_r) + abs(c - cheat_c)
            total_time = dist_start[r][c] + cheat_step + dist_end[cheat_r][cheat_c]

            if total_time <= no_cheats - min_time_saved:
                cheat_count += 1

    return cheat_count

# Load the map and find positions
racetrack = load_racetrack(INPUT_FILE)
rows, cols = len(racetrack), len(racetrack[0])
start_row, start_col = find_position(racetrack, "S")
end_row, end_col = find_position(racetrack, "E")

# Calculate distances
distances_from_start = calculate_distances(racetrack, start_row, start_col)
distances_to_end = calculate_distances(racetrack, end_row, end_col)

# Without cheats
without_cheats = distances_from_start[end_row][end_col]

# Part 1: Festive cheating
part_1_cheats = count_holiday_cheats(
    racetrack, max_cheat_distance=2, min_time_saved=100, no_cheats=without_cheats,
    dist_start=distances_from_start, dist_end=distances_to_end
)
print(f"Part 1: {part_1_cheats} cheats found ({time() - time_start:.3f}s)")

# Part 2: Santa's updated cheat policy
part_2_cheats = count_holiday_cheats(
    racetrack, max_cheat_distance=20, min_time_saved=100, no_cheats=without_cheats,
    dist_start=distances_from_start, dist_end=distances_to_end
)
print(f"Part 2: {part_2_cheats} cheats found ({time() - time_start:.3f}s)")
