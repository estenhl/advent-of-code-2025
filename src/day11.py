import numpy as np
import os
from queue import PriorityQueue

with open(os.path.join('data', 'day11', 'example.txt'), 'r') as file:
    lines = [line.strip() for line in file.readlines()]
    connections = [
        {
            'source': line.split(':')[0],
            'destinations': line.split(': ')[1].split(' ')
        }
        for line in lines
    ]

# nodes = (
#     set([connection['source'] for connection in connections]) |
#     set([destination for connection in connections for destination in connection['destinations']])
# )

sources = set([connection['source'] for connection in connections])
destinations = set([
    destination for connection in connections
    for destination in connection['destinations']
])
nodes = sorted(list(sources | destinations))
print(nodes)

edges = np.zeros((len(nodes), len(nodes)), dtype=int)

for connection in connections:
    print(connection)
    for destination in connection['destinations']:
        print(destination)
        edges[nodes.index(connection['source']), nodes.index(destination)] = +1

if np.amax(edges) > 1:
    raise ValueError('Multiple connections to the same node')

def search(nodes, edges):
    start = nodes.index('you')
    end = nodes.index('out')

    queue = PriorityQueue()
    queue.put((0, start))

    histories = {
        start: {}
    }

    while queue:
        depth, current  = queue.get()
        paths = histories[current]['paths']
        trajectories = histories[current]['trajectories']
        histories[current] = None

        neighbours = np.where(edges[current] > 0)[0]

        for neighbour in neighbours:
            queue.put((depth + 1, neighbour))

            if neighbour not in histories:
                histories[neighbour] = {
                    'trajectories': [histories[current]['trajectories'] + [neighbour]],
                    'paths': paths
                }
            else:
                histories[neighbour]['trajectories'].append(histories[current]['trajectories'] + [neighbour])
                histories[neighbour]['paths'] += paths

search(nodes, edges)