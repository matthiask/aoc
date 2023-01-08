IN = [*open("20.txt")]
blocklist = [tuple(int(n) for n in line.strip().split("-")) for line in IN]


def part1():
    candidates = sorted(r[1] + 1 for r in blocklist)
    for candidate in candidates:
        if not any(r[0] <= candidate <= r[1] for r in blocklist):
            return candidate


print(part1())
