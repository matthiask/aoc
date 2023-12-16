import re
from functools import cache
from pprint import pp

from tools import numbers, open_input


def generate_arrangements(p):
    if (index := p.find("?")) >= 0:
        yield from generate_arrangements(p[:index] + "#" + p[index + 1 :])
        yield from generate_arrangements(p[:index] + "." + p[index + 1 :])
    else:
        yield p


def check(p, n):
    lengths = [len(s) for s in re.findall(r"#+", p)]
    return lengths == n


def solve1():
    lines = open_input("12").read().strip().split("\n")
    patterns_numbers = [
        (pattern, numbers(num)) for pattern, num in (line.split() for line in lines)
    ]
    # pp(patterns_numbers)

    valid = 0
    for p, n in patterns_numbers:
        valid += sum(1 for arr in generate_arrangements(p) if check(arr, n))
    # pp(list(generate_arrangements("???.###")))
    pp(("part1", valid))


# solve1()


# Dynamic programming approach copied from
# https://advent-of-code.xavd.id/writeups/2023/day/12/


def solve2():
    lines = open_input("12").read().strip().split("\n")
    valid = 0
    for line in lines:
        record, groups = line.split(" ")
        groups = tuple(numbers(groups))
        record = "?".join([record] * 5)
        groups *= 5

        # print(record, groups)

        # Collapse dots into a single dot
        # record = re.sub(r"\.+", ".", record)

        new_valid = num_valid(record, groups)
        print(record, groups, new_valid)
        valid += new_valid

    pp(("part2", valid))


@cache
def num_valid(record, groups):
    if not record:  # String empty
        return not groups
    if not groups:
        return "#" not in record

    char, rest = record[0], record[1:]
    if char == ".":
        return num_valid(rest, groups)
    if char == "#":
        first, rest = rest[: groups[0] - 1], rest[groups[0] - 1 :]
        # Same idea as in linked blogpost but reversed
        # - if first is smaller than groups[0] - 1 the whole rest of the record is too short
        # - if a '.' is inside the group it's invalid (only # or ? allowed)
        # - if the first character of the rest is #, it's certainly wrong
        if len(first) < groups[0] - 1 or "." in first or (rest and rest[0] == "#"):
            return 0
        return num_valid(rest[1:], groups[1:])
    if char == "?":
        return num_valid(f"#{rest}", groups) + num_valid(f".{rest}", groups)
    raise Exception


solve2()
