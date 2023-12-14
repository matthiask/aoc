import re
from pprint import pp

from tools import numbers, open_input


lines = open_input("12").read().strip().split("\n")
patterns_numbers = [
    (list(pattern), numbers(num)) for pattern, num in (line.split() for line in lines)
]


# pp(patterns_numbers)


def generate_arrangements(p):
    if "?" in p:
        index = p.index("?")
        yield from generate_arrangements([*p[:index], "#", *p[index + 1 :]])
        yield from generate_arrangements([*p[:index], ".", *p[index + 1 :]])
    else:
        yield p


def check(p, n):
    lengths = [len(s) for s in re.split(r"\.+", p) if len(s)]
    # print(p, lengths, n)
    return lengths == n


# pp(["".join(p) for p in generate_arrangements(list("???.###"))])


valid = 0
for p, n in patterns_numbers:
    # print(list("".join(a) for a in generate_arrangements(p)))
    # print(n)
    valid += sum(
        1 for arrangement in generate_arrangements(p) if check("".join(arrangement), n)
    )
pp(("part1", valid))
