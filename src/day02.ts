import { readFileSync } from 'fs';

const input: [number, number][] = readFileSync('data/day02/input.txt', 'utf8')
  .trim()
  .split(',')
  .map(range => range.split('-').map(Number) as [number, number]);

function isRepeated(number: number, max_repeats?: number) {
  const numStr = number.toString();

  for (let end = 1; end <= (numStr.length / 2) + 1; end++) {
    const subStr = numStr.slice(0, end);

    if (subStr.repeat(2) === numStr) {
      return true;
    }

    const allowedRepeats = max_repeats ?? Math.floor(numStr.length / subStr.length);

    for (let repeats = 2; repeats <= allowedRepeats; repeats++) {
      if (subStr.repeat(repeats) === numStr) {
        return true;
      }
    }
  }

  return false;
}

const doubles = input.map<number>(([start, end]: [number, number]) => {
  const numbers = Array.from({ length: end - start + 1 }, (_, i) => start + i);
  const repeated = numbers.filter(number => isRepeated(number, 2))

  return repeated.reduce((acc, curr) => acc + curr, 0)
});

const totalDoubles = doubles.reduce((acc, curr) => acc + curr, 0)

console.log(`Sum of doubles: ${totalDoubles}`)

const repeats = input.map<number>(([start, end]: [number, number]) => {
  const numbers = Array.from({ length: end - start + 1 }, (_, i) => start + i);
  const repeated = numbers.filter(number => isRepeated(number))

  return repeated.reduce((acc, curr) => acc + curr, 0)
});

const totalRepeats = repeats.reduce((acc, curr) => acc + curr, 0)

console.log(`Sum of repeats: ${totalRepeats}`)