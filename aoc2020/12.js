import { readFileSync } from "fs"
const input = readFileSync("12.txt", { encoding: "utf-8" })

const test = `\
F10
N3
F7
R90
F11
`

const parse = (input) =>
  input
    .split("\n")
    .filter(Boolean)
    .map((line) => ({ mode: line[0], value: Number(line.substring(1)) }))

const ship = { direction: "E", east: 0, north: 0 }
const directions = ["N", "E", "S", "W"]

const simulate = (ship, instructions) => {
  return instructions.reduce((ship, { mode, value }) => {
    // console.debug(ship)
    if (mode == "F") {
      mode = ship.direction
    }
    switch (mode) {
      case "N":
        return { ...ship, north: ship.north + value }
      case "E":
        return { ...ship, east: ship.east + value }
      case "S":
        return { ...ship, north: ship.north - value }
      case "W":
        return { ...ship, east: ship.east - value }
      case "R":
        return {
          ...ship,
          direction:
            directions[(directions.indexOf(ship.direction) + value / 90) % 4],
        }
      case "L":
        return {
          ...ship,
          direction:
            directions[
              (directions.indexOf(ship.direction) + 4 - value / 90) % 4
            ],
        }
      default:
        throw Error(`Unknown mode ${mode}`)
    }
  }, ship)
}

const manhattanDistanceTraveled = (ship) =>
  Math.abs(ship.east) + Math.abs(ship.north)

const rotate = (waypoint, degrees) => {
  const cos = Math.cos((degrees / 180) * Math.PI)
  const sin = Math.sin((degrees / 180) * Math.PI)

  return {
    east: waypoint.east * cos - waypoint.north * sin,
    north: waypoint.east * sin + waypoint.north * cos,
  }
}

const simulate2 = (instructions) => {
  const ship = { east: 0, north: 0 }
  let waypoint = { east: 10, north: 1 }
  for (let { mode, value } of instructions) {
    switch (mode) {
      case "N":
        waypoint.north += value
        break
      case "E":
        waypoint.east += value
        break
      case "S":
        waypoint.north -= value
        break
      case "W":
        waypoint.east -= value
        break
      case "R":
        waypoint = rotate(waypoint, -value)
        break
      case "L":
        waypoint = rotate(waypoint, value)
        break
      case "F":
        ship.east += value * waypoint.east
        ship.north += value * waypoint.north
        break
      default:
        throw Error(`Unknown mode ${mode}`)
    }
  }
  return ship
}

// console.log(parse(test))
// console.log(simulate(ship, parse(test)))

console.log(
  "part1 test",
  manhattanDistanceTraveled(simulate(ship, parse(test))),
)
console.log("part1", manhattanDistanceTraveled(simulate(ship, parse(input))))

console.log("part2 test", manhattanDistanceTraveled(simulate2(parse(test))))
console.log("part2", manhattanDistanceTraveled(simulate2(parse(input))))
