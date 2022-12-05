import re
from collections import deque, namedtuple
from itertools import zip_longest
from pprint import pprint


Op = namedtuple("Op", "count from_ to_")


"""
Implementation notice:

Because it's easier the uppermost crate of each stack has index 0. 
"""

UPPERMOST = 0


def parse_stacks(lines):
    layers = []
    while (line := lines.popleft()) and line.startswith("["):
        layers.append(list(line[1::4]))
    stacks = list(zip_longest(*layers, fillvalue=" "))
    return [list(filter(lambda val: val != " ", stack)) for stack in stacks]


def parse_ops(lines):
    for line in lines:
        if match := re.match(r"move (\d+) from (\d+) to (\d+)", line):
            yield Op(*[int(value) for value in match.groups()])


def parse():
    with open("input.txt") as f:
        lines = deque(line.strip() for line in f)

    return parse_stacks(lines), list(parse_ops(lines))


def move_one(stacks, from_, to_):
    stacks[to_ - 1].insert(UPPERMOST, stacks[from_ - 1].pop(UPPERMOST))


def part1():
    stacks, ops = parse()
    for op in ops:
        for _i in range(op.count):
            move_one(stacks, op.from_, op.to_)
    print("".join(stack[UPPERMOST] for stack in stacks))


def part2():
    stacks, ops = parse()
    for op in ops:
        from_ = stacks[op.from_ - 1]
        moving, stacks[op.from_ - 1] = from_[:op.count], from_[op.count:]
        stacks[op.to_ - 1][0:0] = moving
    print("".join(stack[UPPERMOST] for stack in stacks))


if __name__ == "__main__":
    # pprint(parse())
    part1()
    part2()
