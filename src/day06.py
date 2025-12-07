import os
import numpy as np

with open(os.path.join('data', 'day06', 'input.txt'), 'r') as file:
    lines = [line for line in file.readlines()]
    longest = max(len(line) for line in lines)
    lines = [line + ' ' * (longest - len(line)) for line in lines]
    characters = np.asarray([list[str](line) for line in lines])
    rowwise = np.asarray([line.strip().split() for line in lines])

def apply(operator, values):
    if operator == '+':
        return np.sum(values)
    elif operator == '*':
        return np.prod(values)
    else:
        raise ValueError(f'Invalid operator: {operator}')


rowwise_answers = [
    apply(rowwise[-1, col], rowwise[:-1, col].astype(int))
    for col in range(rowwise.shape[1])
]

print(f'Row-wise sum: {np.sum(rowwise_answers)}')

values = characters[:-1]
operators = rowwise[-1]
columns = [''.join(values[:, col]) for col in range(characters.shape[1])]
columns = [column.replace('\n', '') for column in columns]
splits = np.where(np.asarray([column.strip() for column in columns]) == '')[0][:-1]
chunks = np.split(columns, splits)
chunks = [[int(value.strip()) for value in chunk if len(value.strip()) > 0] for chunk in chunks]

columnwise_answers = [
    apply(operators[col], chunks[col])
    for col in range(len(chunks))
]

print(f'Column-wise sum: {np.sum(columnwise_answers)}')