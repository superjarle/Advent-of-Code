import re


class MemoryProcessor:
    """
    Class to process corrupted memory for valid `mul` instructions
    with support for conditional `do()` and `don't()` instructions.
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.content = self._load_file()
        self.total = 0
        self.patterns = {
            "mul": re.compile(r"mul\((\d{1,3}),(\d{1,3})\)"),
            "do": re.compile(r"do\(\)"),
            "dont": re.compile(r"don't\(\)")
        }

    def _load_file(self):
        with open(self.file_path, 'r') as f:
            return f.read()

    def _get_matches(self, pattern_name):
        """Finds all matches for the specified pattern."""
        return list(re.finditer(self.patterns[pattern_name], self.content))

    def calculate_total(self, conditional=False):
        """
        Calculates the total of valid `mul` instructions.
        :param conditional: Whether to consider `do()` and `don't()` states
        :return: Total sum of valid multiplications
        """
        self.total = 0

        mul_matches = self._get_matches("mul")
        if conditional:
            do_positions = [m.start() for m in self._get_matches("do")]
            dont_positions = [m.start() for m in self._get_matches("dont")]
            current_enabled = True

        for mul_match in mul_matches:
            if conditional:
                # Update state based on closest do() or don't() position
                mul_start = mul_match.start()
                while do_positions and do_positions[0] < mul_start:
                    current_enabled = True
                    do_positions.pop(0)
                while dont_positions and dont_positions[0] < mul_start:
                    current_enabled = False
                    dont_positions.pop(0)

                # Skip this mul if not enabled
                if not current_enabled:
                    continue

            # Process valid mul
            x, y = map(int, mul_match.groups())
            self.total += x * y

        return self.total


if __name__ == "__main__":
    input_file = 'day3_input.txt'
    processor = MemoryProcessor(input_file)

    # Solve part 1: Total of all mul
    total_basic = processor.calculate_total(conditional=False)
    print(f"Total (basic): {total_basic}")

    # Solve part 2: Total with do() and don't() conditions
    total_conditional = processor.calculate_total(conditional=True)
    print(f"Total (conditional): {total_conditional}")
