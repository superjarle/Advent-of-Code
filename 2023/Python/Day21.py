import heapq

# Open and read the puzzle input file
file = open("21.txt", "r")
lines = list(file)
file.close()

# Process the grid and find the starting position
grid = []
start_pos = None
for row_index, line in enumerate(lines):
    line = line.strip()
    grid.append(list(line))
    if 'S' in line:
        start_pos = (row_index, line.find('S'))

# Initialize the priority queue for the breadth-first search
queue = [(0, start_pos[0], start_pos[1])]

# Part 1: Calculate reachable plots in 64 steps
while True:
    current_state = heapq.heappop(queue)
    if current_state[0] == 64:
        print("Reachable plots in 64 steps:", len(queue) + 1)
        break
    for direction in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
        new_pos = (current_state[1] + direction[0], current_state[2] + direction[1])
        if 0 <= new_pos[0] < len(grid) and 0 <= new_pos[1] < len(grid[0]) and grid[new_pos[0]][new_pos[1]] in ['S', '.']:
            next_state = (current_state[0] + 1, new_pos[0], new_pos[1])
            if next_state not in queue:
                heapq.heappush(queue, next_state)

# Reset for part 2
queue = [(0, start_pos[0], start_pos[1])]
visited = set()
odd_visits, even_visits = 0, 0
current_step = -1
v0, v1, v2 = -1, -1, -1
grid_length = len(grid)

# Part 2: Compute using quadratic interpolation
while True:
    current_state = queue.pop(0)
    visited.add((current_state[1], current_state[2]))
    if current_state[0] > current_step:
        if current_state[0] % 2 == 0:
            even_visits += len(queue) + 1
        else:
            odd_visits += len(queue) + 1
        current_step = current_state[0]

    if current_state[0] == start_pos[0]:
        v0 = odd_visits if current_state[0] % 2 == 1 else even_visits
    elif current_state[0] == start_pos[0] + grid_length:
        v1 = odd_visits if current_state[0] % 2 == 1 else even_visits
    elif current_state[0] == start_pos[0] + 2 * grid_length:
        v2 = odd_visits if current_state[0] % 2 == 1 else even_visits
        break

    for direction in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
        new_pos = (current_state[1] + direction[0], current_state[2] + direction[1])
        if new_pos not in visited and grid[new_pos[0] % grid_length][new_pos[1] % len(grid[0])] in ['S', '.']:
            next_state = (current_state[0] + 1, new_pos[0], new_pos[1])
            if next_state not in queue:
                queue.append(next_state)

# Calculate the quadratic function coefficients
constant = v0
a_coefficient = (v2 - constant - 2 * (v1 - constant)) // 2
b_coefficient = v1 - constant - a_coefficient
quadratic_function = lambda n: a_coefficient * n ** 2 + b_coefficient * n + constant

# Calculate and print the result for the given goal
goal = 26501365
print("Reachable plots for", goal, "steps:", quadratic_function(goal // grid_length))
