from itertools import chain
from pprint import pp

from tools import neighbors, open_input


G = {
    x + y * 1j: c
    for y, line in enumerate(open_input("21").read().strip().split("\n"))
    for x, c in enumerate(line)
}
S = next(xy for xy, c in G.items() if c == "S")
# pp(G)
# pp(S)


def solve1(r):
    places = {S}
    for _ in range(r):
        places = set(
            chain.from_iterable(
                (
                    xy
                    for xy in neighbors(prev, diagonal=False)
                    if G.get(xy) in {".", "S"}
                )
                for prev in places
            )
        )
    pp(("part1", len(places)))


solve1(64)
solve1(65)
solve1(65 + 131)
solve1(65 + 131 * 2)
