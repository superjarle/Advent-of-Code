# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 06:44:22 2023

@author: jkv
"""

class HistoryExtrapolator:
    def __init__(self, history):
        self.history = history
        self.sequences = self._generate_difference_sequences()

    def _generate_difference_sequences(self):
        sequences = [self.history]

        while sequences[-1].count(0) != len(sequences[-1]):
            new_sequence = [sequences[-1][i+1] - sequences[-1][i] for i in range(len(sequences[-1])-1)]
            sequences.append(new_sequence)

        return sequences

    def extrapolate(self, direction='next'):
        for i in range(len(self.sequences) - 2, -1, -1):
            if direction == 'next':
                self.sequences[i].append(self.sequences[i][-1] + self.sequences[i+1][-1])
            elif direction == 'previous':
                self.sequences[i].insert(0, self.sequences[i][0] - self.sequences[i+1][0])

        if direction == 'next':
            return self.sequences[0][-1]
        elif direction == 'previous':
            return self.sequences[0][0]
        
    def load_data(file_path):
        with open(file_path, 'r') as file:
            data = file.readlines()
        return [list(map(int, line.split())) for line in data]

# Load the data
file_path = 'day9.txt'
histories = load_data(file_path)


part1 = 0
part2 = 0
for history in histories:
    extrapolator = HistoryExtrapolator(history)
    next_value = extrapolator.extrapolate('next')
    prev_value = extrapolator.extrapolate('previous')
    part1 += next_value
    part2 += prev_value

part1, part2
