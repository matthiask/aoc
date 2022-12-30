import { readFileSync } from "fs"
const input = readFileSync("20.txt", { encoding: "utf-8" })

const test = `
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
`

const reverseString = (s) => [...s].reverse().join("")
const edgeId = (edge) =>
  parseInt(edge.replace(/#/g, "1").replace(/\./g, "0"), 2)

const parseTile = (tile) => {
  let [id, ...lines] = tile.split("\n")
  id = Number(id.replace(/Tile (.*):/, "$1"))
  const cwEdges = [
    lines[0],
    lines.map((line) => [...line].at(-1)).join(""),
    reverseString(lines.at(-1)),
    lines
      .map((line) => line[0])
      .reverse()
      .join(""),
  ]
  const ccwEdges = cwEdges.map(reverseString)
  const cw = cwEdges.map(edgeId)
  const ccw = ccwEdges.map(edgeId)
  const allIds = [...cw, ...ccw]
  return {
    id,
    lines,
    cw,
    ccw,
    allIds,
  }
}

const parse = (input) => {
  const tiles = input.trim().split("\n\n").map(parseTile)
  return {
    tiles,
    dimensions: Math.pow(tiles.length, 0.5),
  }
}

const countOccurrences = (iterable) => {
  const counts = new Map()
  for (let value of iterable) {
    counts.set(value, 1 + (counts.get(value) || 0))
  }
  return counts
}

const groupBy = (iterable) => {
  const groups = new Map()
  for (let [value, group] of iterable) {
    if (!groups.has(group)) groups.set(group, [])
    groups.get(group).push(value)
  }
  return groups
}

// https://stackoverflow.com/a/44012184
function* cartesian(head, ...tail) {
  const remainder = tail.length > 0 ? cartesian(...tail) : [[]]
  for (let r of remainder) for (let h of head) yield [h, ...r]
}

const part1Old = (log, input) => {
  const puzzle = parse(input)
  console.debug(puzzle)
  console.debug(
    "edge id count cw",
    new Set(puzzle.tiles.flatMap((tile) => tile.cw)).size,
  )
  console.debug(
    "edge id count ccw",
    new Set(puzzle.tiles.flatMap((tile) => tile.ccw)).size,
  )
  console.debug(
    "edge id count all",
    new Set(puzzle.tiles.flatMap((tile) => [tile.cw, tile.ccw]).flat()).size,
  )
  // console.log(log, messages.filter((message) => isValid(rules, message)).length)
  // console.debug("count", tiles.length)

  let outsideEdgeIds

  for (let edges of cartesian(
    ...puzzle.tiles.map((tile) => [tile.cw, tile.ccw]),
  )) {
    // console.log(edges)
    const edgeIdOccurrences = countOccurrences(edges.flat())
    const co = countOccurrences(edgeIdOccurrences.values())
    // console.debug(co)

    if (co.get(1) === puzzle.dimensions * 4) {
      console.debug("Found!", co, edges)
      const groups = groupBy(edgeIdOccurrences.entries())
      console.debug("Outside", groups.get(1))
      console.debug("Inside", groups.get(2))
      outsideEdgeIds = groups.get(1)
      break
    }
  }

  const outsideTiles = puzzle.tiles.filter(
    (tile) =>
      [...tile.cw, ...tile.ccw].filter((edgeId) =>
        outsideEdgeIds.includes(edgeId),
      ).length === 2,
  )
  // console.debug(outsideTiles)

  console.log(
    log,
    outsideTiles.reduce((a, b) => a * b.id, 1),
  )
}

// [0, 3] : Clockwise
// [4, 7] : Counterclockwise
const rotatedTile = (tile, rotation) => {
  if (rotation < 0) {
    throw Error()
  } else if (rotation < 4) {
    return tile.cw.map((_id, idx, array) => array[(idx + 4 - rotation) % 4])
  } else if (rotation < 8) {
    return tile.ccw.map((_id, idx, array) => array[(idx + 8 - rotation) % 4])
  } else {
    throw Error()
  }
}

function range(start, end) {
  return Array.from({ length: end - start }, (_, i) => i)
}

const neighbors = (puzzle, idx) => {
  const d = puzzle.dimensions
  const y = Math.floor(idx / d)
  const x = idx % d
  return [
    y > 0 ? x + (y - 1) * puzzle.dimensions : null,
    x < d - 1 ? x + 1 + y * puzzle.dimensions : null,
    y < d - 1 ? x + (y + 1) * puzzle.dimensions : null,
    x > 0 ? x - 1 + y * puzzle.dimensions : null,
  ]
}

// N: 0
// E: 1
// S: 2
// W: 3

const findPlaces = (puzzle) => {
  let result = null
  let unplacedAmount = puzzle.tiles.length

  const _placing = (placement, unplacedIndexes) => {
    if (result) {
      return
    }

    for (let idx of unplacedIndexes) {
      for (let rotation = 0; rotation < 8; ++rotation) {
        const edges = rotatedTile(puzzle.tiles[idx], rotation)

        if (
          neighbors(puzzle, placement.length).every((neighbor, idx) => {
            return (
              !neighbor ||
              neighbor >= placement.length ||
              edges[idx] === placement[neighbor][1][(idx + 2) % 4]
            )
          })
        ) {
          const newPlacement = [...placement, [idx, edges]]
          const newUnplacedIndexes = unplacedIndexes.filter((id) => id != idx)

          if (newUnplacedIndexes.length < unplacedAmount) {
            unplacedAmount = newUnplacedIndexes.length
            console.debug({ unplacedAmount, newUnplacedIndexes })

            if (unplacedAmount <= 0) {
              result = newPlacement
              return
            }
          }

          _placing(newPlacement, newUnplacedIndexes)
        }
      }
    }
  }

  const tileIndexes = range(0, puzzle.tiles.length)
  _placing([], tileIndexes)
  return result
}

const part1Old2 = (log, inp) => {
  const puzzle = parse(inp)
  const placement = findPlaces(puzzle)

  const d = puzzle.dimensions
  const corners = [0, d - 1, (d - 1) * d, d * d - 1]

  console.log(
    log,
    corners
      .map((idx) => puzzle.tiles[placement[idx][0]].id)
      .reduce((a, b) => a * b, 1),
  )
}

const intersects = (list1, list2) => {
  for (let el of list1) {
    if (list2.includes(el)) {
      return true
    }
  }
  return false
}

const part1 = (log, inp) => {
  const puzzle = parse(inp)
  const cornerIds = []

  for (let tile of puzzle.tiles) {
    let degree = 0
    for (let other of puzzle.tiles) {
      if (tile.id === other.id) continue
      if (intersects(tile.allIds, other.allIds)) {
        if (++degree > 2) break
      }
    }
    if (degree === 2) cornerIds.push(tile.id)
  }
  console.log(
    log,
    cornerIds.reduce((a, b) => a * b),
  )
}

part1("part1 test", test)
part1("part1", input)
