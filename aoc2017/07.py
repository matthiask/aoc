import operator
import re
from collections import Counter
from functools import cache, reduce

from utils import open_input


IN = [*open_input("07")]

nodes = {}
parent = {}
for line in IN:
    tokens = re.sub(r"[->(),]+", "", line).split()
    nodes[tokens[0]] = (w, children) = [int(tokens[1]), set(tokens[2:])]
    for child in children:
        parent[child] = tokens[0]
(root,) = tuple(set(nodes) - reduce(operator.or_, (pair[1] for pair in nodes.values())))


@cache
def weight(node):
    w, children = nodes[node]
    return w + sum(weight(child) for child in children)


def unbalanced_node_weight(node):
    w, children = nodes[node]
    if not children:
        # Leaf nodes cannot be unbalanced
        return
    if len({weight(child) for child in children}) != 1:
        # Children are unbalanced
        return
    siblings = Counter(weight(child) for child in nodes[parent[node]][1]).most_common()
    if len(siblings) != 2:
        return
    if weight(node) == siblings[0][0]:
        return
    return siblings[0][0] - sum(weight(child) for child in children)


# print(nodes)
print("part1", root)
print("part2", next(filter(None, (unbalanced_node_weight(node) for node in nodes))))
