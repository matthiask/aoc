import re
import sys


def tryint(v):
    try:
        return int(v)
    except Exception:
        return v


filename = sys.argv[1] if len(sys.argv) > 1 else "22.txt"
grid, moves = open(filename).read().rstrip().split("\n\n")
grid = grid.split("\n")
height = len(grid)
width = max(len(row) for row in grid)
moves = [tryint(v) for v in re.split(r"([A-Z])", moves) if v]
directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
print(grid)
print(moves)


direction = 0
pos = (grid[0].index("."), 0)


def at(pos):
    try:
        return grid[pos[1]][pos[0]]
    except IndexError:
        return " "


def add(a, b):
    x = a[0] + b[0]
    y = a[1] + b[1]
    wrapped = x < 0 or x >= width or y < 0 or y >= height

    return (x % width, y % height), wrapped


def next(pos):
    d = directions[direction]
    next_pos, wrapped = add(pos, d)
    c = at(next_pos)
    if c == " ":
        rd = directions[(direction + 2) % len(directions)]
        opposite = pos
        while True:
            next_opposite, wrapped = add(opposite, rd)
            print(next_opposite, repr(at(next_opposite)), wrapped)
            if at(next_opposite) == " " or wrapped:
                next_pos = opposite
                c = at(opposite)
                print(f"Found opposite, {c!r} at {next_pos}")
                break
            opposite = next_opposite

    if c == ".":
        return next_pos
    elif c == "#":
        return pos
    else:
        raise Exception(f"{c!r} at {pos}, don't know what to do.")


for move in moves:
    if move == "R":
        direction = (direction + 1) % len(directions)
    elif move == "L":
        direction = (direction - 1) % len(directions)
    else:
        for _ in range(move):
            pos = next(pos)

    print(pos)
    print((1 + pos[1]) * 1000 + (1 + pos[0]) * 4 + direction)
