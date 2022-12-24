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


_directions = {
    "^": -1j,
    ">": 1 + 0j,
    "v": 1j,
    "<": -1 + 0j,
}


@dataclass
class Blizzard:
    initial: complex
    direction: str
    bounds: list[int]

    def at(self, step):
        d = _directions[self.direction]
        x = self.initial.real + d.real * step
        y = self.initial.imag + d.imag * step
        return complex(x % self.bounds[0], y % self.bounds[1])


def modulo(c1, c2):
    return complex(c1.real % c2.real, c1.imag % c2.imag)


def parse(inp):
    lines = inp.strip().split("\n")
    entry = complex(lines[0].index(".") - 1, -1)
    exit = complex(lines[-1].index(".") - 1, len(lines) - 1)

    bounds = [len(lines[0]) - 2, len(lines) - 2]

    blizzards = [
        Blizzard(complex(x - 1, y - 1), c, bounds)
        for y, line in enumerate(lines)
        for x, c in enumerate(line)
        if c in _directions
    ]

    return blizzards, bounds, entry, exit


def pretty(blizzards, bounds, entry, exit):
    lines = [
        "#" * (bounds[0] + 2),
    ]
    lines = [
        "#{}#".format(
            "".join(blizzards.get(complex(x, y), ".") for x in range(bounds[0]))
        )
        for y in range(bounds[1])
    ]
    lines.insert(
        0, "".join("." if entry.real + 1 == x else "#" for x in range(bounds[0] + 2))
    )
    lines.append(
        "".join("." if exit.real + 1 == x else "#" for x in range(bounds[0] + 2))
    )
    print("\n".join(lines))
    print()


def _test_animate_blizzards(blizzards, bounds, entry, exit):
    import time

    for step in count():
        b = {blizzard.at(step): blizzard.direction for blizzard in blizzards}
        pretty(b, bounds, entry, exit)
        time.sleep(0.5)


if __name__ == "__main__":
    import sys

    inp = open(sys.argv[1] if len(sys.argv) > 1 else "24.txt").read()
    parse(inp)
    blizzards, bounds, entry, exit = parse(inp)

    _test_animate_blizzards(blizzards, bounds, entry, exit)
