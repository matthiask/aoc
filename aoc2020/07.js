import { readFileSync } from "fs"

const input = readFileSync("07.txt", { encoding: "utf-8" })
const test = `\
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
`

const parse = (input) =>
  input
    .split("\n")
    .filter(Boolean)
    .map((rule) => {
      const matches = rule.match(/^(.+) bags contain (.*)$/, rule)
      const color = matches[1]
      const contains =
        matches[2] == "no other bags."
          ? []
          : matches[2].split(", ").map((bag) => {
              const matches = bag.match(/(\d+) (.+) bag/)
              return {
                count: Number(matches[1]),
                color: matches[2],
              }
            })
      return {
        color,
        contains,
        bags: contains.reduce((a, b) => a + b.count, 0),
      }
    })

// console.log(JSON.stringify(parse(input)))
// console.log()
// console.log(JSON.stringify(parse(test)))

// const modifier = "shiny"
// const color = "gold"

const part1 = (rules) => {
  const reverse = new Map()

  for (let rule of rules) {
    for (let contains of rule.contains) {
      const list = [...(reverse.get(contains.color) || []), rule]
      reverse.set(contains.color, list)
    }
  }

  // console.log(reverse)

  const colors = new Set()
  const _recurse = (color) => {
    for (let r of reverse.get(color) || []) {
      colors.add(r.color)
      _recurse(r.color)
    }
  }

  _recurse("shiny gold")
  console.log("part1", colors, colors.size)
}

part1(parse(test))
part1(parse(input))
