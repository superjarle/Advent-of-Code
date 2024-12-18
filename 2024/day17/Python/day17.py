from time import time

# Start the timer
start_time = time()

# Input file and data processing
INPUT_FILE = "day17_input.txt"
holiday_blocks = [block.splitlines() for block in open(INPUT_FILE, "r").read().split("\n\n")]

# Registers for our holiday machine
gift_register = {line[9]: int(line[12:]) for line in holiday_blocks[0]}
holiday_program = list(map(int, holiday_blocks[1][0][9:].split(",")))

def run_holiday_machine(program, register):
    instruction_pointer = 0
    festive_output = []

    while instruction_pointer < len(program) - 1:
        opcode = program[instruction_pointer]
        operand = program[instruction_pointer + 1]

        literal = operand
        combo = 0
        if 0 <= operand <= 3:
            combo = operand
        elif operand == 4:
            combo = register["A"]
        elif operand == 5:
            combo = register["B"]
        elif operand == 6:
            combo = register["C"]

        if opcode == 0:
            register["A"] = register["A"] >> combo
            instruction_pointer += 2
        elif opcode == 1:
            register["B"] = register["B"] ^ literal
            instruction_pointer += 2
        elif opcode == 2:
            register["B"] = combo % 8
            instruction_pointer += 2
        elif opcode == 3:
            instruction_pointer = literal if register["A"] != 0 else instruction_pointer + 2
        elif opcode == 4:
            register["B"] = register["B"] ^ register["C"]
            instruction_pointer += 2
        elif opcode == 5:
            festive_output.append(combo % 8)
            instruction_pointer += 2
        elif opcode == 6:
            register["B"] = register["A"] >> combo
            instruction_pointer += 2
        elif opcode == 7:
            register["C"] = register["A"] >> combo
            instruction_pointer += 2

    return festive_output

# Part 1: Holiday Magic
holiday_output = run_holiday_machine(holiday_program, gift_register.copy())
part1_result = ",".join(map(str, holiday_output))
print(f"Part 1 (Holiday Magic): {part1_result}  ({time() - start_time:.3f}s)")

# Part 2: Find the Right Gift Combo
def find_gift_combinations(current_value, depth):
    target = holiday_program[depth]
    candidates = []

    for value in range(8):
        temp_register = gift_register.copy()
        temp_register["A"] = current_value | value
        output = run_holiday_machine(holiday_program, temp_register)
        if output[0] == target:
            if depth == 0:
                candidates.append(current_value | value)
            else:
                candidates.extend(find_gift_combinations((current_value | value) << 3, depth - 1))
    return candidates

possible_gifts = find_gift_combinations(0, len(holiday_program) - 1)
part2_result = min(possible_gifts)
print(f"Part 2 (Optimal Gift): {part2_result}  ({time() - start_time:.3f}s)")