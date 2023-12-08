def calc_steps(graph, instructions, src, end_with_z=False):
    visited = set()
    node = src
    for step_count, direction in enumerate(cycle(instructions), 1):
        if node in visited and not end_with_z:
            return step_count - 1  
        visited.add(node)

        node = graph[node][0 if direction == 'L' else 1]

        if end_with_z and node.endswith('Z'):
            return step_count

    return step_count

# Part 1
part1 = calc_steps(graph, instructions, 'AAA')

# Part 2
steps_for_all = [calc_steps(graph, instructions, src, True) for src in srcs]
part2 = lcm(steps_for_all)

part1, part2