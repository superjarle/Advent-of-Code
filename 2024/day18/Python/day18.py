from time import time

# Start the timer
start_time = time()

# Input file and data processing
INPUT_FILE = "day18_input.txt"
holiday_data = [line.rstrip("\n") for line in open(INPUT_FILE, "r")]

# Parse byte positions (Holiday Lights)
light_positions = [tuple(map(int, line.split(","))) for line in holiday_data]

# Grid dimensions for the holiday maze
ROWS, COLS = 71, 71
HOLIDAY_BYTE_LIMIT = 1024
start_row, start_col = 0, 0
end_row, end_col = ROWS - 1, COLS - 1

# Festive safety grid
safety_grid = [[1 << 31] * COLS for _ in range(ROWS)]
for t, (col, row) in enumerate(light_positions, start=1):
    safety_grid[row][col] = t

# BFS function for navigating the holiday maze
def navigate_holiday_maze(max_unsafe_level):
    queue = [(start_row, start_col, 0)]
    visited = [[False] * COLS for _ in range(ROWS)]
    visited[start_row][start_col] = True

    for row, col, time_step in queue:
        if row == end_row and col == end_col:
            return time_step

        for next_row, next_col in [(row - 1, col), (row + 1, col), (row, col + 1), (row, col - 1)]:
            if 0 <= next_row < ROWS and 0 <= next_col < COLS:
                if safety_grid[next_row][next_col] > max_unsafe_level and not visited[next_row][next_col]:
                    queue.append((next_row, next_col, time_step + 1))
                    visited[next_row][next_col] = True
    return -1

# Part 1: Holiday Escape
part1_result = navigate_holiday_maze(HOLIDAY_BYTE_LIMIT)
print(f"Part 1 (Holiday Escape): {part1_result}  ({time() - start_time:.3f}s)")

# Part 2: Brightest Holiday Lights
low, high = HOLIDAY_BYTE_LIMIT, len(light_positions)
while low + 1 < high:
    mid = (low + high) // 2
    result = navigate_holiday_maze(mid)
    if result == -1:
        high = mid
    else:
        low = mid

part2_result = ",".join(map(str, light_positions[high - 1]))
print(f"Part 2 (Brightest Lights): {part2_result}  ({time() - start_time:.3f}s)")