from dataclasses import dataclass
from itertools import chain
from pprint import pp

from tools import neighbors, open_input


DIR = {"U": -1j, "D": 1j, "L": -1, "R": 1}


@dataclass
class Step:
    dir: complex
    dist: int
    rgb: tuple[int]

    @classmethod
    def from_line(cls, line):
        dir, dist, rgb = line.split()
        return cls(
            dir=DIR[dir],
            dist=int(dist),
            rgb=(
                int(rgb[2:4], 16),
                int(rgb[4:6], 16),
                int(rgb[6:8], 16),
            ),
        )


DIG = list(map(Step.from_line, open_input("18").read().strip().split("\n")))
pos = 0
G = {pos}
for step in DIG:
    for _i in range(step.dist):
        pos += step.dir
        G.add(pos)

# pp(DIG)
pp(G)

# Offset of one for flood fill
X = int(min(p.real for p in G)) - 1, int(max(p.real for p in G)) + 1
Y = int(min(p.imag for p in G)) - 1, int(max(p.imag for p in G)) + 1
print("Dug out", len(G))
print("Extent", X, Y)

flood = {complex(X[0], Y[0])}
while True:
    next_flood = flood | set(
        chain.from_iterable(
            (
                next_pos
                for next_pos in neighbors(pos, diagonal=True)
                if next_pos not in G
                and X[0] <= next_pos.real <= X[1]
                and Y[0] <= next_pos.imag <= Y[1]
            )
            for pos in flood
        )
    )
    if next_flood == flood:
        break
    flood = next_flood

print("Extent", (X[1] - X[0] + 1) * (Y[1] - Y[0] + 1) - len(flood))
