from itertools import cycle
from math import gcd

# Funksjon for å beregne minste felles multiplum (LCM)
def lcm(numbers):
    def lcm_pair(a, b):
        return a * b // gcd(a, b)
    
    result = 1
    for number in numbers:
        result = lcm_pair(result, number)
    return result

# Funksjon for å beregne antall skritt for å nå 'ZZZ'
def calc_steps_1(graph, instructions):
    node = 'AAA'  # Startnoden er 'AAA'
    for step_count, direction in enumerate(cycle(instructions), 1):
        node = graph[node][0 if direction == 'L' else 1]
        if node == 'ZZZ':
            return step_count

# Funksjon for å beregne antall skritt fra en gitt startnode til alle noder ender med 'Z'.
def calc_steps_2(graph, instructions, src, end_with_z=False):
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

# Laster inn data fra fil og bygger opp et grafobjekt.
def load_data(puzzleinput):
    with open(puzzleinput, "r") as file:
        lines = file.readlines()

    instructions = lines[0].strip()
    graph = {}
    for line in lines[1:]:
        parts = line.strip().split(" = ")
        if len(parts) == 2:
            node, edges = parts
            graph[node] = edges.strip("()").split(", ")

    return graph, instructions

puzzleinput = "day8.txt"
graph, instructions = load_data(puzzleinput)

# Finner alle noder som ender med 'A'
srcs = [node for node in graph if node.endswith('A')]

# Del 1: Beregner antall skritt for å nå 'ZZZ'
part1 = calc_steps_1(graph, instructions)

# Del 2: Beregner LCM av antall skritt fra alle startnoder som ender med 'A' til alle ender med 'Z'
steps2 = [calc_steps_2(graph, instructions, src, True) for src in srcs]
part2 = lcm(steps2)

part1, part2
