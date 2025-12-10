import os
import numpy as np
from queue import PriorityQueue
from tqdm import tqdm


with open(os.path.join('data', 'day10', 'example.txt'), 'r') as file:
    lines = [line.strip() for line in file.readlines()]

parse_goal = lambda s: [{'.': 0, '#': 1}[c] for c in s[1:-1]]
parse_buttons = lambda l: [
    [int(x) for x in substr[1:-1].split(',')] for substr in l
]
parse_joltage = lambda s: np.asarray([int(x) for x in s[1:-1].split(',')])

entries = [
    {
        'goal': parse_goal(line.split(' ')[0]),
        'buttons': parse_buttons(line.split(' ')[1:-1]),
        'joltage': parse_joltage(line.split(' ')[-1]),
    }
    for line in lines
]

def transform_binary_state(state, button):
    mask = np.zeros(len(state), dtype=int)
    mask[button] = 1
    new_state = state ^ mask

    return new_state

def transform_accumulator_state(state, button):
    mask = np.zeros(len(state), dtype=int)
    mask[button] = 1
    new_state = state + mask

    return new_state

def exclude_larger(current_state, goal_state):
    if np.any(current_state > goal_state):
        return True

    return False

def breadth_first_search(goal_state, buttons, state_transformer, state_filter=None):
    queue = [(np.zeros(len(goal_state), dtype=int), 0)]
    visited = set()

    while queue:
        current_state, depth = queue.pop(0)
        if state_filter is not None:
            print(f'{goal_state}: {current_state}')
            raise ValueError()

        if tuple(current_state) in visited:
            continue

        if (
            state_filter is not None and
            state_filter(current_state, goal_state)
        ):
            continue

        visited.add(tuple(current_state))

        if np.array_equal(current_state, goal_state):
            return depth

        for button in buttons:
            new_state = state_transformer(current_state, button)
            queue.append((new_state, depth + 1))

def heuristic(state, goal_state, depth):
    return np.sum(goal_state - state) + depth

def astar(goal_state, buttons, state_transformer, state_filter=None):
    queue = PriorityQueue()
    visited = set()

    initial_state = tuple(np.zeros(len(goal_state), dtype=int))
    queue.put((heuristic(initial_state, goal_state, 0), initial_state, 0))

    while queue:
        _, current_state, depth = queue.get()
        current_state = np.asarray(current_state)

        print(f'{goal_state}: {current_state}')

        if tuple(current_state) in visited:
            continue

        if (
            state_filter is not None and
            state_filter(current_state, goal_state)
        ):
            continue

        visited.add(tuple(current_state))

        if np.array_equal(current_state, goal_state):
            return depth

        for button in buttons:
            new_state = state_transformer(current_state, button)
            queue.put((
                heuristic(new_state, goal_state, depth + 1),
                tuple(new_state),
                depth + 1
            ))

light_toggles = [
    breadth_first_search(
        goal_state=entry['goal'],
        buttons=entry['buttons'],
        state_transformer=transform_binary_state
    )
    for entry in entries
]

print(f'Light toggles: {np.sum(light_toggles)}')

print([entries[0]['joltage']])
joltage_toggles = [
    astar(
        goal_state=entry['joltage'],
        buttons=entry['buttons'],
        state_transformer=transform_accumulator_state,
        state_filter=exclude_larger
    )
    for entry in tqdm(entries)
]

print(f'Joltage toggles: {np.sum(joltage_toggles)}')
