import re
import sys
from dataclasses import dataclass
from itertools import product
from pprint import pprint


@dataclass
class Node:
    x: int
    y: int
    size: int
    used: int
    avail: int
    used_percentage: int


IN = [
    Node(*[int(n) for n in re.findall(r"\d+", line)])
    for line in list(open("22.txt" if len(sys.argv) < 2 else sys.argv[1]))[2:]
]
grid = {(node.x, node.y): node for node in IN}


def part1():
    def is_viable(node1, node2):
        if node1 == node2:
            return False
        return node1.used and node1.used < node2.avail

    return sum(1 for pair in product(IN, IN) if is_viable(*pair))


def neighbors(node):
    coords = [
        (node.x + 1, node.y),
        (node.x - 1, node.y),
        (node.x, node.y + 1),
        (node.x, node.y - 1),
    ]
    return [node for node in map(grid.get, coords) if node]


def part2():
    data = (0, 32)
    access = (0, 0)
    empty_node = 0  # ??


pprint(grid)
pprint(("part1", part1()))
