import { readFileSync } from 'fs';

const input: Array<[number, number]> = readFileSync('data/day01/input.txt', 'utf8')
  .trim()
  .split('\n')
  .map(line => [line[0] == 'L' ? -1 : 1, parseInt(line.slice(1))])

const start = 50;
const modulo = (n: number, m: number) => (n % m + m) % m;

const history: Array<[number, number]> = input.reduce<Array<[number, number]>>(
  (intermediate, [direction, steps]) => {
    var [position, passes] = intermediate[intermediate.length - 1] ?? [start, 0];
    var newPosition: number = position + direction * steps;

    var newPasses = 0

    if (newPosition >= 100) {
      newPasses = Math.floor(newPosition / 100);
    }
    if (newPosition <= 0) {
      newPasses = (position > 0 ? 1 : 0) + Math.floor(Math.abs(newPosition) / 100);
    }

    passes += newPasses

    return [...intermediate, [modulo(newPosition, 100), passes]]
}, [[start, 0]]);

const positions = history.map(([position, _]) => position);
const zeroPositions = positions.filter(position => position === 0);

console.log(`Zero positions: ${zeroPositions.length}`);

const passes = (history[history.length - 1] ?? [0, 0])[1];
console.log(`Zero passes: ${passes}`);