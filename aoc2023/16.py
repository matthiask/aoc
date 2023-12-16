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


def solve1():
    visited = set()
    beams = {(-1, 1)}
    max_grace = grace = W * H // 10

    # for _ in range(100):
    while grace:
        beams = set(travel(beams))
        # pp(beams)
        if new_visited := {beam[0] for beam in beams} - visited:
            visited |= new_visited
            grace = max_grace
        else:
            grace -= 1
        print(grace)

    # pp(("visited", visited))
    print_visited(visited)
    pp(("part1", len(visited)))


solve1()
