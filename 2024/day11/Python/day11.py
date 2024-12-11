from time import time
from functools import cache

# Start the timer
start_time = time()

# Input data
INPUT_FILE = "day11_input.txt"
input_lines = [line.rstrip("\n") for line in open(INPUT_FILE, "r")]


@cache
def count_stones_after_blinks(stone_value, remaining_blinks):
    ### Recursively calculate the number of stones after a given number of blinks.
    if remaining_blinks == 0:
        return 1  # Each stone is counted as one when no more blinks remain

    # Rule 1: Replace stone engraved with 0
    if stone_value == 0:
        return count_stones_after_blinks(1, remaining_blinks - 1)

    # Rule 2: If the number has an even number of digits, split into two stones
    stone_digits = str(stone_value)
    num_digits = len(stone_digits)
    if num_digits % 2 == 0:
        half_length = num_digits // 2
        left_part = int(stone_digits[:half_length])
        right_part = int(stone_digits[half_length:])
        return (count_stones_after_blinks(left_part, remaining_blinks - 1) +
                count_stones_after_blinks(right_part, remaining_blinks - 1))

    # Rule 3: Multiply by 2024 if no other rule applies
    new_stone_value = stone_value * 2024
    return count_stones_after_blinks(new_stone_value, remaining_blinks - 1)


# Parse the initial numbers engraved on stones from the input file
initial_stones = list(map(int, input_lines[0].split()))

# Part 1: 25 blinks
part1 = sum(count_stones_after_blinks(stone, 25) for stone in initial_stones)
print(f"Part 1: {part1}  ({time() - start_time:.3f}s)")

# Part 2: 75 blinks
part2 = sum(count_stones_after_blinks(stone, 75) for stone in initial_stones)
print(f"Part 2: {part2}  ({time() - start_time:.3f}s)")
