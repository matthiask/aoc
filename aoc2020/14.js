import { readFileSync } from "node:fs"
const input = readFileSync("14.txt", { encoding: "utf-8" })

const test = `\
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
`

const test2 = `\
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
`

const dec2bin = (number) => (Number(number) >>> 0).toString(2).padStart(36, "0")
const bin2dec = (number) => Number.parseInt(number, 2)

const applyMask = (mask, number) => {
  const bin = Array.from(mask)
    .map((m, idx) => (m === "X" ? number[idx] : m))
    .join("")
  // console.debug({ mask, number, bin })
  return bin2dec(bin)
}

const parse = (input) => {
  const program = []
  input
    .split("\n")
    .filter(Boolean)
    .forEach((line) => {
      const [left, right] = line.split(" = ")
      if (left === "mask") {
        program.push(["msk", 0, right])
      } else if (left.startsWith("mem[")) {
        program.push([
          "mem",
          Number(left.replace("mem[", "").replace("]", "")),
          dec2bin(right),
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

  for (const [inst, op1, op2] of program) {
    if (inst === "msk") {
      mask = op2
    } else {
      memory.set(op1, applyMask(mask, op2))
    }
  }

  // console.debug(memory)
  return Array.from(memory.values()).reduce((a, b) => a + b, 0)
}

const allAddresses = (mask, number) => {
  number = dec2bin(number)
  const floating = []
  const num = Array.from(mask).map((m, idx) => {
    if (m === "X") {
      floating.push(idx)
    } else if (m === "0") {
      return number[idx]
    }
    return m
  })

  const floatingNumbers = 1 << floating.length
  const addresses = []
  for (let n = 0; n < floatingNumbers; ++n) {
    const bits = n.toString(2).padStart(floating.length, "0")
    // console.debug(bits)
    floating.forEach((index, idx) => {
      num[index] = bits[idx]
    })
    // console.debug(num)
    addresses.push(bin2dec(num.join("")))
  }

  // console.debug({ mask, number, floating, addresses })
  return addresses
}

const part2 = (input) => {
  const program = parse(input)
  const memory = new Map()

  let mask = ""

  for (const [inst, op1, op2] of program) {
    if (inst === "msk") {
      mask = op2
    } else {
      for (const address of allAddresses(mask, op1)) {
        memory.set(address, bin2dec(op2))
      }
    }
  }

  // console.debug(memory)
  return Array.from(memory.values()).reduce((a, b) => a + b, 0)
}

console.debug(parse(test))
console.debug("part1 test", part1(test))
console.debug("part1", part1(input))

console.debug("part2 test", part2(test2))
console.debug("part2", part2(input))
