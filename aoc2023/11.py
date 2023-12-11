from itertools import combinations
from pprint import pp

from tools import manhattan_distance, open_input


def parse():
    return [line.strip() for line in open_input("11")]


def expand1(universe):
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
    expand1(universe)
    distances = sum(
        manhattan_distance(a - b) for a, b in combinations(galaxies(universe), 2)
    )
    pp(("part1", distances))


def expand2(universe, by):
    distance_x = [1 for _ in universe[0]]
    distance_y = [1 for _ in universe]
    for y, line in enumerate(universe):
        if set(line) == {"."}:
            distance_y[y] = by
    for x, _c in enumerate(universe[0]):
        if {line[x] for line in universe} == {"."}:
            distance_x[x] = by
    return distance_x, distance_y


def solve2():
    universe = parse()
    distance_x, distance_y = expand2(universe, 1000000)
    galaxies = {
        sum(distance_x[:x]) + sum(distance_y[:y]) * 1j
        for x in range(len(universe[0]))
        for y in range(len(universe))
        if universe[y][x] == "#"
    }
    distances = sum(manhattan_distance(a - b) for a, b in combinations(galaxies, 2))
    pp(("part2", distances))


# print("\n".join(IN))
# print()
# expand(IN)
# print("\n".join(IN))
# print(galaxies(IN))

solve1()
solve2()
