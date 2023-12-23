import numpy as np
from collections import defaultdict

with open("22.txt", "r") as file:
    lines = file.readlines()

bricks = []
for line in lines:
    line = line.strip()
    start_coords, end_coords = line.split('~')
    start_coords = [int(coord) for coord in start_coords.split(',')]
    end_coords = [int(coord) for coord in end_coords.split(',')]
    bricks.append(np.array(start_coords + end_coords))
    for start, end in zip(start_coords, end_coords):
        assert start <= end

# Sort bricks by their z-coordinate
bricks.sort(key=lambda brick: brick[2])

# Initialize data structures for tracking brick relationships
supported_by = defaultdict(list)
supports = defaultdict(list)
fixed_positions = []

def get_positions(brick):
    """Gets the positions covered by the brick."""
    direction = brick[3:] - brick[:3]
    length = sum(direction)
    if length == 0:
        return [tuple(brick[:3])]
    direction //= length
    return [tuple(brick[:3] + p * direction) for p in range(length + 1)]

def can_fall(brick, index):
    """Determines if a brick can fall."""
    if brick[2] == 1:
        return False
    brick_positions = set(get_positions(brick - np.array([0, 0, 1, 0, 0, 1])))
    for j in range(index):
        if brick_positions.intersection(fixed_positions[j]):
            supported_by[index].append(j)
            supports[j].append(index)
    return not supported_by[index]

# Process bricks for falling and support
for i, brick in enumerate(bricks):
    while can_fall(brick, i):
        brick -= np.array([0, 0, 1, 0, 0, 1])
    fixed_positions.append(set(get_positions(brick)))

# Check bricks for disintegration and falling
disintegrating_count = 0
falling_count = 0
will_fall = defaultdict(set)

for b in range(len(bricks)):
    can_disintegrate = True
    for i in range(b + 1, len(bricks)):
        if supported_by[i] == [b]:
            can_disintegrate = False
            will_fall[b].add(i)
    if can_disintegrate:
        disintegrating_count += 1

# Further process falling bricks
for b in range(len(bricks)):
    i = b + 1
    while i < len(bricks):
        if i not in will_fall[b] and supported_by[i]:
            if all(s in will_fall[b] for s in supported_by[i]):
                will_fall[b].add(i)
                i = b + 1
        i += 1
    falling_count += len(will_fall[b])

print("Part 1, disintegrating bricks:", disintegrating_count)
print("Part 2, Falling bricks:", falling_count)
