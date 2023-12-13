patterns = []
with open('input.txt', 'r') as file:
    pattern = []
    for line in file.readlines():
        line = list(line.strip())
        if not line:
            patterns.append(pattern)
            pattern = []
        else:
            pattern.append(line)
    patterns.append(pattern)

def rotate_pattern(pattern):
    return list(map(list, zip(*pattern[::-1])))

def find_reflection_line(pattern):
    """
    Find the line of reflection in the pattern, either horizontally or after rotation for vertical.
    Returns the line number (1-based) if found, otherwise -1.
    """
    for i in range(len(pattern) - 1):
        if pattern[i] == pattern[i + 1]:
            # Check if the pattern is mirrored above and below the found line
            for offset in range(1, min(i, len(pattern) - i - 2) + 1):
                if pattern[i - offset] != pattern[i + 1 + offset]:
                    break
            else:
                return i + 1  # Reflection line found
    return -1

def calculate_total_summary(patterns):
    total = 0
    for pattern in patterns:
        # Check for horizontal reflection
        horizontal_reflection = find_reflection_line(pattern)
        if horizontal_reflection != -1:
            total += 100 * horizontal_reflection
        else:
            # Rotate pattern for vertical reflection check
            vertical_reflection = find_reflection_line(rotate_pattern(pattern))
            if vertical_reflection != -1:
                total += vertical_reflection
    return total

part1 = calculate_total_summary(patterns)
print(f"Solution for part 1 is: {part1}")