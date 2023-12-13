class WindowShopper:
    def __init__(self, file_path):
        self.patterns = self._load_patterns(file_path)

    def _load_patterns(self, file_path):
        patterns = []
        with open(file_path, 'r') as file:
            pattern = []
            for line in file.readlines():
                line = list(line.strip())
                if not line:
                    patterns.append(pattern)
                    pattern = []
                else:
                    pattern.append(line)
            if pattern:
                patterns.append(pattern)
        return patterns

    @staticmethod
    def _rotate_pattern(pattern):
        return list(map(list, zip(*pattern[::-1])))

    @staticmethod
    def _find_reflection_line(pattern):
        for i in range(len(pattern) - 1):
            if pattern[i] == pattern[i + 1]:
                for offset in range(1, min(i, len(pattern) - i - 2) + 1):
                    if pattern[i - offset] != pattern[i + 1 + offset]:
                        break
                else:
                    return i + 1
        return -1
    
    @staticmethod
    def count_differences(p1, p2):
        return sum(c1 != c2 for c1, c2 in zip(p1, p2))

    def confirm_match(self, pattern, i, differences):
        first, second = i - 1, i + 2
        while second < len(pattern) and first >= 0:
            if pattern[first] != pattern[second]:
                if differences == 1:
                    return False
                diff = self.count_differences(pattern[first], pattern[second])
                if diff == 1:
                    differences += 1
                else:
                    return False
            first -= 1
            second += 1
        return differences > 0

    def find_reflection(self, pattern):
        for i in range(len(pattern) - 1):
            if pattern[i] == pattern[i + 1]:
                if self.confirm_match(pattern, i, 0):
                    return i + 1
            else:
                differences = self.count_differences(pattern[i], pattern[i + 1])
                if differences == 1 and self.confirm_match(pattern, i, 1):
                    return i + 1
        return -1
    
    def calculate_part1(self):
        total = 0
        for pattern in self.patterns:
            horizontal_reflection = self._find_reflection_line(pattern)
            if horizontal_reflection != -1:
                total += 100 * horizontal_reflection
            else:
                vertical_reflection = self._find_reflection_line(self._rotate_pattern(pattern))
                if vertical_reflection != -1:
                    total += vertical_reflection
        return total
        
    def calculate_part2(self):
        total = 0
        for pattern in self.patterns:
            # Check for horizontal reflection
            horizontal_reflection = self.find_reflection(pattern)
            if horizontal_reflection != -1:
                total += 100 * horizontal_reflection
            else:
                # Rotate pattern to check for vertical reflection
                vertical_reflection = self.find_reflection(self._rotate_pattern(pattern))
                if vertical_reflection != -1:
                    total += vertical_reflection
        return total

if __name__ == "__main__":
    puzzler = WindowShopper('input.txt')
    q1 = puzzler.calculate_part1()
    q2 = puzzler.calculate_part2()
    print(f"Solution for part 1 is: {q1}")
    print(f"Solution for part 2 is: {q2}")