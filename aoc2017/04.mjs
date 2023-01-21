import { readFileSync } from "fs"
const input = readFileSync("04.txt", { encoding: "utf-8" })

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
    .map((word) => {
      let counts = new Map()
      Array.from(word).forEach((char) => {
        counts.set(char, 1 + (counts.get(char) || 0))
      })
      counts = Array.from(counts.entries())
      let ret = counts
        .map(([char, count]) => `${char}${count}`)
        .sort()
        .join("")
      // console.debug({ word, ret, counts })
      return ret
    })
    .join(" ")
}

console.log(
  "part1",
  input.split("\n").filter(Boolean).filter(isValidPart1).length,
)
console.log(
  "part2",
  input.split("\n").filter(Boolean).map(rearrange).filter(isValidPart1).length,
)
