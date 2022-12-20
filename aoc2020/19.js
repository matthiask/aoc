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
      if (messageChars[0] === string[0]) {
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
    isValid: (message) => rules.get(0)(rules, Array.from(message)),
    messages: messages.split("\n").filter(Boolean),
  }
}

const { rules, isValid, messages } = parse(test)
console.debug(rules)

for (let message of messages) {
  console.debug(message, isValid(message))
}
