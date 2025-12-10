import numpy as np
import os
from collections import Counter
from sklearn.metrics.pairwise import euclidean_distances


STEPS = 1000

with open(os.path.join('data', 'day08', 'input.txt'), 'r') as file:
    lines = [line.strip() for line in file.readlines()]
    coordinates = np.asarray([line.split(',') for line in lines]).astype(int)

print(coordinates)
distances = euclidean_distances(coordinates)
distances = distances + np.diag(np.ones(len(coordinates)) * np.inf)
print(distances)
clusters = np.arange(len(coordinates))

for i in range(STEPS):
    smallest = np.unravel_index(np.argmin(distances), distances.shape)
    clusters[clusters == clusters[smallest[1]]] = clusters[smallest[0]]
    distances[smallest[0], smallest[1]] = np.inf
    distances[smallest[1], smallest[0]] = np.inf

counts = Counter(clusters)
counts = [(key, value) for key, value in counts.items()]
counts.sort(key=lambda x: x[1])

print(f'Product: {np.prod([count for _, count in counts[-3:]])}')

while len(np.unique(clusters)) > 1:
    smallest = np.unravel_index(np.argmin(distances), distances.shape)
    clusters[clusters == clusters[smallest[1]]] = clusters[smallest[0]]
    distances[smallest[0], smallest[1]] = np.inf
    distances[smallest[1], smallest[0]] = np.inf

print(smallest)
xs = [coordinates[idx, 0] for idx in smallest]
print(f'Xs: {np.prod(xs)}')