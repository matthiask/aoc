from pprint import pp

from tools import open_input, range_inclusive


patterns = [
    pattern.split("\n") for pattern in open_input("13").read().strip().split("\n\n")
]

pp(patterns)


# part1
target_difference = 0
# part2
target_difference = 1


def vertical(pattern, x):
    return [line[x] for line in pattern]


def differences(p1, p2):
    return sum(0 if a == b else 1 for a, b in zip(p1, p2))


summary = 0
for pattern in patterns:
    for y in range_inclusive(0, len(pattern) - 2):
        difference_sum = 0
        for dy in range_inclusive(0, min(y, len(pattern) - y - 2)):
            difference_sum += differences(pattern[y - dy], pattern[y + 1 + dy])
        if difference_sum == target_difference:
            summary += 100 * (y + 1)
            pp(y)

    for x in range_inclusive(0, len(pattern[0]) - 2):
        difference_sum = 0
        for dx in range_inclusive(0, min(x, len(pattern[0]) - x - 2)):
            difference_sum += differences(
                vertical(pattern, x - dx), vertical(pattern, x + 1 + dx)
            )
        if difference_sum == target_difference:
            summary += x + 1
            pp(x)


pp(("summary", summary))
