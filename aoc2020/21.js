#!/usr/bin/env node

import { readFileSync } from "node:fs"
const input = readFileSync("21.txt", { encoding: "utf-8" })

const test = `\
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
`

// intersect can be simulated via
const intersection = (mySet1, mySet2) =>
  new Set([...mySet1].filter((x) => mySet2.has(x)))

// difference can be simulated via
const difference = (mySet1, mySet2) =>
  new Set([...mySet1].filter((x) => !mySet2.has(x)))

const parse = (input) => {
  const foods = input
    .trim()
    .split("\n")
    .map((line) => {
      const parts = line.split(/[ (),]+/).filter(Boolean)
      const contains = parts.indexOf("contains")
      const ingredients = new Set(parts.slice(0, contains))
      const allergens = new Set(parts.slice(contains + 1))

      // console.debug({ ingredients, allergens })
      return { ingredients, allergens }
    })

  const ingredients = new Set(
    foods.flatMap((food) => Array.from(food.ingredients)),
  )
  const allergens = new Set(foods.flatMap((food) => Array.from(food.allergens)))

  return { foods, ingredients, allergens }
}

const part1 = (log, input) => {
  const puzzle = parse(input)

  const knowledge = new Map()
  for (const food of puzzle.foods) {
    for (const allergen of food.allergens) {
      if (knowledge.has(allergen)) {
        knowledge.set(
          allergen,
          intersection(knowledge.get(allergen), food.ingredients),
        )
      } else {
        knowledge.set(allergen, food.ingredients)
      }
    }
  }

  // console.debug(knowledge)

  const maybeAllergenIngredients = new Set(
    Array.from(knowledge.values()).flatMap((ingredients) =>
      Array.from(ingredients),
    ),
  )
  const noAllergenIngredients = difference(
    puzzle.ingredients,
    maybeAllergenIngredients,
  )

  // console.debug({ maybeAllergenIngredients, noAllergenIngredients })

  console.log(
    log,
    puzzle.foods
      .map((food) => intersection(food.ingredients, noAllergenIngredients).size)
      .reduce((a, b) => a + b),
  )

  const identified = new Map()
  while (knowledge.size) {
    for (const [allergen, ingredients] of knowledge.entries()) {
      if (ingredients.size === 1) {
        const ingredient = Array.from(ingredients)[0]
        identified.set(allergen, ingredient)
        knowledge.delete(allergen)
        for (const ingredients of knowledge.values()) {
          ingredients.delete(ingredient)
        }
      }
    }
  }

  // console.debug(identified)

  console.log(
    "part2",
    Array.from(identified.entries())
      .sort()
      .map((a) => a[1])
      .join(","),
  )
}

part1("part1 test", test)
part1("part1", input)
