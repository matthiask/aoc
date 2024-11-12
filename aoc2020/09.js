import { readFileSync } from "node:fs"
const input = readFileSync("09.txt", { encoding: "utf-8" })
const test = `\
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
`

const parse = (input) => input.split("\n").filter(Boolean).map(Number)

const isSumOfTwo = (sum, numbers) => {
  for (let i = 0, len = numbers.length; i < len; ++i) {
    for (let j = i + 1, len = numbers.length; j < len; ++j) {
      if (sum === numbers[i] + numbers[j]) {
        return true
      }
    }
  }
  return false
}

const part1 = (numbers, preamble) => {
  for (let i = preamble, len = numbers.length; i < len; ++i) {
    if (!isSumOfTwo(numbers[i], numbers.slice(i - preamble, i))) {
      // console.log(i, numbers[i])
      return numbers[i]
    }
  }
}

const sum = (numbers) => numbers.reduce((a, b) => a + b, 0)

const part2 = (numbers, weakness) => {
  for (let i = 0, len = numbers.length; i < len; ++i) {
    for (let j = i, len = numbers.length; j < len; ++j) {
      const slice = numbers.slice(i, j)
      if (sum(slice) === weakness) {
        return Math.max(...slice) + Math.min(...slice)
      }
    }
  }
}

let numbers
let weakness

numbers = parse(test)
weakness = part1(numbers, 5)
console.log("part1 test", weakness)
console.log("part2 test", part2(numbers, weakness))

numbers = parse(input)
weakness = part1(numbers, 25)
console.log("part1", weakness)
console.log("part2", part2(numbers, weakness))
