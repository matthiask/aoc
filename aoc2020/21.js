import { readFileSync } from "fs"
const input = readFileSync("21.txt", { encoding: "utf-8" })

const test = `\
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
`

const parse = (input) => {
  return input
    .trim()
    .split("\n")
    .map((line) => {
      const parts = line.split(/[ ()]+/).filter(Boolean)
      const contains = parts.indexOf("contains")
      const ingredients = parts.slice(0, contains)
      const allergens = parts.slice(contains + 1)

      return { ingredients, allergens }
    })
}

console.debug(parse(test))
