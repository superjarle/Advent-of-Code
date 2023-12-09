def extrapolate_value(history):
    """
    Extrapolartes the next value and evalute the diff sequence. Returns extrapolated value. 
    """
    sequences = [history]
    while len(set(sequences[-1])) > 1:
        sequences.append([seq - sequences[-1][i - 1] for i, seq in enumerate(sequences[-1][1:], 1)])
    for i in reversed(range(len(sequences) - 1)):
        sequences[i].append(sequences[i][-1] + sequences[i + 1][-1])
    return sequences[0][-1]

# Calculates the sum of next and previous values
def sum_of_next(puzzleinput):
    with open(puzzleinput, 'r') as file:
        histories = [list(map(int, line.split())) for line in file.read().splitlines()]
    return sum(extrapolate_value(history) for history in histories)

def sum_of_previous(puzzleinput):
    with open(puzzleinput, 'r') as file:
        histories = [list(map(int, line.split())) for line in file.read().splitlines()]
    return sum(extrapolate_value(history[::-1]) for history in histories)

if __name__ == "__main__":
    puzzleinput = "day9.txt"
    print("Solution to part 1 is:", sum_of_next(puzzleinput))
    print("Solution to part 2 is:", sum_of_previous(puzzleinput))