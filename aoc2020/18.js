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

const evaluateSumThenMul = (tokens) => {
  let factors = [null]
  let operator = null
  while (tokens.length) {
    const token = tokens.shift()
    // console.debug({ tokens: JSON.stringify(tokens), factors, operator, token })
    if (token === "(") {
      tokens.unshift(evaluateSumThenMul(tokens))
    } else if (token === ")") {
      break
    } else if (factors[0] === null) {
      factors[0] = token
    } else if (operator === null && token === "+") {
      operator = operators[token]
    } else if (operator === null && token === "*") {
      factors.unshift(null)
    } else {
      factors[0] = operator(factors[0], token)
      operator = null
    }
  }
  return factors.reduce((a, b) => a * b, 1)
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
    console.debug(evaluateSumThenMul(tokenize(calculation)))
  }
}

runTests()

const part1 = (log, input, ev = evaluate) => {
  console.log(
    log,
    input
      .split("\n")
      .filter(Boolean)
      .reduce((a, b) => a + ev(tokenize(b)), 0),
  )
}

part1("part1", input)
part1("part1", input, evaluateSumThenMul)

// console.debug(tokenize("1 + 2 * 3 + 4 * 5 + 6"))
// console.debug(evaluateSumThenMul(tokenize("1 + 2 * 3 + 4 * 5 + 6")))
// console.debug(evaluateSumThenMul(tokenize("5 + (8 * 3 + 9 + 3 * 4 * 3)")))
