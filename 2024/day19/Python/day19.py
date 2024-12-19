from time import time
from functools import cache

time_start = time()

#Input
INPUT_FILE = "day19_input.txt"
blocks = [block.splitlines() for block in open(INPUT_FILE, "r").read().split("\n\n")]

available_towel_patterns = list(blocks[0][0].split(", "))

# Memoized function to count the number of ways to decompose the designs
@cache
def count_ways(designs):
    if not designs:
        return 1
    return sum(count_ways(designs[len(p):]) for p in available_towel_patterns if designs.startswith(p))

#solving
solution1, solution2 = 0, 0
for designs in blocks[1]:
    solution1 += 1 if count_ways(designs) else 0
    solution2 += count_ways(designs)

#printing solutions
print(f"Part 1: {solution1}  ({time() - time_start:.3f}s)")
print(f"Part 2: {solution2}  ({time() - time_start:.3f}s)")