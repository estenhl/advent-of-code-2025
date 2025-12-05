import numpy as np
import os
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components


with open(os.path.join('data', 'day05', 'input.txt'), 'r') as file:
    inputs = file.read().strip()

ranges, entries = inputs.split('\n\n')

ranges = ranges.split('\n')
entries = entries.split('\n')

ranges = np.asarray([list(map(int, range.split('-'))) for range in ranges])
entries = np.asarray([int(entry) for entry in entries])

valid = [
    entry for entry in entries
    if any(range[0] <= entry <= range[1] for range in ranges)
]

print(f'Fresh: {len(valid)}')

def determine_overlap(range1, range2):
    return (
        range1[0] <= range2[0] <= range1[1] or
        range1[0] <= range2[1] <= range1[1]
    )

def determine_overlaps(current, ranges):
    return [determine_overlap(current, range) for range in ranges]

def consolidate(ranges):
    return [np.amin(ranges), np.amax(ranges)]

def consolidate_ranges(ranges):
    overlaps = np.asarray(
        [determine_overlaps(range, ranges) for range in ranges]
    ).astype(int)
    overlaps = csr_matrix(overlaps)

    components = connected_components(overlaps)[1]
    components = [
        np.where(components == i)[0] for i in range(np.max(components) + 1)
    ]

    ranges = [
        consolidate(np.asarray(ranges[component])) for component in components
    ]

    return ranges

ranges = consolidate_ranges(ranges)
total = np.sum([range[1] - range[0] + 1 for range in ranges])
print(f'Total: {total}')
