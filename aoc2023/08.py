import math
import re
from itertools import cycle
from pprint import pp

from tools import open_input


def parse():
    instructions, lines = open_input("08").read().strip().split("\n\n")
    nodes = {}
    for line in lines.split("\n"):
        parts = re.findall(r"[A-Z0-9]+", line)
        nodes[parts[0]] = parts[1:]
    instructions = [{"L": 0, "R": 1}[c] for c in instructions]
    return instructions, nodes


def solve1():
    instructions, nodes = parse()
    # pp(parse())

    location = "AAA"
    steps = 0
    for instruction in cycle(instructions):
        location = nodes[location][instruction]
        steps += 1
        if location == "ZZZ":
            pp(("part1", steps))
            break


def steps(instructions, nodes, location):
    count = 0
    first = None
    for instruction in cycle(instructions):
        location = nodes[location][instruction]
        count += 1
        if location.endswith("Z"):
            if first:
                return first, count - first
            else:
                first = count


def solve2():
    instructions, nodes = parse()
    # pp(parse())

    locations = [node for node in nodes if node.endswith("A")]
    lengths = {location: steps(instructions, nodes, location) for location in locations}

    pp(locations)
    pp(lengths)

    pp(("part2", math.lcm(*(length[1] for length in lengths.values()))))


solve2()
