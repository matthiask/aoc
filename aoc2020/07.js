import { readFileSync } from "fs"

const input = readFileSync("07.txt", { encoding: "utf-8" })

const rules = input
  .split("\n")
  .filter(Boolean)
  .map((rule) => {
    const matches = rule.match(/^(.+) (.+) bags contain (.*)$/, rule)
    const modifier = matches[1]
    const color = matches[2]
    const contains =
      matches[3] == "no other bags."
        ? []
        : matches[3].split(", ").map((bag) => {
            const matches = bag.match(/(\d+) (.+) (.+) bag/)
            return {
              count: Number(matches[1]),
              modifier: matches[2],
              color: matches[3],
            }
          })
    return { modifier, color, contains }
  })

console.log(JSON.stringify(rules))
