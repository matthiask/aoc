from dataclasses import dataclass


@dataclass
class Puzzle:
    east: set[complex]
    south: set[complex]
    bounds: tuple[int, int]

    def occupied(self):
        return self.east | self.south


def parse(lines):
    east = {
        complex(x, y)
        for y, line in enumerate(lines)
        for x, c in enumerate(line.strip())
        if c == ">"
    }
    south = {
        complex(x, y)
        for y, line in enumerate(lines)
        for x, c in enumerate(line.strip())
        if c == "v"
    }
    return Puzzle(
        east,
        south,
        (
            len(lines[0].strip()),
            len(lines),
        ),
    )


def step(puzzle):
    occupied = puzzle.occupied()
    puzzle.east = {
        orig if new in occupied else new
        for orig, new in (
            (orig, complex((orig.real + 1) % puzzle.bounds[0], orig.imag))
            for orig in puzzle.east
        )
    }
    occupied = puzzle.occupied()
    puzzle.south = {
        orig if new in occupied else new
        for orig, new in (
            (orig, complex(orig.real, (orig.imag + 1) % puzzle.bounds[1]))
            for orig in puzzle.south
        )
    }


def pretty(puzzle):
    print(
        "\n".join(
            "".join(
                ">" if xy in puzzle.east else "v" if xy in puzzle.south else "."
                for xy in (complex(x, y) for x in range(puzzle.bounds[0]))
            )
            for y in range(puzzle.bounds[1])
        )
    )
    print()


def solve1(puzzle):
    rounds = 0
    occupied = puzzle.occupied()
    while True:
        step(puzzle)
        rounds += 1
        new_occupied = puzzle.occupied()
        if new_occupied == occupied:
            break
        occupied = new_occupied
        print("rounds", rounds)
    print("part1", rounds)


def animate(puzzle):
    import time
    from itertools import count

    for round in count():
        print("Round", round)
        pretty(puzzle)
        time.sleep(0.5)
        step(puzzle)


if __name__ == "__main__":
    import sys

    puzzle = parse([*open(sys.argv[1] if len(sys.argv) > 1 else "25.txt")])

    # print(puzzle)
    solve1(puzzle)

    # animate(puzzle)
