import os
import numpy as np
from tqdm import tqdm


with open(os.path.join('data', 'day09', 'example.txt'), 'r') as file:
    lines = [line.strip() for line in file.readlines()]
    coordinates = np.asarray([line.split(',') for line in lines]).astype(int)

def calculate_area(coordinate1, coordinate2):
    return (
        (abs(coordinate1[0] - coordinate2[0]) + 1) *
        (abs(coordinate1[1] - coordinate2[1]) + 1)
    )

areas = np.asarray([
    [
        calculate_area(coordinates[i], coordinates[j])
        for j in range(len(coordinates))
    ]
    for i in range(len(coordinates))
])

print(f'Largest area: {np.max(areas)}')