const input = 289326

//
// circle 0: 1
// circle 1: 8
// circle 2: 16
// circle 3: 24
// etc.
//

const circle = (input) => {
  let circle = 0,
    sum = 1

  for (;;) {
    const current = (circle + 1) * 2 * 4

    if (sum + current >= input) {
      break
      // return { circle, current, offset: input - sum }
    }

    ++circle
    sum += current
  }

  for (;;) {
    if (sum + circle >= input) {
      break
    }

    sum += circle
  }

  let remainder = Math.abs(circle / 2 - (sum % circle))

  return circle + remainder
}

console.debug(circle(input))
