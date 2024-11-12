import { readFileSync } from "node:fs"
const input = readFileSync("05.txt", { encoding: "utf-8" })
  .split("\n")
  .filter(Boolean)
  .map(Number)

// console.debug(input)

const part1 = () => {
  const program = [...input]
  let ip = 0
  for (let i = 1; ; ++i) {
    ip += program[ip]++

    if (0 <= ip && ip < program.length) continue
    console.log("part1", i)
    break
  }
}

const part2 = () => {
  const program = [...input]
  let ip = 0
  for (let i = 1; ; ++i) {
    const o = program[ip]
    if (o >= 3) {
      --program[ip]
    } else {
      ++program[ip]
    }
    ip += o

    if (0 <= ip && ip < program.length) continue
    console.log("part2", i)
    break
  }
}

part1()
part2()
