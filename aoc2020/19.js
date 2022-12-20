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
    return (rules, messageChars) => {
      // console.debug({ string, messageChars })
      if (messageChars[0] === string[1]) {
        messageChars.shift()
        return true
      }
      return false
    }
  }

  const variants = spec
    .split("|")
    .map((variant) => variant.trim().split(" ").filter(Boolean).map(Number))
  console.debug({ variants })
  return (rules, messageChars) => {
    for (let variant of variants) {
      if (variant.every((number) => rules.get(number)(rules, messageChars)))
        return true
    }
    return false
  }
}

const isValid = (rules, message) => {
  const check = rules.get(0),
    messageChars = Array.from(message)
  return check(rules, messageChars) && !messageChars.length
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

const { rules, messages } = parse(test)
console.debug(rules)

for (let message of messages) {
  console.debug(message, isValid(rules, message))
}
