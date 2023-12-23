def get_neighbours(grid, x, y):
    unfiltered = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    return [(x2, y2) for x2, y2 in unfiltered if 0 <= x2 < len(grid[0]) and 0 <= y2 < len(grid) and grid[y2][x2] != "#"]

def make_network(grid):
    network = {}
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell != "#":
                network[(x, y)] = [(neighbour, 1) for neighbour in get_neighbours(grid, x, y)]
    
    del_list = []
    for (x, y), neighbours in network.items():
        if len(neighbours) == 2:
            half_distances = []
            new_neighbour_lists = [[], []]
            for i, (neighbour, dist) in enumerate(neighbours):
                for n2, dist2 in network[neighbour]:
                    if n2 != (x, y):
                        new_neighbour_lists[i].append((n2, dist2))
                    else:
                        half_distances.append(dist2)
            full_distance = sum(half_distances)
            new_neighbour_lists[0].append((neighbours[1][0], full_distance))
            new_neighbour_lists[1].append((neighbours[0][0], full_distance))
            for i in range(2):
                network[neighbours[i][0]] = new_neighbour_lists[i]
            del_list.append((x, y))
    for key in del_list:
        del network[key]
    return network

def search(grid, start, end, use_network=False):
    path_lengths = []
    stack = [(start, 0, set())] if use_network else [(start, set())]
    network = make_network(grid) if use_network else None

    while stack:
        if use_network:
            pos, current_length, visited = stack.pop()
        else:
            pos, visited = stack.pop()
            current_length = len(visited)

        if pos == end:
            path_lengths.append(current_length + (1 if use_network else 0))
            continue

        neighbours = network[pos] if use_network else get_neighbours(grid, pos[0], pos[1])
        for neighbour in neighbours:
            next_pos, dist = neighbour if use_network else (neighbour, 1)
            if next_pos not in visited:
                visited_copy = visited.copy()
                visited_copy.add(next_pos)
                stack.append((next_pos, current_length + dist, visited_copy) if use_network else (next_pos, visited_copy))

    return path_lengths

# Read the grid from the file
with open("23.txt") as file:
    grid = [line.strip() for line in file]

start = (grid[0].index("."), 0)
end = (grid[-1].index("."), len(grid) - 1)

# Search without using network
path_lengths_without_network = search(grid, start, end)
print("Part 1, Max path length without network:", max(path_lengths_without_network))

# Search using network
path_lengths_with_network = search(grid, start, end, use_network=True)
print("Part 2,Max path length with network:", max(path_lengths_with_network))
#2110, 6522