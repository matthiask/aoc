import { readFileSync } from "fs"
const input = readFileSync("08.txt", { encoding: "utf-8" })
const test = `\
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
`

const parse = (input) =>
  input
    .split("\n")
    .filter(Boolean)
    .map((line) => {
      const [instruction, operand] = line.split(" ")
      return [instruction, Number(operand)]
    })

const execute = (program) => {
  let ip = 0,
    acc = 0,
    lastIp = 0

  const ipCounter = Object.fromEntries(program.map((_, idx) => [idx, 0]))

  for (;;) {
    if (++ipCounter[ip] > 1) {
      throw Error(`duplicate execution at ${ip}, accumulator is ${acc}`)
    }
    const [instruction, operand] = program[ip] || ["trm", 0]

    // console.log({ ip, acc, instruction, operand })

    switch (instruction) {
      case "nop":
        break
      case "acc":
        acc += operand
        break
      case "jmp":
        lastIp = ip
        ip += operand
        continue
      case "trm":
        console.debug("orderly termination?", ip, lastIp, program.length)
        return acc
      default:
        throw Error(`unknown instruction ${instruction}`)
    }

    lastIp = ip++
  }
}

// console.log("part1 test", execute(parse(test)))
// console.log("part1", execute(parse(input)))

const program = parse(input)
for (let i = 0; i < program.length; ++i) {
  const modified = parse(input)

  if (program[i][0] == "jmp") {
    modified[i][0] = "nop"
  } else if (program[i][0] == "nop") {
    modified[i][0] = "jmp"
  } else {
    continue
  }

  try {
    const acc = execute(modified)
    console.log("part2", acc, program[i], modified[i])
  } catch (e) {
    /* nothing */
  }
}
