from time import time

# Start the timer
start_time = time()

# Input file and data processing
INPUT_FILE = "day13_input.txt"
lines = [line.strip() for line in open(INPUT_FILE, "r")]
data_blocks = [block.splitlines() for block in open(INPUT_FILE, "r").read().split("\n\n")]

# Function to solve equations for non-negative integers a and b so that:
#   a * coefficients_x[0] + b * coefficients_x[1] = coefficients_x[2]
#   a * coefficients_y[0] + b * coefficients_y[1] = coefficients_y[2]
def solve_equations(coefficients_x, coefficients_y):
    constant_diff = coefficients_x[2] * coefficients_y[0] - coefficients_y[2] * coefficients_x[0]
    coefficient_diff = coefficients_x[1] * coefficients_y[0] - coefficients_y[1] * coefficients_x[0]

    # Check divisibility
    if constant_diff % coefficient_diff != 0:
        return ()
    b = constant_diff // coefficient_diff

    # Solve for 'a'
    if (coefficients_x[2] - b * coefficients_x[1]) % coefficients_x[0] != 0:
        return ()
    a = (coefficients_x[2] - b * coefficients_x[1]) // coefficients_x[0]

    # Return result if non-negative
    if a >= 0 and b >= 0:
        return a, b
    return ()

# Initialize results
part1_result = 0
part2_result = 0

# Process each of those data blocks
for block in data_blocks:
    coefficients_x, coefficients_y = [0] * 3, [0] * 3

    # Parsing the coefficients
    for i in range(3):
        _, equation = block[i].split(": ")
        term_x, term_y = equation.split(", ")
        coefficients_x[i] = int(term_x[2:])
        coefficients_y[i] = int(term_y[2:])

    # Solving part 1
    solution = solve_equations(coefficients_x, coefficients_y)
    if solution:
        part1_result += 3 * solution[0] + solution[1]

    # Adjusting for part 2 and solving
    coefficients_x[2] += 10_000_000_000_000
    coefficients_y[2] += 10_000_000_000_000
    solution = solve_equations(coefficients_x, coefficients_y)
    if solution:
        part2_result += 3 * solution[0] + solution[1]

# Printing the output
print(f"Part 1: {part1_result}  ({time() - start_time:.3f}s)")
print(f"Part 2: {part2_result}  ({time() - start_time:.3f}s)")
