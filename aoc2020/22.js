#!/usr/bin/env node

import { readFileSync } from "fs"
const input = readFileSync("22.txt", { encoding: "utf-8" })

const test = `\
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
`

const parse = (input) => {
  const decks = input
    .trim()
    .split("\n\n")
    .map((player) => player.split("\n").slice(1).map(Number))
  return decks
}

const round = (decks) => {
  const top1 = decks[0].shift()
  const top2 = decks[1].shift()

  if (top1 > top2) {
    decks[0].push(top1, top2)
  } else {
    decks[1].push(top2, top1)
  }
}

const score = (deck) => {
  return deck
    .map((value, idx) => (deck.length - idx) * value)
    .reduce((a, b) => a + b)
}

const solve = (input) => {
  const decks = parse(input)

  // console.debug(decks)
  while (decks[0].length && decks[1].length) {
    round(decks)
  }
  // console.debug(decks)

  console.log("part1", score(decks[0].length ? decks[0] : decks[1]))
}

solve(test)
solve(input)
