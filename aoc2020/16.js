import { readFileSync } from "fs"
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

const parse = (input) => {
  const [ruleLines, myTicket, nearbyTickets] = input.split("\n\n")

  const rules = {}
  ruleLines.split("\n").forEach((line) => {
    const [name, rangePieces] = line.split(": ")
    const ranges = rangePieces
      .split(" or ")
      .map((range) =>
        range.split("-").map((number, idx) => Number(number) + idx),
      )
    rules[name] = {
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
    (number) => !Object.values(rules).some((rule) => rule.test(number)),
  )
  // console.log(allNumbers, invalidNumbers)
  return invalidNumbers.reduce((a, b) => a + b, 0)
}

console.debug(parse(test))
console.log("part1 test", part1(test))
console.log("part1", part1(input))
