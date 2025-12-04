import { readFileSync } from 'fs';

const input: string[] = readFileSync('data/day03/input.txt', 'utf8')
  .trim()
  .split('\n')

function findLargest(str: string, start: number, end?: number): [number, number] {
  let largest = 0;
  let largestIndex = 0;

  if (end === undefined || end > str.length) {
    end = str.length;
  }

  for (let i = start; i < end; i++) {
    const current = parseInt(str[i] ?? '0');
    if (current > largest) {
      largest = current;
      largestIndex = i;
    }
  }
  return [largest, largestIndex];
}

function findCombination(str: string, count: number) {
  let start = 0
  let entry = 0
  let total = 0

  for (let i = 0; i < count; i++) {
    const end = str.length - (count - (i + 1))
    let values = findLargest(str, start, end)
    entry = values[0]
    start = values[1] + 1
    total += entry * Math.pow(10, count - (i + 1))
  }

  return total
}

const pairs = input.map((str) => findCombination(str, 2));
const total = pairs.reduce((acc, curr) => acc + curr, 0);
console.log(`Total with 2 entries: ${total}`);

const twelves = input.map((str) => findCombination(str, 12));
const totalTwelves = twelves.reduce((acc, curr) => acc + curr, 0);
console.log(`Total with 12 entries: ${totalTwelves}`);