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

const round = (deck1, deck2) => {
  const top1 = deck1.shift()
  const top2 = deck2.shift()

  if (top1 > top2) {
    deck1.push(top1, top2)
  } else {
    deck2.push(top2, top1)
  }
}

const winningDeck = (deck1, deck2) => {
  while (deck1.length && deck2.length) {
    round(deck1, deck2)
  }
  return deck1.length ? deck1 : deck2
}

const score = (deck) => {
  return deck
    .map((value, idx) => (deck.length - idx) * value)
    .reduce((a, b) => a + b)
}

const solve = (input) => {
  const decks = parse(input)

  console.log("part1", score(winningDeck(...decks)))
}

solve(test)
solve(input)
