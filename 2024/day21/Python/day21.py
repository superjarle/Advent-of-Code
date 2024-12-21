import time
from functools import cache

# Start timer
time_start = time.time()

# Hardcoded keypads and input file
KEYPAD_1 = [
    "789",
    "456",
    "123",
    ".0A"
]

KEYPAD_2 = [
    ".^A",
    "<v>"
]

INPUT_FILE = "day21_input.txt"

# Function to load door codes from the file
def load_door_codes(file_path):
    with open(file_path, "r") as f:
        return f.read().strip().splitlines()

door_codes = load_door_codes(INPUT_FILE)

# Finding characters in the grid
def find_char(grid, ch):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == ch:
                return (i, j)

# Then finding the paths between
def find_paths(grid):
    def go(u, t, path, dist, res):
        if len(path) == dist:
            if u == t:
                res.append(path)
        else:
            i, j = u
            for ii, jj, d in ((i-1, j, '^'), (i+1, j, 'v'), (i, j-1, '<'), (i, j+1, '>')):
                if ii < 0 or ii >= len(grid) or jj < 0 or jj >= len(grid[0]): continue
                if grid[ii][jj] == '.': continue
                go((ii, jj), t, path + d, dist, res)

    s = ''.join(''.join(row) for row in grid).replace('.', '')
    res = {}
    for u in s:
        x = find_char(grid, u)
        for v in s:
            y = find_char(grid, v)
            dist = abs(x[0]-y[0]) + abs(x[1]-y[1])
            res[(u, v)] = []
            go(x, y, "", dist, res[(u, v)])
    return res

paths_1 = find_paths(KEYPAD_1)
paths_2 = find_paths(KEYPAD_2)

@cache
def calc_1(seq, levels, i=1):
    if i == len(seq): return 0
    return min(
        calc_2(0, levels, 'A' + s + 'A') + calc_1(seq, levels, i+1)
        for s in paths_1[(seq[i-1], seq[i])]
    )

@cache
def calc_2(level, levels, seq, i=1):
    if i == len(seq): return 0
    if level == levels: return len(seq) - i
    return min(
        calc_2(level+1, levels, 'A' + s + 'A') + calc_2(level, levels, seq, i+1)
        for s in paths_2[(seq[i-1], seq[i])]
    )

# Solving and printing solutions
print(
    sum(
        int(x[:-1]) * calc_1('A' + x, 2)
        for x in door_codes
    )
)
print(
    sum(
        int(x[:-1]) * calc_1('A' + x, 25)
        for x in door_codes
    )
)

# Timer end.
print(f"Execution time: {time.time() - time_start:.2f} seconds")
