from time import time

# Constants
EMPTY_SLOT = -1

start_time = time()

# Innput and parsing
INPUT_FILE = "day9_input.txt"
input_lines = [line.rstrip("\n") for line in open(INPUT_FILE, "r")]
disk_map = list(map(int, list(input_lines[0])))

# Disk layout and free space counter
disk_layout = []
free_space_count = 0
for index, value in enumerate(disk_map):
    disk_layout += [EMPTY_SLOT if index & 1 else index >> 1] * value
    free_space_count += value if index & 1 else 0

# Processing..
empty_slot_index = 0
while free_space_count:
    last_disk_value = disk_layout.pop()
    if last_disk_value != EMPTY_SLOT:
        empty_slot_index = next(
            i for i in range(empty_slot_index, len(disk_layout)) if disk_layout[i] == EMPTY_SLOT
        )
        disk_layout[empty_slot_index] = last_disk_value
    free_space_count -= 1

# Calculate Part 1
part1_result = sum(index * value for index, value in enumerate(disk_layout))
print(f"Part 1: {part1_result}  ({time() - start_time:.3f}s)")

# Rebuild disk
disk_layout = []
for index, value in enumerate(disk_map):
    disk_layout += [[EMPTY_SLOT if index & 1 else index >> 1, value]]

max_file_id = max(file_data[0] for file_data in disk_layout)

# Processing..
current_file_index = len(disk_layout) - 1
for file_id in range(max_file_id, 1, -1):
    current_file_index = next(
        i for i in range(current_file_index, -1, -1) if disk_layout[i][0] == file_id
    )
    file_size = disk_layout[current_file_index][1]
    empty_space_index = next(
        (i for i in range(0, current_file_index)
         if disk_layout[i][0] == EMPTY_SLOT and disk_layout[i][1] >= file_size),
        None
    )
    if empty_space_index is not None:
        disk_layout[current_file_index][0] = EMPTY_SLOT
        if file_size == disk_layout[empty_space_index][1]:
            disk_layout[empty_space_index][0] = file_id
        else:
            disk_layout[empty_space_index][1] -= file_size
            disk_layout.insert(empty_space_index, [file_id, file_size])

# Calculating part 2
part2_result = 0
index_counter = 0
for file_id, file_count in disk_layout:
    for _ in range(file_count):
        if file_id != EMPTY_SLOT:
            part2_result += file_id * index_counter
        index_counter += 1
print(f"Part 2: {part2_result}  ({time() - start_time:.3f}s)")