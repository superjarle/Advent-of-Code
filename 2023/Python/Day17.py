import time
from collections import defaultdict
from heapq import heappop, heappush

class ClumsyCrucible:
    def __init__(self, filepath):
        self.filepath = filepath
        self.city_blocks = {}

    def load_data(self):
        with open(self.filepath) as file:
            self.city_blocks = {
                row_index * 1j + col_index: int(char)
                for row_index, row in enumerate(file)
                for col_index, char in enumerate(row.strip())
            }

    def calculate_min_heat_loss(self, min_straight, max_straight):
        max_row = int(max(rc.imag for rc in self.city_blocks))
        max_col = int(max(rc.real for rc in self.city_blocks))

        to_visit = [(0, 0, 0, 0, 1, 0), (0, 0, 0, 0, 0, 1)]
        seen = defaultdict(lambda: float("inf"))
        while to_visit:
            heat_loss, straight, rc_real, rc_imag, d_real, d_imag = heappop(to_visit)
            rc = rc_imag * 1j + rc_real
            d = d_imag * 1j + d_real
            if rc == max_row * 1j + max_col and straight >= min_straight:
                return heat_loss
            directions = [d] if straight < max_straight else []
            if straight >= min_straight:
                directions.extend([d * 1j, d / 1j])

            for new_d in directions:
                new_rc = rc + new_d
                new_straight = straight + 1 if new_d == d else 1
                if new_rc in self.city_blocks:
                    new_heat_loss = heat_loss + self.city_blocks[new_rc]
                    if seen[new_rc, new_d, new_straight] > new_heat_loss:
                        seen[new_rc, new_d, new_straight] = new_heat_loss
                        heappush(to_visit, (new_heat_loss, new_straight, new_rc.real, new_rc.imag, new_d.real, new_d.imag))

    def run(self):
        start_time = time.time()
        self.load_data()
        result_part1 = self.calculate_min_heat_loss(1, 3)
        result_part2 = self.calculate_min_heat_loss(4, 10)
        end_time = time.time()
        elapsed_time = (end_time - start_time) * 1000
        return result_part1, result_part2, elapsed_time


if __name__ == '__main__':
    crucible = ClumsyCrucible('input.txt')
    part1_result, part2_result, total_time = crucible.run()
    print(f"Answer for Part 1: {part1_result}")
    print(f"Answer for Part 2: {part2_result}")
    print(f"Execution time: {total_time:.2f} milliseconds")
