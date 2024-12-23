# Constants
DIRECTIONS = [1, -1, 1j, -1j, 1+1j, 1-1j, -1+1j, -1-1j]  # Part 1
DIAGONAL_PAIRS = [((-1-1j), (1+1j)), ((1+1j), (-1-1j)), 
                  ((-1+1j), (1-1j)), ((1-1j), (-1+1j))]  # Part 2

# Functions
def extract_word_in_direction(position, direction, length):
    word = ""
    for step in range(length):
        current_position = position + step * direction
        if current_position not in grid:
            return False
        word += grid[current_position]
    return word

def is_xmas_shape(position):
    if grid[position] != "A":
        return False
    
    found_pairs = 0
    for dir1, dir2 in DIAGONAL_PAIRS:
        start_pos = position + dir1
        if start_pos in grid and extract_word_in_direction(start_pos, dir2, 3) == "MAS":
            found_pairs += 1
            if found_pairs == 2:  # Early exit if two valid pairs are found
                return True
    return False

# Parse Input
with open("day4_input.txt") as f:
    inp = f.read().strip().split("\n")
grid = {j + i * 1j: inp[i][j] for i in range(len(inp)) for j in range(len(inp[0]))}

# Search
x_positions = [pos for pos in grid if grid[pos] == "X"]  # Starting positions for "XMAS"
a_positions = [pos for pos in grid if grid[pos] == "A"]  # Centers for "X-MAS"

# Part 1: 
xmas_count = sum(
    extract_word_in_direction(pos, direction, 4) == "XMAS"
    for pos in x_positions 
    for direction in DIRECTIONS
)
print(f"Part 1: Number of XMAS occurrences: {xmas_count}")

# Part 2:
xmas_shape_count = sum(is_xmas_shape(pos) for pos in a_positions)
print(f"Part 2: Number of X-MAS shapes: {xmas_shape_count}")
