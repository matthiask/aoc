import { readFileSync } from "fs"
const input = readFileSync("19.txt", { encoding: "utf-8" })

const test = `
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
`

const parseSpec = (rules, spec) => {
  // console.debug({ spec })
  const string = spec.match(/"(.)"/)
  if (string) {
    const char = string[1]
    return (rules, messageChars, index) => {
      // console.debug({ string, messageChars })
      if (messageChars[index] === char) {
        return index + 1
      }
      return index
    }
  }

  const variants = spec
    .split("|")
    .map((variant) => variant.trim().split(" ").filter(Boolean).map(Number))
  // console.debug({ variants })
  return (rules, messageChars, index) => {
    for (let variant of variants) {
      let now = index,
        next,
        matches = true
      for (let number of variant) {
        next = rules.get(number)(rules, messageChars, now)
        if (next > now) {
          now = next
        } else {
          matches = false
        }
      }
      if (matches) {
        return next
      }
    }
    return index
  }
}

const isValid = (rules, message) => {
  const rootRule = rules.get(0),
    messageChars = Array.from(message)
  const consumed = rootRule(rules, messageChars, 0)
  return consumed == messageChars.length
}

const parse = (input) => {
  const [ruleLines, messages] = input.split("\n\n")

  const rules = new Map()
  ruleLines
    .split("\n")
    .filter(Boolean)
    .forEach((ruleLine) => {
      const [number, spec] = ruleLine.split(":")
      // console.debug({ ruleLine, number, spec })

      rules.set(Number(number), parseSpec(rules, spec))
    })

  return {
    rules,
    messages: messages.split("\n").filter(Boolean),
  }
}

const part1 = (log, input) => {
  const { rules, messages } = parse(input)
  // console.debug(rules)

  console.log(log, messages.filter((message) => isValid(rules, message)).length)
}

part1("part1 test", test)
part1("part1", input)
