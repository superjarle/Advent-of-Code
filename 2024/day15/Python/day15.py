from time import time
from collections import deque

# Start the timer
start_time = time()

# Input file and data processing
INPUT_FILE = "day15_input.txt"
raw_data = open(INPUT_FILE, "r").read().strip()
maze_map, path_directions = raw_data.split("\n\n")
maze = [list(row) for row in maze_map.splitlines()]

# Function to expand the maze for part 2
def double_the_fun(maze):
    rows, cols = len(maze), len(maze[0])
    expanded_maze = []
    for row in range(rows):
        extended_row = []
        for col in range(cols):
            if maze[row][col] == '#':
                extended_row.extend(['#', '#'])  # Wall stays solid!
            elif maze[row][col] == 'O':
                extended_row.extend(['[', ']'])  # Add a portal
            elif maze[row][col] == '.':
                extended_row.extend(['.', '.'])  # Open path remains open
            elif maze[row][col] == '@':
                extended_row.extend(['@', '.'])  # Start gets extra space
        expanded_maze.append(extended_row)
    return expanded_maze

# Function to find the starting position
def find_starting_spot(maze):
    for row_idx in range(len(maze)):
        for col_idx in range(len(maze[0])):
            if maze[row_idx][col_idx] == '@':
                maze[row_idx][col_idx] = '.'  # Mark start as visited
                return row_idx, col_idx
    raise ValueError("No starting spot '@' found in the maze!")

# Function to navigate those path directons and calculate the score
def navigate_and_score(maze, path_directions):
    rows, cols = len(maze), len(maze[0])
    player_row, player_col = find_starting_spot(maze)
    path_directions = path_directions.replace('\n', '')
    moves = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}

    for step in path_directions:
        dr, dc = moves[step]
        new_row, new_col = player_row + dr, player_col + dc
        if maze[new_row][new_col] == '#':  # Wall blocks the way
            continue
        elif maze[new_row][new_col] == '.':  # Move to open path
            player_row, player_col = new_row, new_col
        elif maze[new_row][new_col] in ['[', ']', 'O']:  # Handle portals
            if handle_portal_challenge(maze, player_row, player_col, dr, dc):
                player_row, player_col = new_row, new_col

    # Find total score
    total_score = sum(
        100 * row + col
        for row in range(rows)
        for col in range(cols)
        if maze[row][col] in ['[', 'O']
    )
    return total_score

# Handling those portal challenges
def handle_portal_challenge(maze, row, col, dr, dc):
    queue = deque([(row, col)])
    visited = set()
    is_path_clear = True

    while queue:
        curr_row, curr_col = queue.popleft()
        if (curr_row, curr_col) in visited:
            continue
        visited.add((curr_row, curr_col))
        next_row, next_col = curr_row + dr, curr_col + dc

        if maze[next_row][next_col] == '#':
            is_path_clear = False
            break
        if maze[next_row][next_col] == 'O':
            queue.append((next_row, next_col))
        if maze[next_row][next_col] == '[':
            queue.append((next_row, next_col))
            assert maze[next_row][next_col + 1] == ']'
            queue.append((next_row, next_col + 1))
        if maze[next_row][next_col] == ']':
            queue.append((next_row, next_col))
            assert maze[next_row][next_col - 1] == '['
            queue.append((next_row, next_col - 1))

    if not is_path_clear:
        return False

    while visited:
        for curr_row, curr_col in sorted(visited):
            next_row, next_col = curr_row + dr, curr_col + dc
            if (next_row, next_col) not in visited:
                assert maze[next_row][next_col] == '.'
                maze[next_row][next_col] = maze[curr_row][curr_col]
                maze[curr_row][curr_col] = '.'
                visited.remove((curr_row, curr_col))
    return True

# Solving and printing
part1_score = navigate_and_score([row[:] for row in maze], path_directions)
expanded_maze = double_the_fun([row[:] for row in maze])
part2_score = navigate_and_score(expanded_maze, path_directions)
print(f"Part 1 Score: {part1_score}  ({time() - start_time:.3f}s)")
print(f"Part 2 Score: {part2_score}  ({time() - start_time:.3f}s)")
