from time import time
from collections import defaultdict

def parse_input(file_path):
    """Reads the input file and constructs the graph."""
    graph = defaultdict(set)
    with open(file_path, "r") as f:
        for line in f:
            a, b = line.strip().split("-")
            graph[a].add(b)
            graph[b].add(a)
    return graph

def find_triples_with_t(graph):
    """Finds all sets of three interconnected computers where at least one starts with 't'."""
    cliques_3t = set()
    for node1 in (n for n in graph if n.startswith("t")):
        for node2 in graph[node1]:
            for node3 in graph[node1]:
                if node3 in graph[node2] and node2 != node3:
                    cliques_3t.add(tuple(sorted((node1, node2, node3))))
    return cliques_3t

def bron_kerbosch_with_pivot(graph):
    """Implementing the Bron-Kerbosch algorithm with pivoting to find all maximal cliques.
    The algorithm works as follows:
    - R is the current clique being built.
    - P is the set of candidates that can extend R.
    - X is the set of nodes that should be excluded from further extensions of R.
    - Pivoting improves efficiency by reducing the size of P.
    """
    cliques = []
    stack = [(set(), set(graph.keys()), set())]
    while stack:
        r, p, x = stack.pop()
        if not p and not x:
            cliques.append(r)
        else:
            pivot = max(p.union(x), key=lambda v: len(graph[v]), default=None)
            candidates = p - graph[pivot] if pivot else p
            for v in list(candidates):
                stack.append((r | {v}, p & graph[v], x & graph[v]))
                p.remove(v)
                x.add(v)
    return cliques

def find_largest_clique(graph):
    """Finds the largest clique in the graph."""
    max_clique = set()
    for clique in bron_kerbosch_with_pivot(graph):
        if len(clique) > len(max_clique):
            max_clique = clique
    return max_clique

if __name__ == "__main__":
    time_start = time()
    INPUT_FILE = "day23_input.txt"
    graph = parse_input(INPUT_FILE)

    # Part 1: Find all sets of three LAN computers with at least one 't'
    triples_with_t = find_triples_with_t(graph)
    print(f"Number of computers: {len(triples_with_t)} ({time() - time_start:.3f}s)")

    # Part 2: Find the largest clique and compute the password
    largest_clique = find_largest_clique(graph)
    password = ",".join(sorted(largest_clique))
    print(f"LAN Password: {password} ({time() - time_start:.3f}s)")