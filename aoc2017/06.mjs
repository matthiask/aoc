import { readFileSync } from "fs"
import { numbers } from "./utils.mjs"
const input = numbers(readFileSync("06.txt", { encoding: "utf-8" }))

const redistribute = (blocks) => {
  let most = Math.max(...blocks)
  const index = blocks.indexOf(most)
  blocks = [...blocks]
  blocks[index] = 0
  for (let i = index + 1, len = blocks.length; most; --most, ++i) {
    ++blocks[i % len]
  }
  return blocks
}

const cycleAfter = (blocks) => {
  const seen = new Set()
  for (let i = 1; ; ++i) {
    blocks = redistribute(blocks)
    const key = blocks.join(",")
    if (seen.has(key)) return i
    seen.add(key)
  }
}

// console.debug(input)
// console.debug(redistribute(input))
//

console.debug("part1 test", cycleAfter([0, 2, 7, 0]))
console.debug("part1", cycleAfter(input))
