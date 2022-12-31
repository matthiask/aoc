#!/usr/bin/env node

import { readFileSync } from "fs"
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
  const foods = [...puzzle.foods]
  foods.sort((a, b) => a.allergens.size - b.allergens.size)

  const knowledge = new Map()
  for (let food of foods) {
    for (let allergen of food.allergens) {
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
    Array.from(knowledge.values())
      .map((ingredients) => Array.from(ingredients))
      .flat(),
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
}

part1("part1 test", test)
part1("part1", input)
