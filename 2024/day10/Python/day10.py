from time import time

# Starting timer
time_start = time()

# Input file and read the map
INPUT_FILE = "day10_input.txt"
topo_map = [list(map(int, line.strip())) for line in open(INPUT_FILE, "r")]
rows, cols = len(topo_map), len(topo_map[0])

# Data structures
reachable_positions = [[set() for _ in range(cols)] for _ in range(rows)]
trail_count = [[0 for _ in range(cols)] for _ in range(rows)]

# Results for part 1 (scores) and part 2 (ratings)
total_score, total_rating = 0, 0

# Traverse height levels from highest (9) to lowest (0)
for height in range(9, -1, -1):
    for row in range(rows):
        for col in range(cols):
            # Skip cells that doesnt match current height
            if topo_map[row][col] != height:
                continue

            # Base case
            if topo_map[row][col] == 9:
                reachable_positions[row][col] = {(row, col)}
                trail_count[row][col] = 1
            else:
                for neighbor_row, neighbor_col in [
                    (row + 1, col), (row - 1, col),
                    (row, col + 1), (row, col - 1)
                ]:
                    if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                        if topo_map[neighbor_row][neighbor_col] == topo_map[row][col] + 1:
                            reachable_positions[row][col] |= reachable_positions[neighbor_row][neighbor_col]
                            trail_count[row][col] += trail_count[neighbor_row][neighbor_col]

            # Updating if trailhead (=0)
            if topo_map[row][col] == 0:
                total_score += len(reachable_positions[row][col])
                total_rating += trail_count[row][col]

# Results
print(f"Part 1 (Total Score): {total_score}  ({time() - time_start:.3f}s)")
print(f"Part 2 (Total Rating): {total_rating}  ({time() - time_start:.3f}s)")
