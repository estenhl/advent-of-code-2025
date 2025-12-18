from curses import BUTTON1_PRESSED
import os
import numpy as np
from functools import lru_cache, reduce
from itertools import product
from queue import PriorityQueue
from tqdm import tqdm


with open(os.path.join('data', 'day10', 'input.txt'), 'r') as file:
    lines = [line.strip() for line in file.readlines()]

parse_goal = lambda s: np.asarray([{'.': 0, '#': 1}[c] for c in s[1:-1]])
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

def heuristic(state, goal_state, depth):
    return np.sum(goal_state - state) + depth

def astar(goal_state, buttons, state_transformer):
    queue = PriorityQueue()
    visited = set()

    initial_state = tuple(0 for _ in range(len(goal_state)))
    queue.put((
        heuristic(initial_state, goal_state, 0),
        0,
        initial_state,
        0,
        buttons
    ))

    while not queue.empty():
        _, _, current_state, depth, valid_buttons = queue.get()

        if current_state in visited:
            continue

        visited.add(current_state)

        current_state = np.asarray(current_state)

        if np.array_equal(current_state, goal_state):
            return depth

        for button in buttons:
            new_state = state_transformer(current_state, button)
            queue.put((
                heuristic(new_state, goal_state, depth + 1),
                len(goal_state) - len(button),
                tuple(int(x) for x in new_state),
                depth + 1,
                valid_buttons
            ))

    raise ValueError(f'Unable to reach {goal_state} with {buttons}')

light_toggles = [
    astar(
        goal_state=entry['goal'],
        buttons=entry['buttons'],
        state_transformer=transform_binary_state
    )
    for entry in entries
]

print(f'Light toggles: {np.sum(light_toggles)}')

@lru_cache(maxsize=None)
def decomposition_step(current_state, buttons):
    current_state = np.asarray(current_state)

    if np.array_equal(current_state, np.zeros_like(current_state)):
        return 0

    possible_presses = list(product((0, 1), repeat=len(buttons)))
    configurations = [
        [buttons[i] for i, press in enumerate(presses) if press == 1]
        for presses in possible_presses
    ]
    changes = [
        (
            np.bincount(
                reduce(lambda x, y: x + y, configuration, tuple()),
                minlength=len(current_state)
            ),
            configuration
        )
        for configuration in configurations
    ]

    best_changes = {}

    for change, configuration in changes:
        key = tuple(change)
        if key not in best_changes or len(best_changes[key]) > len(configuration):
            best_changes[key] = configuration

    changes = [
        (np.asarray(change), configuration)
        for change, configuration in best_changes.items()
    ]

    evens = []
    for change, configuration in changes:
        remainder = current_state - change
        if not np.all(remainder % 2 == 0):
            continue
        if np.all(change == 0) and not np.all(current_state % 2 == 0):
            continue
        if np.any(remainder < 0):
            continue
        evens.append((remainder, configuration))

    if len(evens) == 0:
        return np.inf

    presses = []

    for new_state, configuration in evens:
        presses.append(
            2 *
            decomposition_step(
                tuple(int(x) for x in (new_state // 2)),
                buttons
            ) + len(configuration)
        )

    return np.amin(presses)

joltage_toggles = [
    decomposition_step(
        tuple(int(x) for x in entry['joltage']),
        tuple((tuple(configuration) for configuration in entry['buttons']))
    )
    for entry in tqdm(entries)
]

print(f'Joltage toggles: {np.sum(joltage_toggles)}')
