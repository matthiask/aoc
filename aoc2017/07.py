import operator
import re
from functools import reduce

from utils import open_input


IN = [*open_input("07")]

nodes = {}
for line in IN:
    tokens = re.sub(r"[->(),]+", "", line).split()
    nodes[tokens[0]] = [int(tokens[1]), set(tokens[2:])]
(root,) = tuple(set(nodes) - reduce(operator.or_, (pair[1] for pair in nodes.values())))


def weight(node):
    w, children = nodes[node]
    return w + sum(weight(child) for child in children)


# print(nodes)
print("part1", root)
print("part2", [(child, weight(child)) for child in nodes[root][1]])
