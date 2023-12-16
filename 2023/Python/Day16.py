
import time

file_path = 'input.txt'

with open(file_path, 'r') as file:
    puzzleinput = file.readlines()

start_tid = time.time()
def simulate_beampath(layout):
    # Reformatted layout as a single string and dimensions
    grid = ''.join(layout).replace('\n', '')
    rows, cols = len(layout), len(layout[0].strip())
    
    # Beam starting points: all edges of the grid
    beam_starts = []
    for i in range(rows):
        beam_starts.extend(((i, 0, 0), (i, cols - 1, 2)))
    for i in range(cols):
        beam_starts.extend(((0, i, 3), (rows - 1, i, 1)))
    
    # Directions: RIGHT, UP, LEFT, DOWN
    direction_moves = ((0, 1), (-1, 0), (0, -1), (1, 0))

    # Simulation function
    def lavafloor(beam_start):
        stack = [beam_start]
        energized_tiles = [0] * rows * cols
        visited_tiles = [0] * 4 * rows * cols

        while stack:
            row, col, dir = stack.pop()
            if 0 <= row < rows and 0 <= col < cols and visited_tiles[(index := 4 * row * cols + 4 * col + dir)] == 0:
                visited_tiles[index] = energized_tiles[index // 4] = 1
                tile = grid[index // 4]

                # Beam interactions
                if tile == '|' and dir % 2 == 0:
                    stack.extend([(row - 1, col, 1), (row + 1, col, 3)])
                elif tile == '-' and dir % 2 == 1:
                    stack.extend([(row, col - 1, 2), (row, col + 1, 0)])
                elif tile in ['\\', '/']:
                    new_dir = dir ^ (3 if tile == '\\' else 1)
                    dr, dc = direction_moves[new_dir]
                    stack.append((row + dr, col + dc, new_dir))
                else:
                    dr, dc = direction_moves[dir]
                    stack.append((row + dr, col + dc, dir))

        return sum(energized_tiles)

    # Part 1: Starting from top-left corner
    part1 = lavafloor((0, 0, 0))
    
    # Part 2: Max energized tiles from any starting point
    part2 = max(map(lavafloor, beam_starts))
    slutt_tid = time.time()
    totaltid = (slutt_tid - start_tid) * 1000
    
    return part1, part2, totaltid

# Simulate the beam path 
del1, del2, totaltid = simulate_beampath(puzzleinput)
print(f"Svaret for del 1 er: {del1}")
print(f"Svaret for del 2 er: {del2}")
print(f"Tiden det tok er: {totaltid:.2f} millisekunder")
