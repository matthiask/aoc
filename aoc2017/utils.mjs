export const sum = (numbers, initial = 0) =>
  numbers.reduce((a, b) => a + b, initial)

export const numbers = (line) => [...line.matchAll(/[-\d]+/g)].map(Number)
