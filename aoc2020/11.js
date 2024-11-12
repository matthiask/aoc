import { readFileSync } from "node:fs"
const input = readFileSync("11.txt", { encoding: "utf-8" })

const test = `\
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
`

const parse = (input) =>
  input
    .split("\n")
    .filter(Boolean)
    .map((line) => Array.from(line))

const adjacentOccupiedCount = (grid, x, y) => {
  const yMax = grid.length
  const xMax = grid[0].length

  let count = 0
  for (let dy = -1; dy <= 1; ++dy) {
    for (let dx = -1; dx <= 1; ++dx) {
      if (dx === 0 && dy === 0) continue

      const ax = x + dx
      const ay = y + dy

      if (
        ax >= 0 &&
        ax < xMax &&
        ay >= 0 &&
        ay < yMax &&
        grid[ay][ax] === "#"
      ) {
        ++count
      }
    }
  }
  return count
}

const offsets = (i) => [
  [0, -i],
  [i, -i],
  [i, 0],
  [i, i],
  [0, i],
  [-i, i],
  [-i, 0],
  [-i, -i],
]

const occupiedSeatsIn8DirectionsOver = (grid, x, y, over) => {
  const yMax = grid.length
  const xMax = grid[0].length
  const max = Math.max(yMax, xMax)

  const char = (x, y) => (grid[y] ? grid[y][x] : ".")

  const seatSeen = [false, false, false, false, false, false, false, false]
  let count = 0
  for (let i = 1; i <= max; ++i) {
    offsets(i).forEach(([dx, dy], idx) => {
      if (seatSeen[idx]) return
      const ax = x + dx
      const ay = y + dy
      const c = char(ax, ay)
      if (c === ".") return
      seatSeen[idx] = true
      count += c === "#" ? 1 : 0
    })
    if (count > over) return true
  }
  return count > over
}

const round = (grid) => {
  let changed = false
  const newGrid = grid.map((row, y) =>
    row.map((character, x) => {
      // console.debug({ x, y, character, occupied: adjacentOccupiedCount(grid, x, y) })
      if (character === ".") {
        return character
      }
      if (character === "L") {
        return adjacentOccupiedCount(grid, x, y) === 0 && (changed = true)
          ? "#"
          : "L"
      }
      if (character === "#") {
        return adjacentOccupiedCount(grid, x, y) >= 4 && (changed = true)
          ? "L"
          : "#"
      }
    }),
  )
  return changed ? newGrid : grid
}

const occupiedSeats = (grid) => {
  let occupied = 0
  for (const row of grid) {
    for (const cell of row) {
      if (cell === "#") ++occupied
    }
  }
  return occupied
}

const printify = (grid) => grid.map((row) => row.join("")).join("\n")

const part1 = (grid) => {
  for (;;) {
    const newGrid = round(grid)
    if (newGrid === grid) {
      console.debug(printify(grid))
      return occupiedSeats(grid)
    }
    grid = newGrid
  }
}

const round2 = (grid) => {
  let changed = false
  const newGrid = grid.map((row, y) =>
    row.map((character, x) => {
      // console.debug({ x, y, character, occupied: adjacentOccupiedCount(grid, x, y) })
      if (character === ".") {
        return character
      }
      if (character === "L") {
        if (occupiedSeatsIn8DirectionsOver(grid, x, y, 0)) {
          return "L"
        }
        changed = true
        return "#"
      }
      if (character === "#") {
        return occupiedSeatsIn8DirectionsOver(grid, x, y, 4) && (changed = true)
          ? "L"
          : "#"
      }
    }),
  )
  return changed ? newGrid : grid
}

const part2 = (grid) => {
  for (;;) {
    const newGrid = round2(grid)
    if (newGrid === grid) {
      console.debug(printify(grid))
      return occupiedSeats(grid)
    }
    // console.log("looped once", new Date())
    grid = newGrid
  }
}
console.log("part1 test", part1(parse(test)))
console.log("part1", part1(parse(input)))

console.log("part2 test", part2(parse(test)))
console.log("part2", part2(parse(input)))
