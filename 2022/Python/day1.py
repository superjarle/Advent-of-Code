puzzle = '202201.txt'

with open(puzzle, 'r') as file:
    calorie_data = file.readlines()


def calculate_max_calories(data):
    max_calories = 0
    current_calories = 0

    for line in data:
        if line.strip():  
            current_calories += int(line.strip())
        else:  
            if current_calories > max_calories:
                max_calories = current_calories
            current_calories = 0  

    if current_calories > max_calories:
        max_calories = current_calories

    return max_calories

max_calories = calculate_max_calories(calorie_data)
max_calories

def calculate_top_three_calories(data):
    elf_calories = []
    current_calories = 0

    for line in data:
        if line.strip():  
            current_calories += int(line.strip())
        else:
            if current_calories > 0:
                elf_calories.append(current_calories)
            current_calories = 0

    if current_calories > 0:
        elf_calories.append(current_calories)

    elf_calories.sort(reverse=True)
    return sum(elf_calories[:3])  # Sum the top three

total_top_three_calories = calculate_top_three_calories(calorie_data)
total_top_three_calories