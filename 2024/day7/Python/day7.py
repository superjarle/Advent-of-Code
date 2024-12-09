from functools import lru_cache
from collections import deque

# Read input data
with open("day7_input.txt") as f:
    jungle_input = f.read().strip()

# Parse the input
equations = []
for line in jungle_input.split("\n"):
    test_value, numbers = line.split(": ")
    numbers = list(map(int, numbers.split(" ")))
    equations.append((int(test_value), numbers))


# Evaluation function for operations
def calculate(current_value, next_value, operation):
    if operation == "||":
        return int(f"{current_value}{next_value}")
    elif operation == "+":
        return current_value + next_value
    elif operation == "*":
        return current_value * next_value
    else:
        raise ValueError("Invalid operation")



@lru_cache(None)  # Memoizes the function to avoid redundant computations
def possible_results(numbers, include_concat=False):
    """
    Calculate all possible results of inserting operations (+, *, ||)
    between the given numbers, evaluated left-to-right.

    Args:
    - numbers: A tuple of numbers to evaluate.
    - include_concat: Whether to include concatenation ('||') as an operator.

    Returns:
    - A set of all possible results.

    Remember this link from last year:
    - https://docs.python.org/3/library/functools.html#functools.lru_cache
    """
    operations = ["+", "*"]
    if include_concat:
        operations.append("||")

    queue = deque([(numbers[0], 1)])  # Start with the first number and position
    results = set()

    while queue:
        current_value, pos = queue.popleft()
        if pos == len(numbers):
            results.add(current_value)
            continue
        for operation in operations:
            queue.append((calculate(current_value, numbers[pos], operation), pos + 1))

    return results


# Solving the puzzles
part1_total = sum(
    test_value for test_value, numbers in equations
    if test_value in possible_results(tuple(numbers))
)
part2_total = sum(
    test_value for test_value, numbers in equations
    if test_value in possible_results(tuple(numbers), include_concat=True)
)

print(f"Part 1 Total Calibration Result: {part1_total}")
print(f"Part 2 Total Calibration Result: {part2_total}")
