from time import time
from collections import defaultdict

def calculate_region_properties(input_file):
    # Start the timer
    start_time = time()

    # Read and prepare grid data
    with open(input_file, "r") as file:
        grid_data = [line.strip() for line in file]
    rows, cols = len(grid_data), len(grid_data[0])

    # Initialize grid with a default value for out-of-bound checks
    grid = defaultdict(lambda: ".", {(r, c): value for r, row in enumerate(grid_data) for c, value in enumerate(row)})

    # Initialize results and visited set
    total_area_perimeter1 = 0
    total_area_perimeter2 = 0
    visited = set()

    # Process each cell
    for row in range(rows):
        for col in range(cols):
            if (row, col) in visited:
                continue

            # Initialize stack and region tracking
            stack = [(row, col)]
            visited.add((row, col))
            region = set(stack)

            # Explore the region using DFS
            while stack:
                current_row, current_col = stack.pop()
                for neighbor_row, neighbor_col in [
                    (current_row + 1, current_col),
                    (current_row - 1, current_col),
                    (current_row, current_col + 1),
                    (current_row, current_col - 1),
                ]:
                    if (
                        grid[neighbor_row, neighbor_col] == grid[current_row, current_col]
                        and (neighbor_row, neighbor_col) not in visited
                    ):
                        stack.append((neighbor_row, neighbor_col))
                        visited.add((neighbor_row, neighbor_col))
                        region.add((neighbor_row, neighbor_col))

            # Calculate area and perimeters
            area = len(region)

            # Perimeter type 1: Edges not in the region
            perimeter1 = sum(
                1
                for r, c in region
                for nr, nc in [
                    (r + 1, c), (r - 1, c),
                    (r, c + 1), (r, c - 1)
                ]
                if (nr, nc) not in region
            )

            # Perimeter type 2: More complex condition
            perimeter2 = 0
            for r, c in region:
                if (r, c - 1) not in region and (
                    (r - 1, c) not in region or (r - 1, c - 1) in region
                ):
                    perimeter2 += 1
                if (r, c + 1) not in region and (
                    (r - 1, c) not in region or (r - 1, c + 1) in region
                ):
                    perimeter2 += 1
                if (r - 1, c) not in region and (
                    (r, c - 1) not in region or (r - 1, c - 1) in region
                ):
                    perimeter2 += 1
                if (r + 1, c) not in region and (
                    (r, c - 1) not in region or (r + 1, c - 1) in region
                ):
                    perimeter2 += 1

            # Accumulate results
            total_area_perimeter1 += area * perimeter1
            total_area_perimeter2 += area * perimeter2

    # Print results
    elapsed_time = time() - start_time
    print(f"Part 1 (Total Area x Perimeter 1): {total_area_perimeter1} ({elapsed_time:.3f}s)")
    print(f"Part 2 (Total Area x Perimeter 2): {total_area_perimeter2} ({elapsed_time:.3f}s)")

# Input file path
INPUT_FILE = "day12_input.txt"
calculate_region_properties(INPUT_FILE)