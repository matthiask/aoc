#!/usr/bin/env node

import { readFileSync } from "fs"
const input = readFileSync("24.txt", { encoding: "utf-8" })

const test = `\
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
`

const adjacent = {
  e: [2, 0],
  se: [1, 1],
  sw: [-1, 1],
  w: [-2, 0],
  nw: [-1, -1],
  ne: [1, -1],
}

const parse = (input) => {
  const lines = input.trim().split("\n")
  return lines
}

const parseCoords = (coords) => coords.split(",").map(Number)

const getAdjacent = (coords) =>
  Object.values(adjacent).map((v) => [coords[0] + v[0], coords[1] + v[1]])

const getAdjacentAndSelf = (coords) => [coords, ...getAdjacent(coords)]

const solve = (input) => {
  let lines = parse(input)
  let black = new Set()
  for (let line of lines) {
    let coords = [0, 0]
    let re = /(se|sw|ne|nw|e|w)/g
    let match
    while ((match = re.exec(line))) {
      let d = adjacent[match[0]]
      coords[0] += d[0]
      coords[1] += d[1]
    }
    coords = coords.join(",")
    if (black.has(coords)) {
      black.delete(coords)
    } else {
      black.add(coords)
    }
  }
  // console.debug(black)
  console.log("part1", black.size)

  for (let i = 0; i < 100; ++i) {
    let check = Array.from(black).map(parseCoords).flatMap(getAdjacentAndSelf)

    // console.debug("check", check)

    black = new Set(
      check
        .map((coords) => [
          coords,
          black.has(coords.join(",")),
          getAdjacent(coords).filter((coords) => black.has(coords.join(",")))
            .length,
        ])
        .filter(
          ([_coords, isBlack, adjacentBlack]) =>
            (isBlack && (adjacentBlack === 1 || adjacentBlack === 2)) ||
            (!isBlack && adjacentBlack === 2),
        )
        .map(([coords]) => coords.join(",")),
    )

    // console.debug(i, black.size)
  }

  console.log("part2", black.size)
}

solve(test)
solve(input)
