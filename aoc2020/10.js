import { readFileSync } from "node:fs"
const input = readFileSync("10.txt", { encoding: "utf-8" })
const test1 = `\
16
10
15
5
1
11
7
19
6
12
4
`

const test2 = `\
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
`

const parse = (input) => input.split("\n").filter(Boolean).map(Number)

const maxJoltage = (joltages) => Math.max(...joltages) + 3

const joltageDifferences = (joltages) => {
  const differences = []
  const values = [...joltages, 0, maxJoltage(joltages)].sort((a, b) => a - b)
  for (let i = 1, len = values.length; i < len; ++i) {
    differences.push(values[i] - values[i - 1])
  }
  return differences
}

const countDifferences = (joltages) => {
  const differences = new Map()
  for (const diff of joltageDifferences(joltages)) {
    differences.set(diff, (differences.get(diff) || 0) + 1)
  }
  return differences
}

const part1 = (diff) => diff.get(1) * diff.get(3)

console.log("part1 test1", part1(countDifferences(parse(test1))))
console.log("part1 test2", part1(countDifferences(parse(test2))))
console.log("part1", part1(countDifferences(parse(input))))

const findRunsOfOnes = (joltages) => {
  const differences = joltageDifferences(joltages)
  let i = 0
  const runs = []

  // console.debug(differences)

  const _eatRun = () => {
    let length = 0
    while (differences[i] === 1) {
      ++i
      ++length
    }
    runs.push(length)
  }

  const _eatNoOnes = () => {
    while (differences[i] !== 1 && i < differences.length) {
      ++i
    }
  }

  while (i < differences.length) {
    _eatRun()
    _eatNoOnes()
  }

  console.debug(runs)
  return runs
}

const factors = new Map()
factors.set(1, 1)
factors.set(2, 2) // [1, 1] or [2]
factors.set(3, 4) // [3], [1, 1, 1], [1, 2], [2, 1]
factors.set(4, 7) //

const reduce = (runs) => runs.reduce((a, b) => a * factors.get(b), 1)

findRunsOfOnes(parse(test1))
console.log(reduce(findRunsOfOnes(parse(test1))))
findRunsOfOnes(parse(test2))
console.log(reduce(findRunsOfOnes(parse(test2))))
findRunsOfOnes(parse(input))
console.log(reduce(findRunsOfOnes(parse(input))))
