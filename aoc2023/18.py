from dataclasses import dataclass
from pprint import pp

from tools import neighbors, open_input


DIR = {"U": -1j, "D": 1j, "L": -1, "R": 1}
DIR_2 = {"0": 1, "1": 1j, "2": -1, "3": -1j}


@dataclass
class Step:
    dir: complex
    dist: int

    @classmethod
    def from_line(cls, line):
        dir, dist, _rgb = line.split()
        return cls(
            dir=DIR[dir],
            dist=int(dist),
        )

    @classmethod
    def from_2(cls, line):
        _, _, rgb = line.split()
        return cls(
            dir=DIR_2[rgb[7]],
            dist=int(rgb[2:7], 16),
        )


def solve1():
    dig = list(map(Step.from_line, open_input("18").read().strip().split("\n")))
    pos = 0
    border = {pos}
    for step in dig:
        for _i in range(step.dist):
            pos += step.dir
            border.add(pos)

    # pp(dig)
    pp(border)

    # Offset of one for flood fill
    xr = int(min(p.real for p in border)) - 1, int(max(p.real for p in border)) + 1
    yr = int(min(p.imag for p in border)) - 1, int(max(p.imag for p in border)) + 1
    print("Dug out", len(border))
    print("Extent", xr, yr)

    flood = {complex(xr[0], yr[0])}
    # Frontier only contains those positions which were found by the last flood
    # fill step; all other positions cannot possibly find additional positions
    # (we'd only be rechecking the same positions over and over).
    frontier = set(flood)
    while True:
        next_frontier = set()
        for pos in frontier:
            if (
                new_positions := {
                    next_pos
                    for next_pos in neighbors(pos, diagonal=True)
                    if next_pos not in border
                    and xr[0] <= next_pos.real <= xr[1]
                    and yr[0] <= next_pos.imag <= yr[1]
                }
                - flood
            ):
                flood |= new_positions
                next_frontier |= new_positions
        if not next_frontier:
            break
        flood |= next_frontier
        frontier = next_frontier

    print("Extent", (xr[1] - xr[0] + 1) * (yr[1] - yr[0] + 1) - len(flood))


# def solve2():
#     dig = list(map(Step.from_2, open_input("18").read().strip().split("\n")))
#     pos = 0
#     border = {pos}
#     for step in dig:
#         for _i in range(step.dist):
#             pos += step.dir
#             border.add(pos)
#
#     # pp(dig)
#     pp(border)


solve1()
# solve2()
