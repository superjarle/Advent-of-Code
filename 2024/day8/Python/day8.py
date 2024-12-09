from time import time
from collections import defaultdict
from math import gcd

time_start = time()

# Input stuff
INPUT_FILE = "day8_input.txt"
signal_map = [line.rstrip("\n") for line in open(INPUT_FILE, "r")]
antenna_grid = [list(line.rstrip("\n")) for line in open(INPUT_FILE, "r")]
rows, cols = len(antenna_grid), len(antenna_grid[0])

# Parse antenna locations
antennas_by_frequency = defaultdict(list)
for row in range(rows):
    for col in range(cols):
        if antenna_grid[row][col] != ".":
            antennas_by_frequency[antenna_grid[row][col]].append((row, col))

# Calculate antinodes
antinodes_resonant = set()
antinodes_harmonics = set()

for positions in antennas_by_frequency.values():
    num_antennas = len(positions)
    for i in range(num_antennas):
        for j in range(num_antennas):
            if i != j:
                # Get coordinates of two antennas
                r1, c1 = positions[i]
                r2, c2 = positions[j]
                dr = r1 - r2
                dc = c1 - c2

                # Part 1: Antinodes for resonant distances
                if 0 <= r1 + dr < rows and 0 <= c1 + dc < cols:
                    antinodes_resonant.add((r1 + dr, c1 + dc))

                # Normalize direction for Part 2
                g = gcd(dr, dc)
                dr //= g
                dc //= g

                # Part 2: Antinodes along the line of antennas
                k = 0
                while 0 <= r1 + k * dr < rows and 0 <= c1 + k * dc < cols:
                    antinodes_harmonics.add((r1 + k * dr, c1 + k * dc))
                    k += 1a

# Results
total_resonant_antinodes = len(antinodes_resonant)
total_harmonic_antinodes = len(antinodes_harmonics)

print(f"Part 1: {total_resonant_antinodes} ({time() - time_start:.4f}s)")
print(f"Part 2: {total_harmonic_antinodes} ({time() - time_start:.4f}s)")