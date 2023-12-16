import sys
from pprint import pp

from tools import open_input


IN = open_input("16").read().strip().split("\n")
W = len(IN[0])
H = len(IN)
GRID = {complex(x, y): IN[y][x] for y in range(H) for x in range(W)}
# pp(GRID)


def travel(beams):
    for prev, direction in beams:
        xy = prev + direction

        if not (0 <= xy.real < W and 0 <= xy.imag < H):
            # Outside grid
            continue

        c = GRID[xy]
        # pp({xy: c})
        if (c == ".") or (c == "-" and direction.real) or (c == "|" and direction.imag):
            yield (xy, direction)
        elif (c == "/" and direction.imag) or (c == "\\" and direction.real):
            # Turn to the right
            yield (xy, direction * 1j)
        elif (c == "/" and direction.real) or (c == "\\" and direction.imag):
            # Turn to the left
            yield (xy, direction * -1j)
        elif (c == "-" and direction.imag) or (c == "|" and direction.real):
            # Split
            yield (xy, direction * 1j)
            yield (xy, direction * -1j)
        else:
            raise Exception(c)


def print_visited(visited):
    print(
        "\n".join(
            "".join("#" if x + y * 1j in visited else "." for x in range(W))
            for y in range(H)
        )
    )


def send_beam(beam):
    visited = set()
    max_grace = grace = W * H // 50  # Heuristic
    beams = {beam}

    # for _ in range(100):
    while grace:
        beams = set(travel(beams))
        # pp(beams)
        if new_visited := {beam[0] for beam in beams} - visited:
            visited |= new_visited
            grace = max_grace
        else:
            grace -= 1
        sys.stdout.write(f"{grace} ")
        sys.stdout.flush()
    print()
    return visited


def solve1():
    visited = send_beam((-1, 1))
    # pp(("visited", visited))
    print_visited(visited)
    pp(("part1", len(visited)))


def solve2():
    max_visited = 0
    for x in range(W):
        max_visited = max(
            max_visited,
            len(send_beam((x - 1j, 1j))),
            len(send_beam((x + H * 1j, -1j))),
        )
        print({"x": x, "max_visited": max_visited})
    for y in range(H):
        max_visited = max(
            max_visited,
            len(send_beam((y - 1, 1))),
            len(send_beam((y + H, -1))),
        )
        print({"y": y, "max_visited": max_visited})
    pp(("part2", max_visited))


solve1()
solve2()
