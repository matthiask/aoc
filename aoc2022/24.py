"""
O = (0, 0)
(Offset each axis by 1 to make modulo calculations easier)

    #.#####
    #O....#
    #>....#
    #.....#
    #...v.#
    #.....#
    #####.#
"""

from dataclasses import dataclass
from itertools import count
from typing import List


_directions = {
    "^": -1j,
    ">": 1 + 0j,
    "v": 1j,
    "<": -1 + 0j,
}
_moves = {0} | set(_directions.values())

_move_cost = {
    1j: 1,
    1: 1,
    0: 2,
    -1j: 3,
    -1: 3,
}


@dataclass
class Blizzard:
    initial: complex
    direction: str
    bounds: List[int]

    def at(self, step):
        d = _directions[self.direction]
        x = self.initial.real + d.real * step
        y = self.initial.imag + d.imag * step
        return complex(x % self.bounds[0], y % self.bounds[1])


@dataclass
class Puzzle:
    blizzards: List[Blizzard]
    bounds: List[int]
    entry: complex
    exit: complex


def parse(inp) -> Puzzle:
    lines = inp.strip().split("\n")
    entry = complex(lines[0].index(".") - 1, -1)
    exit = complex(lines[-1].index(".") - 1, len(lines) - 2)

    bounds = [len(lines[0]) - 2, len(lines) - 2]

    blizzards = [
        Blizzard(complex(x - 1, y - 1), c, bounds)
        for y, line in enumerate(lines)
        for x, c in enumerate(line)
        if c in _directions
    ]

    return Puzzle(blizzards, bounds, entry, exit)


def pretty(puzzle, blizzards):
    lines = [
        "#" * (puzzle.bounds[0] + 2),
    ]
    lines = [
        "#{}#".format(
            "".join(blizzards.get(complex(x, y), ".") for x in range(puzzle.bounds[0]))
        )
        for y in range(puzzle.bounds[1])
    ]
    lines.insert(
        0,
        "".join(
            "." if puzzle.entry.real + 1 == x else "#"
            for x in range(puzzle.bounds[0] + 2)
        ),
    )
    lines.append(
        "".join(
            "." if puzzle.exit.real + 1 == x else "#"
            for x in range(puzzle.bounds[0] + 2)
        )
    )
    print("\n".join(lines))
    print()


def _test_animate_blizzards(puzzle):
    import time

    for step in count():
        b = {blizzard.at(step): blizzard.direction for blizzard in puzzle.blizzards}
        pretty(puzzle, b)
        time.sleep(0.5)


def solve(puzzle):
    now = [puzzle.entry]
    step = 0

    while now:
        step += 1
        b = {blizzard.at(step) for blizzard in puzzle.blizzards}
        next = {pos + move for pos in now for move in _moves}
        now = []
        for pos in next:
            if pos == puzzle.exit:
                return step
            if (
                (0 <= pos.real < puzzle.bounds[0] and 0 <= pos.imag < puzzle.bounds[1])
                or pos in {puzzle.entry, puzzle.exit}
            ) and pos not in b:
                now.append(pos)

        # print("len", len(heap))


if __name__ == "__main__":
    import sys

    inp = open(sys.argv[1] if len(sys.argv) > 1 else "24.txt").read()
    puzzle = parse(inp)

    # _test_animate_blizzards(puzzle)
    print(puzzle)
    print(solve(puzzle))
