import { readFileSync } from "fs"
const input = readFileSync("18.txt", { encoding: "utf-8" })

const regexp = /([0-9]*|[()+*]*|\s*)/g
const removeWS = (s) => s.replace(/\s+/g, "")
const tokenize = (calculation) =>
  removeWS(calculation)
    .split(regexp)
    .filter(Boolean)
    .map((token) => {
      switch (token) {
        case "(":
        case ")":
        case "+":
        case "*":
          return token
        default:
          if (/[0-9]+/.test(token)) return Number(token)
          throw Error()
      }
    })
const operators = {
  "+": (a, b) => a + b,
  "*": (a, b) => a * b,
}
const evaluate = (tokens) => {
  let result = null
  let operator = null

  while (tokens.length) {
    // console.debug({ tokens: JSON.stringify(tokens), result, operator })
    const token = tokens.shift()
    if (token === "(") {
      tokens.unshift(evaluate(tokens))
    } else if (token === ")") {
      break
    } else if (result === null) {
      result = token
    } else if (operator === null) {
      operator = operators[token]
    } else {
      result = operator(result, token)
      operator = null
    }
  }
  // console.debug("Returning", result)
  return result
}

/*
 */

const tests = [
  ["1 + 2 * 3 + 4 * 5 + 6", 71],
  ["1 + (2 * 3) + (4 * (5 + 6))", 51],
  ["2 * 3 + (4 * 5)", 26],
  ["5 + (8 * 3 + 9 + 3 * 4 * 3)", 437],
  ["5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 12240],
  ["((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 13632],
]

const runTests = () => {
  for (let [calculation, expected] of tests) {
    let calculated = evaluate(tokenize(calculation))
    console.debug(calculated, expected, calculated === expected)
  }
}

runTests()

const part1 = (log, input) => {
  console.log(
    log,
    input
      .split("\n")
      .filter(Boolean)
      .reduce((a, b) => a + evaluate(tokenize(b)), 0),
  )
}

part1("part1", input)

// console.debug(evaluate(tokenize(tests[5][0])))
