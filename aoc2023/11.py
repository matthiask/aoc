from itertools import combinations
from pprint import pp

from tools import manhattan_distance, open_input


def parse():
    return [line.strip() for line in open_input("11")]


def expand(universe):
    x = 0
    while x < len(universe[0]):
        if {line[x] for line in universe} == {"."}:
            for y in range(len(universe)):
                universe[y] = universe[y][: x + 1] + "." + universe[y][x + 1 :]
            x += 2
        else:
            x += 1

    y = 0
    while y < len(universe):
        if set(universe[y]) == {"."}:
            universe.insert(y + 1, universe[y])
            y += 2
        else:
            y += 1


def galaxies(universe):
    return {
        x + y * 1j
        for x in range(len(universe[0]))
        for y in range(len(universe))
        if universe[y][x] == "#"
    }


def solve1():
    universe = parse()
    expand(universe)
    distances = sum(
        manhattan_distance(a - b) for a, b in combinations(galaxies(universe), 2)
    )
    pp(("part1", distances))


# print("\n".join(IN))
# print()
# expand(IN)
# print("\n".join(IN))
# print(galaxies(IN))

solve1()
