const test = [0, 3, 6]
const input = [6, 4, 12, 1, 20, 0, 16]

/*
const iterate = (sequence, rounds) => {
  const numbers = [...sequence]

  for (let i = sequence.length; i < rounds; ++i) {
    const index = numbers.slice(0, i - 1).lastIndexOf(numbers.at(-1))
    if (index < 0) {
      numbers.push(0)
    } else {
      numbers.push(i - index - 1)
    }
    // console.debug({ numbers: numbers.join(", "), last: numbers.at(-1), index })
    if (i % 100_000 == 0) console.debug(i, "iterations", new Date())
  }
  return numbers.at(-1)
}

console.log("part1 test", test, iterate(test, 10))
console.log("part1 test", test, iterate(test, 2020))
console.log("part1", input, iterate(input, 2020))
// console.log("part2", input, iterate(input, 30_000_000))
*/

const solve = (log, sequence, rounds) => {
  const numbers = new Map()
  for (let i = 0; i < sequence.length - 1; ++i) {
    numbers.set(sequence[i], 1 + i)
  }
  let lastNumber = sequence.at(-1)
  let number

  for (let i = sequence.length; i < rounds; ++i) {
    if (numbers.has(lastNumber)) {
      const round = numbers.get(lastNumber)
      number = i - round
    } else {
      number = 0
    }

    // console.log({ i, number })

    numbers.set(lastNumber, i)
    lastNumber = number
    // lastRound = round
  }
  console.log(log, { lastNumber, number })
}

solve("test", test, 2020)
solve("part1", input, 2020)
solve("part2", input, 30_000_000)
