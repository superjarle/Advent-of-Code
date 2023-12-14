import numpy as np
import collections
import time

# Leser input filen
# --------------------
# Filen har hele input. Her er hver linje en rad i grid, med char som 
# representerer hver celle i en grid

puzzleinput = 'input.txt'
with open(puzzleinput, 'r') as file:
    lines = [line.rstrip() for line in file]

# Start timer for del 2 og
start_time_total = time.time()

# Starter timer
start_time_part1 = time.time()

# Del 1: Tilt nordover og finn load 
# ---------------------------------------
# Her deler vi opp tilitingen nordover før vi beregner "load" 
# Tilting nordover involverer å flytte sener ('O') så langt de kan

# Starter matrisen hvor vi konverterer hver linje til en matrise
# Lager en 2D array hvor hvert element er en celle i en grid
matrix_part1 = np.array([list(line) for line in lines])

# Tilter nordover 
def tilt_north(matrix):
    # Transponerer til å jobbe med kolonner som rader
    matrix = np.transpose(matrix)
    new_matrix = []
    # Prosesserer hver rad (originalt en kolonne)
    for l in matrix:
        # Deler opp raden etter kube-stener ('#') og prosesserer hvert segment
        line = ''.join(l)
        line = line.split('#')
        new_line = []
        for item in line:
            # Teller og flytter runde-stener ('O') og tomme områder ('.')
            c = collections.Counter(item)
            new_line.append('O' * c['O'] + '.' * c['.'])
        line = new_line
        new_matrix.append(list('#'.join(line)))
    # Transponerer tilbake til originalen
    return np.transpose(new_matrix)

# Utførelsen
matrix_part1 = tilt_north(matrix_part1)
del1 = 0
for i, l in enumerate(matrix_part1):
    del1 += list(l).count('O') * (len(matrix_part1) - i)

# Avslutter tidtaking
end_time_part1 = time.time()
execution_time_part1 = end_time_part1 - start_time_part1

print(f"Svaret for del 1 er: {del1}")
print(f"Tiden det tok for del 1 er: {execution_time_part1:.2f} sekunder")


# Del2 
# --------------------------------------------------
# Denne delen tar den i alle 4 himmelretninger og beregner load etter
# At den har gjort alle roteringene

# Start tiden for del 2 
start_time_part2 = time.time()


# Funskjon for a tilte vestover
def tilt_west(matrix):
    new_matrix = []
    for l in matrix:
       # Deler opp raden etter kube-stener ('#') og prosesserer hvert segment
        line = ''.join(l)
        line = line.split('#')
        new_line = []
        for item in line:
           # Teller og flytter runde-stener ('O') og tomme områder ('.')
            c = collections.Counter(item)
            new_line.append('O' * c['O'] + '.' * c['.'])
        line = new_line
        new_matrix.append(list('#'.join(line)))
    return np.array(new_matrix)

# Tilte nord, sor, ost og vest
def tilt_north(matrix):
    matrix = np.transpose(matrix)
    matrix = tilt_west(matrix)
    return np.transpose(matrix)

def tilt_south(matrix):
    matrix = np.flipud(matrix)
    matrix = tilt_north(matrix)
    return np.flipud(matrix)

def tilt_east(matrix):
    matrix = np.fliplr(matrix)
    matrix = tilt_west(matrix)
    return np.fliplr(matrix)

# Funskjon for a finne loaden 
def calculate_load(matrix):
    total_load = 0
    for i, l in enumerate(matrix):
        total_load += np.count_nonzero(l == 'O') * (len(matrix) - i)
    return total_load

# Tilter og beregner seriene 
def perform_tilts_and_calculate(matrix, num_iterations):
    for _ in range(num_iterations):
        matrix = tilt_north(matrix)
        matrix = tilt_west(matrix)
        matrix = tilt_south(matrix)
        matrix = tilt_east(matrix)
    return calculate_load(matrix)



# Lager matrisen for del 2 og
matrix_part2 = np.array([list(line) for line in lines])


# Regne ut del 2
load_p2 = perform_tilts_and_calculate(matrix_part2, 1001)

# Slutt for del 2
end_time_part2 = time.time()

# Slutttid for totalen
end_time_total = time.time()

# Regne ut brukt tid
execution_time_part2 = end_time_part2 - start_time_part2
execution_time_total = end_time_total - start_time_total


print(f"Løsningen for del 2 er: {load_p2}")
print(f"Tid tatt for del 2 er : {execution_time_part2:.2f} sekunder")
print(f"Total tid for hele run er: {execution_time_total:.2f} sekunder")




