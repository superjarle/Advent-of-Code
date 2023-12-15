"""
Created on Tue Dec 12 06:07:44 2023

@author: jkv
"""


class HotSpringPuzzle:
    """
    A class to solve the spring puzzle. This class reads an input file containing
    the condition of springs (operational (.), damaged(#), or unknown(?)) and calculates
    the total number of valid arrangements of these hot springs.
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.history = {}
        self.values = []

    def read_input(self):
        with open(self.file_path, 'r') as file:
            self.values = [line.strip() for line in file.readlines()]

    def calc_clue(self, clue, vals, current_run):
        """
        Recursively calculates the number of valid arrangements for a given row
        of springs, based on the current clue, the values of damaged spring groups,
        and the current run of contiguous damaged springs.

        clue: Current state of conditions
        vals: Size of damanged groups
        current_run: Size of current contiguous group of damaged springs.
        return: The number of valid arrangements for the present state
        """
        key = (clue, tuple(vals), current_run)
        if key in self.history:
            return self.history[key]

        retur = 0
        if clue == ".":
            if len(vals) == 0 and current_run == 0:
                retur += 1
        else:
            if clue[0] == "?":
                if current_run == 0 or len(vals) > 0 and vals[0] == current_run:
                    retur += self.calc_clue("." + clue[1:], vals, current_run)
                if len(vals) > 0:
                    retur += self.calc_clue("#" + clue[1:], vals, current_run)
            elif clue[0] == "#":
                if len(vals) > 0:
                    if vals[0] == current_run + 1:
                        if clue[1] == ".":
                            retur += self.calc_clue(clue[1:], vals[1:], 0)
                        elif clue[1] == "?":
                            retur += self.calc_clue("." + clue[2:], vals[1:], 0)
                    elif current_run < vals[0] and clue[1] == "#":
                        retur += self.calc_clue(clue[1:], vals, current_run + 1)
                    elif current_run < vals[0] and clue[1] == "?":
                        retur += self.calc_clue("#" + clue[2:], vals, current_run + 1)
            elif clue[0] == ".":
                if current_run == 0:
                    retur += self.calc_clue(clue[1:], vals, 0)

        self.history[key] = retur
        return retur

    def calc_arrangements(self, mode):
        """
        Calculates the total number of valid arrangements for all rows in the input
        """
        retur = 0
        for row in self.values:
            clue, vals = row.split(" ")
            if mode == 2:
                clue = "?".join([clue] * 5)
                vals = ",".join([vals] * 5)
            vals = [int(x) for x in vals.split(",")]
            clue += "."
            retur += self.calc_clue(clue, vals, 0)
        return retur

if __name__ == "__main__":
    puzzler = HotSpringPuzzle('input.txt')
    puzzler.read_input()
    arrangements_1 = puzzler.calc_arrangements(mode=1)
    arrangements_2 = puzzler.calc_arrangements(mode=2)

# And finally! 
    print(f"Solution for part 1 is: {arrangements_1}")
    print(f"Solution for part 2 is: {arrangements_2}")