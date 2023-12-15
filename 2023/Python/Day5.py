# Day 5 combined

class Solve:
    def __init__(self, filename):
        self.filename = filename
        self.seeds, self.stages = self.read_from_file()

    @staticmethod
    def make_maps(data):
        return sorted((int(src_start), int(src_start) + int(length), int(dest_start)) for dest_start, src_start, length in (line.split() for line in data))

    def read_from_file(self):
        with open(self.filename, 'r') as file:
            lines = file.read().split('\n')

        seeds_line, *stages_lines = lines
        seeds = [(int(x), int(y)) for x, y in zip(*[iter(seeds_line.split(': ')[1].split())]*2)]

        stages = []
        stage = []
        for line in stages_lines:
            if line.endswith(' map:'):
                if stage:
                    stages.append(stage)
                    stage = []
            elif line:
                stage.append(line)
        stages.append(stage)

        return seeds, stages

    def lowest_location_1(self):
        min_locations = []
        for seed in self.seeds:
            location = seed[0]
            for stage in self.stages:
                location = self.convert_1(location, self.make_maps(stage))
            min_locations.append(location)

        return min(min_locations)

    @staticmethod
    def convert_1(value, maps):
        for src_start, src_end, dest_start in maps:
            if src_start <= value < src_end:
                return value - src_start + dest_start
        return value

    def lowest_location_2(self):
        ranges = self.seeds
        for maps in self.stages:
            new_ranges = []
            for start, length in ranges:
                new_ranges.extend(self.convert_range(start, length, self.make_maps(maps)))
            ranges = new_ranges

        return min(start for start, length in ranges)

    @staticmethod
    def convert_range(start, length, maps):
        out_ranges = []
        i = 0
        while length > 0 and i < len(maps):
            src_start, src_end, dest_start = maps[i]
            if start >= src_end:
                i += 1
            elif start < src_start:
                if length <= src_start - start:
                    out_ranges.append((start, length))
                    return out_ranges
                else:
                    out_ranges.append((start, src_start - start))
                    length -= src_start - start
                    start = src_start
            else:
                if length <= src_end - start:
                    out_ranges.append((start - src_start + dest_start, length))
                    return out_ranges
                else:
                    out_ranges.append((start - src_start + dest_start, src_end - start))
                    length -= src_end - start
                    start = src_end
        if length > 0:
            out_ranges.append((start, length))
        return out_ranges

## Solving the two parts
solver = Solve('')
part1 = solver.lowest_location_1()
part2 = solver.lowest_location_2()
part1, part2

