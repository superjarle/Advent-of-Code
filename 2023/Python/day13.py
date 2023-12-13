class PatternAnalyzer:
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

    def calculate_total_summary(self):
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

analyzer = PatternAnalyzer('input.txt')
part1 = analyzer.calculate_total_summary()
print(f"Solution for part 1 is: {part1}")
