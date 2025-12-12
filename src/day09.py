import os
import numpy as np
from functools import reduce
from tqdm import tqdm
import matplotlib
matplotlib.use('Agg')


with open(os.path.join('data', 'day09', 'input.txt'), 'r') as file:
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

def add_padding(value: int) -> Tuple[int, int, int]:
    return value - 1, value, value + 1

x_indices = [add_padding(x) for x in np.unique(coordinates[:,0])]
y_indices = [add_padding(y) for y in np.unique(coordinates[:,1])]
x_indices = sorted(set(reduce(lambda a, b: a + b, x_indices)))
y_indices = sorted(set(reduce(lambda a, b: a + b, y_indices)))
tiles = np.zeros((len(y_indices), len(x_indices)))


wrapped_coordinates = np.concatenate(
    [coordinates, np.expand_dims(coordinates[0], axis=0)]
)

for i in range(len(wrapped_coordinates) - 1):
    first = wrapped_coordinates[i]
    second = wrapped_coordinates[i + 1]

    xs = [x_indices.index(x) for x in [first[0], second[0]]]
    ys = [y_indices.index(y) for y in [first[1], second[1]]]

    x_range = np.arange(np.amin(xs), np.amax(xs) + 1)
    y_range = np.arange(np.amin(ys), np.amax(ys) + 1)

    tiles[y_range, x_range] = 1

for i in range(tiles.shape[0]):
    if np.all(tiles[i] != 1):
        tiles[i] = 2
        continue

    first, last = np.where(tiles[i] == 1)[0][[0, -1]]
    tiles[i, 0:first] = 2
    tiles[i, (last + 1):] = 2

tiles = np.where(tiles == 2, 0, 1)
import matplotlib.pyplot as plt
plt.imshow(tiles)
plt.savefig('tiles.png')

def calculate_tiled_area(tiles, coordinate1, coordinate2):
    xs = [x_indices.index(x) for x in [coordinate1[0], coordinate2[0]]]
    ys = [y_indices.index(y) for y in [coordinate1[1], coordinate2[1]]]

    x_range = np.arange(np.amin(xs), np.amax(xs) + 1)
    y_range = np.arange(np.amin(ys), np.amax(ys) + 1)

    if np.all(
        tiles[
            np.amin(ys):np.amax(ys) + 1,
            np.amin(xs):np.amax(xs) + 1
        ] == 1
    ):
        area = calculate_area(coordinate1, coordinate2)
        return area

    return 0

tiled_areas = np.asarray([
    [
        calculate_tiled_area(tiles, coordinates[i], coordinates[j])
        for j in range(len(coordinates))
    ]
    for i in tqdm(range(len(coordinates)))
])

print(f'Largest tiled area: {np.max(tiled_areas)}')
