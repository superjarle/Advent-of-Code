from collections import Counter


def read_input(file_name):
    """
    Reads the input file and splits it into lines.
    """
    with open(file_name, 'r') as file:
        return file.read().splitlines()

def parse_data(data):
    """
    Parses the input data to extract and sort left and right values.
    """
    left = sorted([int(line.split("   ")[0]) for line in data])
    right = sorted([int(line.split("   ")[-1]) for line in data])
    return left, right

def part_a(data):
    """
    Computes the sum of absolute differences between corresponding
    elements in the sorted left and right lists.
    """
    left, right = parse_data(data)
    return sum(abs(l - r) for l, r in zip(left, right))

def part_b(data):
    """
    Computes a custom similarity score by counting matches
    between sorted left and right lists.
    """
    left, right = parse_data(data)
    right_counts = Counter(right)  # Count occurrences in the right list

    result = 0
    for l in set(left):  # Iterate through unique values in left
        result += l * right_counts[l]  # Multiply value by its count in right
    return result

if __name__ == "__main__":
    # File paths
    test_file = 'day1_test.txt'
    real_file = 'day1_input.txt'

    # Read and test data
    test_data = read_input(test_file)
    assert part_a(test_data) == 11
    assert part_b(test_data) == 31
    print("Test cases passed!")

    # Process real input
    real_data = read_input(real_file)
    print("Part A:", part_a(real_data))
    print("Part B:", part_b(real_data))
