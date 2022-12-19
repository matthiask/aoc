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

const neighbors = (point) => {
  const neighbors = []
  const values = unkey(point)

  const pool = [-1, 0, 1]
  const idxFun = values.map(
    (_, idx) => (i) => pool[Math.floor(i / Math.pow(pool.length, idx)) % 3],
  )
  for (let i = 0; i < Math.pow(pool.length, values.length); ++i) {
    neighbors.push(key(...idxFun.map((fn, idx) => values[idx] + fn(i))))
  }
  neighbors.splice(13, 1)
  return neighbors
  // console.debug({ point, neighbors })
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

  return values.map((_, idx) => range(idx))
}

const cycle = (points) => {
  const [xr, yr, zr] = ranges(points)
  const newPoints = new Set()

  for (let x = xr[0] - 1; x <= xr[1] + 1; x++) {
    for (let y = yr[0] - 1; y <= yr[1] + 1; y++) {
      for (let z = zr[0] - 1; z <= zr[1] + 1; z++) {
        const point = key(x, y, z)
        const activeNeighbors = neighbors(point).filter((p) =>
          points.has(p),
        ).length
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
    }
  }

  return newPoints
}

const part1 = (input, zero) => {
  let points = parse(input, zero)
  console.debug("points at the start", { points })
  for (let i = 0; i < 6; ++i) {
    points = cycle(points)
    console.debug("points after cycle", points.size)
  }
  return points.size
}

console.debug(parse(test, [0]))
console.debug(parse(input, [0]))

console.log("part1 test", part1(test, [0]))
console.log("part1", part1(input, [0]))

// console.log("part2 test", part1(test, [0, 0]))
// console.log("part2", part1(input, [0, 0]))
