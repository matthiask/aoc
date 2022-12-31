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

const untilWin = (deck1, deck2) => {
  while (deck1.length && deck2.length) {
    round(deck1, deck2)
  }
}

const winningDeck = (deck1, deck2) => {
  untilWin(deck1, deck2)
  return deck1.length ? deck1 : deck2
}

// PART 2 ########################################

const round2 = (deck1, deck2) => {
  const top1 = deck1.shift()
  const top2 = deck2.shift()

  let winner

  if (top1 <= deck1.length && top2 <= deck2.length) {
    winner = playGame(deck1.slice(0, top1), deck2.slice(0, top2))
  } else {
    winner = top1 > top2 ? 1 : 2
  }

  if (winner === 1) {
    deck1.push(top1, top2)
  } else if (winner === 2) {
    deck2.push(top2, top1)
  } else {
    console.debug("Unexpected winner value", winner)
    throw Error()
  }
}

const playGame = (deck1, deck2) => {
  // console.debug("Playing game with", deck1, deck2)
  const memo = new Set()

  while (deck1.length && deck2.length) {
    const key = `${deck1.join(",")}|${deck2.join(",")}`
    if (memo.has(key)) {
      return 1
    }
    memo.add(key)

    round2(deck1, deck2)
  }

  return deck1.length ? 1 : 2
}

const score = (deck) => {
  return deck
    .map((value, idx) => (deck.length - idx) * value)
    .reduce((a, b) => a + b)
}

const solve = (input) => {
  let decks = parse(input)
  console.log("part1", score(winningDeck(...decks)))

  decks = parse(input)
  playGame(...decks)
  // console.debug(decks)
  console.log("part2", score(decks[0].length ? decks[0] : decks[1]))
}

solve(test)
solve(input)

/*
solve(`\
Player 1:
43
19

Player 2:
2
29
14
`)
*/
