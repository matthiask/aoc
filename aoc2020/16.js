import { readFileSync } from "node:fs"
const input = readFileSync("16.txt", { encoding: "utf-8" })

const test = `\
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
`

const test2 = `\
class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
`

const parse = (input) => {
  const [ruleLines, myTicket, nearbyTickets] = input.split("\n\n")

  const rules = ruleLines.split("\n").map((line) => {
    const [name, rangePieces] = line.split(": ")
    const ranges = rangePieces
      .split(" or ")
      .map((range) =>
        range.split("-").map((number, idx) => Number(number) + idx),
      )
    return {
      name,
      ranges,
      test(number) {
        return ranges.some((range) => range[0] <= number && number < range[1])
      },
    }
  })

  return {
    rules,
    myTicket: myTicket.split("\n")[1].split(",").map(Number),
    nearbyTickets: nearbyTickets
      .split("\n")
      .filter(Boolean)
      .slice(1)
      .map((line) => line.split(",").map(Number)),
  }
}

const part1 = (input) => {
  const { rules, nearbyTickets } = parse(input)
  const allNumbers = nearbyTickets.flat()
  const invalidNumbers = allNumbers.filter(
    (number) => !rules.some((rule) => rule.test(number)),
  )
  // console.log(allNumbers, invalidNumbers)
  return invalidNumbers.reduce((a, b) => a + b, 0)
}

const part2 = (input) => {
  const { rules, myTicket, nearbyTickets } = parse(input)

  const validTickets = nearbyTickets.filter((ticket) =>
    ticket.every((number) => rules.some((rule) => rule.test(number))),
  )

  const possible = new Map(
    rules.map((_, idx) => [idx, new Set(rules.map((rule) => rule.name))]),
  )

  // console.debug(validTickets)
  // console.debug(possible)

  validTickets.forEach((ticket) => {
    ticket.forEach((number, idx) => {
      rules.forEach((rule) => {
        if (!rule.test(number)) {
          possible.get(idx).delete(rule.name)
        }
      })
    })
  })

  // console.debug(possible)

  const fieldsToIndex = new Map()

  let foundAnother = true
  while (foundAnother) {
    foundAnother = false
    for (const [idx, names] of possible.entries()) {
      if (names.size === 1) {
        const name = Array.from(names)[0]
        fieldsToIndex.set(name, idx)
        for (const names of possible.values()) {
          names.delete(name)
        }
        foundAnother = true
      }
    }
  }

  console.log(fieldsToIndex)

  let result = 1
  Array.from(fieldsToIndex.entries()).forEach(([name, idx]) => {
    if (name.startsWith("departure")) result *= myTicket[idx]
  })

  return result
}

console.debug(parse(test))
console.log("part1 test", part1(test))
console.log("part1", part1(input))

console.log("part2 test", part2(test2))
console.log("part2", part2(input))
