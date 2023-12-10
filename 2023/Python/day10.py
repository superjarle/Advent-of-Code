class PipeNetwork:
    def __init__(self, file_path):
        self.file_path = file_path
        self.nodes = []
        self.start_node = []
        self.pipes = {"|": [1, 0, -1, 0], "-": [0, 1, 0, -1], 
                      "L": [-1, 0, 0, 1], "J": [-1, 0, 0, -1], 
                      "7": [1, 0, 0, -1], "F": [1, 0, 0, 1], 
                      ".": [0, 0, 0, 0]}
        self.read_input()
        self.create_graph()

    def read_input(self):
        with open(self.file_path, 'r') as file:
            self.lines = [line.strip() for line in file]

    def create_graph(self):
        for i, line in enumerate(self.lines):
            line_nodes = []
            for j, char in enumerate(line):
                if char == "S":
                    line_nodes.append([])
                    self.start_node = [i, j]
                else:
                    pipe = self.pipes[char]
                    line_nodes.append([i + pipe[0], j + pipe[1], i + pipe[2], j + pipe[3]])
            self.nodes.append(line_nodes)
        self.update_start_node_connections()

    def update_start_node_connections(self):
        for i, row in enumerate(self.nodes):
            for j, node in enumerate(row):
                if [i, j] == self.start_node:
                    continue
                if [node[0], node[1]] == self.start_node or [node[2], node[3]] == self.start_node:
                    self.nodes[self.start_node[0]][self.start_node[1]] += [i, j]

    def simulate_movement(self):
        steps = 0
        pos1 = [self.start_node, [self.nodes[self.start_node[0]][self.start_node[1]][0], self.nodes[self.start_node[0]][self.start_node[1]][1]]]
        pos2 = [self.start_node, [self.nodes[self.start_node[0]][self.start_node[1]][2], self.nodes[self.start_node[0]][self.start_node[1]][3]]]

        while True:
            steps += 1
            pos1 = self.move_position(pos1)
            pos2 = self.move_position(pos2)
            if pos1[0] == pos2[0]:
                break
        return steps

    def move_position(self, position):
        current, prev = position
        values = self.nodes[current[0]][current[1]]
        if values[0] == prev[0] and values[1] == prev[1]:
            return [[values[2], values[3]], current]
        else:
            return [[values[0], values[1]], current]

    def calculate_empty_spaces(self):
        loop_nodes = [[False for j in range(len(self.nodes[0]) * 3)] for i in range(len(self.nodes) * 3)]
        self.add_node_to_loop(loop_nodes, self.start_node)

        pos1 = [self.start_node, [self.nodes[self.start_node[0]][self.start_node[1]][0], self.nodes[self.start_node[0]][self.start_node[1]][1]]]
        pos2 = [self.start_node, [self.nodes[self.start_node[0]][self.start_node[1]][2], self.nodes[self.start_node[0]][self.start_node[1]][3]]]

        while True:
            pos1 = self.move_position(pos1)
            pos2 = self.move_position(pos2)
            self.add_node_to_loop(loop_nodes, pos1[0])
            self.add_node_to_loop(loop_nodes, pos2[0])
            if pos1[0] == pos2[0]:
                break

        self.flood_fill(loop_nodes)
        return self.count_empty_spaces(loop_nodes)

    def add_node_to_loop(self, loop_nodes, position):
        conn_node = self.nodes[position[0]][position[1]]
        conn = [position[0] - conn_node[0], position[1] - conn_node[1], position[0] - conn_node[2], position[1] - conn_node[3]]
        loop_nodes[position[0] * 3 + 1][position[1] * 3 + 1] = True
        loop_nodes[position[0] * 3 + 1 - conn[0]][position[1] * 3 + 1 - conn[1]] = True
        loop_nodes[position[0] * 3 + 1 - conn[2]][position[1] * 3 + 1 - conn[3]] = True

    def flood_fill(self, loop_nodes):
        filling = [[0, 0]]
        loop_nodes[0][0] = True
        directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        while filling:
            new_filling = []
            for pos in filling:
                for dir in directions:
                    new = [pos[0] + dir[0], pos[1] + dir[1]]
                    if not loop_nodes[new[0]][new[1]]:
                        new_filling.append(new)
                        loop_nodes[new[0]][new[1]] = True
            filling = new_filling

    def count_empty_spaces(self, loop_nodes):
        empty_spaces = 0
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes[0])):
                valid = True
                for x in range(3):
                    for y in range(3):
                        if loop_nodes[i * 3 + x][j * 3 + y]:
                            valid = False
                if valid:
                    empty_spaces += 1
        return empty_spaces


file_path = 'input.txt'  
pipe_network = PipeNetwork(file_path)

steps = pipe_network.simulate_movement()
empty_spaces = pipe_network.calculate_empty_spaces()

print(f"Number of steps: {steps}")
print(f"Number of empty spaces: {empty_spaces}")
