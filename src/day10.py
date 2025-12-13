from curses import BUTTON1_PRESSED
import os
import numpy as np
from functools import reduce
from itertools import product
from queue import PriorityQueue
from tqdm import tqdm


with open(os.path.join('data', 'day10', 'example.txt'), 'r') as file:
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

def bifurcate_step(current_state, buttons):
    print(current_state)
    if np.array_equal(current_state, np.zeros_like(current_state)):
        return 0

    if np.any(current_state < 0):
        return np.inf

    possible_presses = list(product((0, 1), repeat=len(buttons)))
    configurations = [
        [buttons[i] for i, press in enumerate(presses) if press == 1]
        for presses in possible_presses[1:]
    ]
    changes = [
        np.bincount(
            reduce(lambda x, y: x + y, configuration, []),
            minlength=len(current_state)
        )
        for configuration in configurations
    ]
    #print(buttons)
    #for i in range(len(changes)):
        #print(f'{possible_presses[i]} -> {configurations[i]} -> {changes[i]}')
    evens = [
        (current_state - change, len(configurations[i]))
        for i, change in enumerate(changes)
        if (
            np.all((current_state - change) % 2 == 0) and
            np.all(change <= current_state)
        )
    ]

    return np.amin([
        (
            2 * bifurcate_step(current_state - change, buttons) +
            len(configurations[i])
        )
        for change, configuration in evens
    ])

def bifurcate(goal_state, buttons):
    return bifurcate_step(goal_state, buttons)

joltage_toggles = [
    bifurcate(
        goal_state=entry['joltage'],
        buttons=entry['buttons']
    )
    for entry in tqdm(entries)
]

print(f'Joltage toggles: {np.sum(joltage_toggles)}')
