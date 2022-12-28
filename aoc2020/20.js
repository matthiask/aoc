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
  return {
    id,
    lines,
    cwEdges,
    ccwEdges,
    cw: cwEdges.map(edgeId),
    ccw: ccwEdges.map(edgeId),
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

const part1 = (log, input) => {
  const puzzle = parse(input)
  console.debug(puzzle)
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

part1("part1 test", test)
part1("part1", input)
