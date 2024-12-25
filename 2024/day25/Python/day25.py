from time import time

time_start = time()

# 🎁 Input file containing lock and key schematics 🎁
INPUT_FILE = "day25_input.txt"
snowflakes = [block.splitlines() for block in open(INPUT_FILE, "r").read().split("\n\n")]
ROWS, COLS = len(snowflakes[0]), len(snowflakes[0][0])

# 🎄 Separate locks and keys from the schematics 🎄
santa_locks, elf_keys = [], []
for snowflake in snowflakes:
    if snowflake[0][0] == "#":
        santa_locks += [snowflake]
    else:
        elf_keys += [snowflake]

# 🎅 Function to check if a lock and key fit 🎅
def magical_fit(lock, key):
    for col in range(COLS):
        for row in range(ROWS):
            if lock[row][col] == key[row][col] == "#":
                return 0
    return 1

# 🎁 Count the number of lock/key pairs that fit 🎁
perfect_fits = 0
for santa_lock in santa_locks:
    for elf_key in elf_keys:
        perfect_fits += magical_fit(santa_lock, elf_key)

# 🎄 Part 1 Result 🎄
print(f"part 1: {perfect_fits}  ({time() - time_start:.3f}s)")
