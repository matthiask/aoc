import { readFileSync } from "node:fs"

const input = readFileSync("06.txt", { encoding: "utf-8" })

const groups = input
  .split("\n\n")
  .map((group) => {
    const set = new Set(Array.from(group.replace(/[^a-z]+/g, "")))
    return set.size
  })
  .reduce((a, b) => a + b)
console.log("part1", groups)

const union = (a, b) =>
  new Set(Array.from(a.values()).filter((value) => b.has(value)))

const groups2 = input
  .split("\n\n")
  .map((group) => {
    const items = group.split("\n").map((item) => new Set(Array.from(item)))
    return items.reduce(union).size
  })
  .reduce((a, b) => a + b)
console.log("part2", groups2)
