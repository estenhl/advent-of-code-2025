import numpy as np
import os


with open(os.path.join('data', 'day07', 'input.txt'), 'r') as file:
    board = np.asarray([list(line.strip()) for line in file.readlines()])

current_beams = {np.where(board[0] == 'S')[0][0]: 1}
splits = 0

def _add_count(new_beams, beam, count):
    if beam in new_beams:
        new_beams[beam] += count
    else:
        new_beams[beam] = count

for i in range(len(board)):
    new_beams = {}

    for beam, count in current_beams.items():
        if board[i][beam] == '^':
            splits += 1
            _add_count(new_beams, beam - 1, count)
            _add_count(new_beams, beam + 1, count)
        else:
            _add_count(new_beams, beam, count)
    current_beams = new_beams

print(f'Splits: {splits}')
print(f'Timelines: {np.sum(list(current_beams.values()))}')
