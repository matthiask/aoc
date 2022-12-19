const test = `\
.#.
..#
###
`

const input = `\
..#..##.
#.....##
##.#.#.#
..#...#.
.###....
######..
.###..#.
..#..##.
`

const key = (...values) => values.map((v) => `${v}`).join(",")
const unkey = (key) => key.split(",").map(Number)

const parse = (input, zero) => {
  const points = new Set()
  input
    .split("\n")
    .filter(Boolean)
    .forEach((line, y) =>
      Array.from(line).forEach((char, x) => {
        if (char === "#") points.add(key(x, y, ...zero))
      }),
    )
  return points
}

/*
// https://stackoverflow.com/a/43053803
const cartesian = (...a) =>
  a.reduce((a, b) => a.flatMap((d) => b.map((e) => [d, e].flat())))
*/

const cartesian = (head, ...tail) => {
  const next = tail.length ? cartesian(...tail) : [[]]
  const results = []
  for (let h of head) {
    for (let n of next) {
      results.push([h, ...n])
    }
  }
  return results
}

const neighbors = (point) => {
  const neighbors = []
  const values = unkey(point)

  const pool = [-1, 0, 1]
  const deltas = cartesian(...values.map((_) => pool))

  deltas.forEach((delta) => {
    if (!delta.every((idx) => !idx))
      neighbors.push(key(...values.map((v, idx) => v + delta[idx])))
  })
  // console.debug({ point, neighbors, values, deltas })
  return neighbors
  // return [...neighbors.slice(0, 13), ...neighbors.slice(14)]
}

/*
const neighbors = (point) => {
  const neighbors = []
  const [x, y, z] = unkey(point)
  for (let i = -1; i <= 1; ++i) {
    for (let j = -1; j <= 1; ++j) {
      for (let k = -1; k <= 1; ++k) {
        if (!i && !j && !k) {
          continue
        }
        neighbors.push(key(x + i, y + j, z + k))
      }
    }
  }
  // console.debug({ point, neighbors })
  return neighbors
}
*/

const ranges = (points) => {
  const values = Array.from(points).map(unkey)
  const range = (dimension) => {
    const dimensionValues = values.map((v) => v[dimension])
    return [Math.min(...dimensionValues), Math.max(...dimensionValues)]
  }

  // console.log({ values })
  return values[0].map((_, idx) => range(idx))
}

const rangeInclusive = (start, end) => {
  const r = []
  for (; start <= end; ++start) {
    r.push(start)
  }
  // console.debug({ start, end, r })
  return r
}

const cycle = (points) => {
  const newPoints = new Set()

  const allRanges = ranges(points).map((r) =>
    rangeInclusive(r[0] - 1, r[1] + 1),
  )
  // console.debug(allRanges)
  const allPoints = cartesian(...allRanges).map((point) => key(point))
  // console.debug(allPoints)

  for (let point of allPoints) {
    const activeNeighbors = neighbors(point).filter((p) => points.has(p)).length
    if (points.has(point)) {
      // Active
      if (2 <= activeNeighbors && activeNeighbors <= 3) {
        newPoints.add(point)
      }
    } else {
      // Inactive
      if (activeNeighbors === 3) {
        newPoints.add(point)
      }
    }
  }

  return newPoints
}

const part1 = (input, zero) => {
  let points = parse(input, zero)
  console.debug("points at the start", points.size)
  for (let i = 0; i < 6; ++i) {
    points = cycle(points)
    console.debug("points after cycle", points.size)
  }
  return points.size
}

// console.debug(parse(test, [0]))
// console.debug(parse(input, [0]))

console.log("part1 test", part1(test, [0]))
console.log("part1", part1(input, [0]))

console.log("part2 test", part1(test, [0, 0]))
console.log("part2", part1(input, [0, 0]))
