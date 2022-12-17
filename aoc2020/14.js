import { readFileSync } from "fs"
const input = readFileSync("14.txt", { encoding: "utf-8" })

const test = `\
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
`

const dec2bin = (number) => (number >>> 0).toString(2)
const bin2dec = (number) => parseInt(number, 2)

const applyMask = (mask, number) => {
  const bin = Array.from(mask)
    .map((m, idx) => (m === "X" ? number[idx] : m))
    .join("")
  console.debug({ mask, number, bin })
  return bin2dec(bin)
}

const parse = (input) => {
  const program = []
  input
    .split("\n")
    .filter(Boolean)
    .forEach((line) => {
      const [left, right] = line.split(" = ")
      if (left == "mask") {
        program.push(["msk", 0, right])
      } else if (left.startsWith("mem[")) {
        program.push([
          "mem",
          Number(left.replace("mem[", "").replace("]", "")),
          dec2bin(Number(right)).padStart(36, "0"),
        ])
      } else {
        throw Error()
      }
    })
  return program
}

const part1 = (input) => {
  const program = parse(input)
  const memory = new Map()

  let mask = ""

  for (let [inst, op1, op2] of program) {
    if (inst == "msk") {
      mask = op2
    } else {
      memory.set(op1, applyMask(mask, op2))
    }
  }

  // console.debug(memory)
  return Array.from(memory.values()).reduce((a, b) => a + b, 0)
}

console.debug(parse(test))
console.debug("part1 test", part1(test))
console.debug("part1", part1(input))
