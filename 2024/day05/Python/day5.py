from collections import defaultdict

# Load
with open("input_day5.txt") as file:
    input_data = file.read().strip()

# Split rules and updates sections
rules_section, updates_section = input_data.split("\n\n")

# Parse rules
page_rules = defaultdict(set)
for rule_line in rules_section.split("\n"):
    page_before, page_after = map(int, rule_line.split("|"))
    page_rules[page_before].add(page_after)

# Parse updates
updates_list = [list(map(int, update_line.split(","))) for update_line in updates_section.split("\n")]


def is_in_correct_order(update):
    remaining_pages = set(update)  # Track remaining pages to check
    for current_page in update:
        remaining_pages.remove(current_page)
        if not (remaining_pages <= page_rules[current_page]):
            return False
    return True


# Part 1
correctly_ordered_updates = [
    update[len(update) // 2] for update in updates_list if is_in_correct_order(update)
]
print(sum(correctly_ordered_updates))


def reorder_update(update):
    index = 0
    while index < len(update) - 1:
        current_page = update[index]
        remaining_pages = set(update[index + 1:])
        if not (remaining_pages <= page_rules[current_page]):
            # Move the out-of-place page to the end
            update.append(update.pop(index))
            # Restart checking from the beginning
            index = 0
        else:
            index += 1
    return update


# Part 2
incorrect_updates = [
    update for update in updates_list if not is_in_correct_order(update)
]
reordered_updates = [reorder_update(update) for update in incorrect_updates]
reordered_middle_pages = [
    update[len(update) // 2] for update in reordered_updates
]
print(sum(reordered_middle_pages))
