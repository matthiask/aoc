import { readFileSync } from "fs"
const input = readFileSync("04.txt", { encoding: "utf-8" })
  .split("\n")
  .filter(Boolean)

const isValidPart1 = (line) => {
  let seen = new Set()
  for (let word of line.split(" ")) {
    if (seen.has(word)) return false
    seen.add(word)
  }
  return true
}

const rearrange = (line) => {
  return line
    .split(" ")
    .map((word) => Array.from(word).sort().join(""))
    .join(" ")
}

console.log("part1", input.filter(isValidPart1).length)
console.log("part2", input.map(rearrange).filter(isValidPart1).length)
