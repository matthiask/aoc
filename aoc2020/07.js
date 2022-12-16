import { readFileSync } from "fs"

const input = readFileSync("07.txt", { encoding: "utf-8" })

const rules = input
  .split("\n")
  .filter(Boolean)
  .map((rule) => {
    const matches = rule.match(/^(.*?) bags contain (.*)$/, rule)
    const bag = matches[1]
    const contains =
      matches[2] == "no other bags."
        ? []
        : matches[2].split(", ").map((bag) => {
            const matches = bag.match(/(\d+) (.+?) bag/)
            return { count: Number(matches[1]), bag: matches[2] }
          })
    return { bag, contains }
  })

console.log(JSON.stringify(rules))
