keypad = """\
1 2 3
4 5 6
7 8 9
"""

keypad = {
    (x, y): key
    for y, line in enumerate(keypad.strip().split("\n"))
    for x, key in enumerate(line.split())
}
directions = {
    "U": (0, -1),
    "D": (0, 1),
    "L": (-1, 0),
    "R": (1, 0),
}


def clamp(lo, v, hi):
    return min(hi, max(lo, v))


def interpret(line):
    x = y = 1
    for c in line:
        dx, dy = directions[c]
        x = clamp(0, x + dx, 2)
        y = clamp(0, y + dy, 2)
    return keypad[(x, y)]


IN = [*open("02.txt")]
print("".join(interpret(line.strip()) for line in IN))


keypad = """\
    1
  2 3 4
5 6 7 8 9
  A B C
    D
"""

keypad = {
    (x // 2 - 2, y - 2): key
    for y, line in enumerate(keypad.rstrip().split("\n"))
    for x, key in enumerate(line.rstrip())
    if key != " "
}
print(keypad)


def mh(xy):
    return sum(map(abs, xy))


def interpret2(line):
    x = -2
    y = 0
    for c in line:
        dx, dy = directions[c]
        nx = x + dx
        ny = y + dy
        if mh((nx, ny)) <= 2:
            x = nx
            y = ny
    return keypad[(x, y)]


print("".join(interpret2(line.strip()) for line in IN))
