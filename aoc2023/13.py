from pprint import pp

from tools import open_input, range_inclusive


patterns = [
    pattern.split("\n") for pattern in open_input("13").read().strip().split("\n\n")
]

pp(patterns)


def vertical(pattern, x):
    return [line[x] for line in pattern]


summary = 0
for pattern in patterns:
    for y in range_inclusive(0, len(pattern) - 2):
        match = True
        for dy in range_inclusive(0, min(y, len(pattern) - y - 2)):
            if pattern[y - dy] != pattern[y + 1 + dy]:
                match = False
        if match:
            summary += 100 * (y + 1)
            pp(y)

    for x in range_inclusive(0, len(pattern[0]) - 2):
        match = True
        for dx in range_inclusive(0, min(x, len(pattern[0]) - x - 2)):
            if vertical(pattern, x - dx) != vertical(pattern, x + 1 + dx):
                match = False
        if match:
            summary += x + 1
            pp(x)

pp(("part1", summary))
