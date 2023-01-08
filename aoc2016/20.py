# The input uses [] intervals, we use [) for convenience
IN = [*open("20.txt")]
blocklist = [
    tuple(int(n) + i for i, n in enumerate(line.strip().split("-"))) for line in IN
]


def part1():
    candidates = sorted(r[1] for r in blocklist)
    for candidate in candidates:
        if not any(r[0] <= candidate < r[1] for r in blocklist):
            return candidate


def overlaps(range1, range2):
    s1, e1 = range1
    s2, e2 = range2
    return e1 >= s2 and e2 >= s1


def union(range1, range2):
    s1, e1 = range1
    s2, e2 = range2
    return (min(s1, s2), max(e1, e2))


def part2():
    ranges = []
    for block in blocklist:
        with_overlaps = block
        no_overlaps = []
        for r in ranges:
            if overlaps(r, with_overlaps):
                with_overlaps = union(with_overlaps, r)
            else:
                no_overlaps.append(r)
        ranges = sorted(no_overlaps + [with_overlaps])

    # print("ranges", ranges)
    return 2**32 - sum(r[1] - r[0] for r in ranges)


print(part1())
print(part2())
