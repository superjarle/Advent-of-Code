
fil = 'day03.txt'

with open(fil, 'r') as file:
    rucksack_contents = file.readlines()

def find_common_items_and_calculate_priority(contents):
    def calculate_priority(char):

        if 'a' <= char <= 'z':
            return ord(char) - ord('a') + 1
        elif 'A' <= char <= 'Z':
            return ord(char) - ord('A') + 27

    total_priority = 0
    for line in contents:
        line = line.strip()
        half_length = len(line) // 2
        compartment_1, compartment_2 = set(line[:half_length]), set(line[half_length:])

        common_items = compartment_1.intersection(compartment_2)

        if common_items:
            common_item = common_items.pop()
            total_priority += calculate_priority(common_item)

    return total_priority

def find_badge_items_and_calculate_priority(contents):
    def calculate_priority(char):
        if 'a' <= char <= 'z':
            return ord(char) - ord('a') + 1
        elif 'A' <= char <= 'Z':
            return ord(char) - ord('A') + 27

    total_priority = 0
    for i in range(0, len(contents), 3):
        group = contents[i:i+3]
        common_items = set(group[0].strip())

        for elf in group[1:]:
            common_items.intersection_update(elf.strip())

        if common_items:
            badge_item = common_items.pop()
            total_priority += calculate_priority(badge_item)

    return total_priority

part1 = find_common_items_and_calculate_priority(rucksack_contents)
part1
part2 = find_badge_items_and_calculate_priority(rucksack_contents)
part2