import { readFileSync } from 'fs';

const input: string[][] = readFileSync('data/day04/input.txt', 'utf8')
  .trim()
  .split('\n')
  .map(line => line.split(''));

function countAdjacent(map: string[][], i: number, j: number) {
  let count = 0;
  for (let x = -1; x <= 1; x++) {
    for (let y = -1; y <= 1; y++) {
      if (x === 0 && y === 0) {
        continue;
      }
      else if (
        i + x < 0 ||
        i + x >= map.length ||
        j + y < 0 ||
        j + y >= map[i + x]!.length
      ) {
        continue;
      }
      else if (map[i + x]?.[j + y] != '.') {
        count++;
      }
    }
  }
  return count;
}

function move(map: string[][]): [number, string[][]] {
  const grid = map.map(row => [...row]);
  let movable = 0;

  for (let i = 0; i < grid.length; i++) {
    for (let j = 0; j < grid[i]!.length; j++) {
      if (grid[i]![j] === '@') {
        let adjacent = countAdjacent(grid, i, j);
        if (adjacent < 4) {
          movable++;
          grid[i]![j] = 'X';
        }
      }
    }
  }

  return [movable, grid];
}

let [movable, grid]: [number, string[][]] = move(input);
console.log(`Movable after first iteration: ${movable}`);

let total = movable

while (movable > 0) {
  grid = grid.map(row => row.map(cell => cell === 'X' ? '.' : cell));
  [movable, grid] = move(grid);
  total += movable;
}

console.log(`Total movable: ${total}`);