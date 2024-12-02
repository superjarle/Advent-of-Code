# -*- coding: utf-8 -*-
"""
@author: jkv
"""

def is_save(level):
    """
    Check if a level is safe based on given rules:
    - Consecutive differences must remain consistent in direction.
    - Absolute differences between elements must be between 1 and 3.
    """
    prev_diff = 0
    for i in range(len(level) - 1):
        diff = level[i + 1] - level[i]
        if prev_diff * diff < 0 or not (0 < abs(diff) <= 3):
            return False
        prev_diff = diff
    return True


def parse_input(file_path):
    """
    Parse input from a text file where each line represents a level.
    """
    with open(file_path, 'r') as f:
        return [[int(n) for n in line.split()] for line in f.readlines()]


def part_a(levels):
    """
    Solve Part A: Count how many levels are safe.
    """
    return sum(1 for level in levels if is_save(level))


def part_b(levels):
    """
    Solve Part B: Count how many levels can be made safe by removing one element.
    """
    safe_count = 0
    for level in levels:
        if is_save(level):
            safe_count += 1
            continue

        # Check if removing one element makes the level safe
        for i in range(len(level)):
            modified_level = level[:i] + level[i + 1:]
            if is_save(modified_level):
                safe_count += 1
                break

    return safe_count


if __name__ == "__main__":
    # Load test and input data
    test_file = "day2_test.txt"
    input_file = "day2_input.txt"

    test_levels = parse_input(test_file)
    input_levels = parse_input(input_file)

    # Run assertions for test data
    assert part_a(test_levels) == 2, "Part A Test failed!"
    assert part_b(test_levels) == 4, "Part B Test failed!"

    # Solve and print results for input data
    print("Part A:", part_a(input_levels))
    print("Part B:", part_b(input_levels))
