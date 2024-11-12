import { readFileSync } from "node:fs"
const input = readFileSync("13.txt", { encoding: "utf-8" })

const test = `\
939
7,13,x,x,59,x,31,19
`

const parse = (input) => {
  const lines = input.split("\n").filter(Boolean)
  const earliest = Number(lines[0])
  const busLines = lines[1]
    .split(",")
    .filter((bus) => bus !== "x")
    .map(Number)
  return { earliest, busLines }
}

const earliestBusDeparture = (earliest, busLines) => {
  const nextDepartures = busLines.map((bus) => [bus, bus - (earliest % bus)])
  nextDepartures.sort((a, b) => a[1] - b[1])
  // console.debug(nextDepartures)
  return nextDepartures[0]
}

const part1 = (log, input) => {
  const { earliest, busLines } = parse(input)
  // console.debug({ earliest, busLines })
  const res = earliestBusDeparture(earliest, busLines)
  console.log(log, res[0] * res[1])
}

part1("part1 test", test)
part1("part1", input)

const parseDepartureRules = (input) => {
  return input
    .split(",")
    .map((bus, offset) => (bus === "x" ? null : [Number(bus), offset]))
    .filter(Boolean)
}

// console.debug(parseDepartureRules(test))

const part2 = (log, input) => {
  const rules = parseDepartureRules(input)
  console.debug(rules)
  let time = 0
  let step = rules[0][0]
  let rule = 1
  let prevmatch = 0

  while (rule < rules.length) {
    time += step
    if ((time + rules[rule][1]) % rules[rule][0] === 0) {
      if (!prevmatch) {
        console.debug(`Found match for rule ${rule} at ${time}`)
        prevmatch = time

        if (rule + 1 === rules.length) {
          console.log(log, time)
          return
        }
      } else {
        step = time - prevmatch
        prevmatch = 0
        console.debug(`Found new step size ${step}`)
        ++rule
      }
    }
  }
}

part2("part2 test", "17,x,13,19")
part2("part2 test", "67,7,59,61")
part2("part2 test", "67,x,7,59,61")
part2("part2 test", "67,7,x,59,61")
part2("part2 test", "1789,37,47,1889")
part2(
  "part2",
  "17,x,x,x,x,x,x,x,x,x,x,37,x,x,x,x,x,439,x,29,x,x,x,x,x,x,x,x,x,x,13,x,x,x,x,x,x,x,x,x,23,x,x,x,x,x,x,x,787,x,x,x,x,x,x,x,x,x,41,x,x,x,x,x,x,x,x,19",
)
