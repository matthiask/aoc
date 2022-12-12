import functools
import re
from dataclasses import dataclass
from pprint import pprint
from typing import Any, Union


@dataclass
class Leaf:
    parent: "Branch"
    value: int

    @property
    def magnitude(self):
        return self.value


@dataclass
class Branch:
    parent: Union[None, "Branch"] = None
    left: Union[Leaf, "Branch"] = None
    right: Union[Leaf, "Branch"] = None

    @property
    def magnitude(self):
        return self.left.magnitude * 3 + self.right.magnitude * 2


def dfs(node, *, depth=0):
    yield node, depth
    if isinstance(node, Branch):
        yield from dfs(node.left, depth=depth + 1)
        yield from dfs(node.right, depth=depth + 1)


def _parse_branch(tokens, parent):
    node = Branch(parent=parent)
    is_left = True
    while token := next(tokens):
        if token == "[" and is_left:
            node.left = _parse_branch(tokens, node)
        elif token == "[" and not is_left:
            node.right = _parse_branch(tokens, node)
        elif token == "]":
            break
        elif token == ",":
            is_left = False
        elif is_left:
            node.left = Leaf(node, int(token))
        else:
            node.right = Leaf(node, int(token))
    return node


def parse_number(line):
    line = re.sub(r"\s+", "", line)
    tokens = filter(None, re.split(r"([\[\]\,])", line))
    next(tokens)  # Discard first "[", outermost node is always a branch
    return _parse_branch(tokens, None)


def read():
    numbers = []
    with open("18.txt") as f:
        for line in (line.strip() for line in f):
            numbers.append(parse_number(line))
    return numbers


def find_splittable(node):
    """
    >>> find_splittable(parse_number("[9,[2,1]]")) is None
    True
    >>> find_splittable(parse_number("[9,[2,11]]")).value
    11
    """
    try:
        return next(n for n, depth in dfs(node) if isinstance(n, Leaf) and n.value > 9)
    except StopIteration:
        pass
    return None


def find_explosable(node):
    """
    >>> node = find_explosable(parse_number("[[[[[9, 8], 1], 2], 3], 4]"))
    >>> node and [node.left.value, node.right.value]
    [9, 8]
    """

    try:
        return next(n for n, depth in dfs(node) if depth == 4 and isinstance(n, Branch))
    except StopIteration:
        pass
    return None


def substitute_with(node, new):
    if node.parent.left == node:
        node.parent.left = new
    elif node.parent.right == node:
        node.parent.right = new
    else:
        raise Exception()


def explode(node):
    left = node.left.value
    right = node.right.value

    # TODO Find first Leaf on the left and add "left"
    # TODO Find first Leaf on the right and add "right"

    substitute_with(node, Leaf(node.parent, 0))


def split(node):
    """
    >>> p = Branch()
    >>> p.left = Leaf(p, 11)
    >>> p.right = Leaf(p, 8)
    >>> split(find_splittable(p))
    >>> [p.left.left.value, p.left.right.value]
    [5, 6]
    >>> p.right.value
    8
    """
    new = Branch(parent=node.parent)
    left = node.value // 2
    new.left = Leaf(new, left)
    new.right = Leaf(new, node.value - left)
    substitute_with(node, new)


def simplify(node):
    while True:
        if explosable := find_explosable(node):
            explode(node)
            continue
        if splittable := find_splittable(node):
            split(node)
            continue
        break


def magnitude(node):
    """
    >>> magnitude(parse_number("[[1,2],[[3,4],5]]"))
    143
    >>> magnitude(parse_number("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"))
    1384
    >>> magnitude(parse_number("[[[[1,1],[2,2]],[3,3]],[4,4]]"))
    445
    >>> magnitude(parse_number("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"))
    3488
    """
    return node.magnitude


# def add(n1, n2):
#     return [n1, n2]
#
#
# class Stop(Exception):
#     pass
#
#
# def split(n):
#     """
#     >>> split(10)
#     [5, 5]
#     >>> split(11)
#     [5, 6]
#     >>> split(12)
#     [6, 6]
#     """
#     left = n // 2
#     return [left, n - left]
#
#
# def reduce(n):
#     """
#     >>> reduce([[[[[9, 8], 1], 2], 3], 4])[0]
#     [[[[0, 9], 2], 3], 4]
#     >>> reduce([7, [6, [5, [4, [3, 2]]]]])[0]
#     [7, [6, [5, [7, 0]]]]
#     >>> reduce([[6, [5, [4, [3, 2]]]], 1])[0]
#     [[6, [5, [7, 0]]], 3]
#     >>> reduce([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]])[0]
#     [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]
#     >>> reduce([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]])[0]
#     [[3, [2, [8, 0]]], [9, [5, [7, 0]]]]
#     """
#
#     def _apply(p, idx, to_explode):
#         if idx > 0 and to_explode[0]:
#             if isinstance(p[idx - 1], int):
#                 p[idx - 1] += to_explode[0]
#             # FIXME That's bad.
#             elif isinstance(p[idx - 1][1], int):
#                 p[idx - 1][1] += to_explode[0]
#             elif isinstance(p[idx - 1][1][1], int):
#                 p[idx - 1][1][1] += to_explode[0]
#             elif isinstance(p[idx - 1][1][1][1], int):
#                 p[idx - 1][1][1][1] += to_explode[0]
#             elif isinstance(p[idx - 1][1][1][1][1], int):
#                 p[idx - 1][1][1][1][1] += to_explode[0]
#             to_explode[0] = 0
#
#         if idx < len(p) - 1 and to_explode[1]:
#             if isinstance(p[idx + 1], int):
#                 p[idx + 1] += to_explode[1]
#             # FIXME That's bad.
#             elif isinstance(p[idx + 1][0], int):
#                 p[idx + 1][0] += to_explode[1]
#             elif isinstance(p[idx + 1][0][0], int):
#                 p[idx + 1][0][0] += to_explode[1]
#             elif isinstance(p[idx + 1][0][0][0], int):
#                 p[idx + 1][0][0][0] += to_explode[1]
#             elif isinstance(p[idx + 1][0][0][0][0], int):
#                 p[idx + 1][0][0][0][0] += to_explode[1]
#             to_explode[1] = 0
#
#     def _helper(p, depth):
#         for idx in range(len(p)):
#             if isinstance(p[idx], list):
#                 if depth < 4:
#                     if to_explode := _helper(p[idx], depth + 1):
#                         _apply(p, idx, to_explode)
#                         return to_explode
#                 else:
#                     # Inner list has depth 4 and is to be exploded.
#                     to_explode = p[idx]
#                     p[idx] = 0
#                     _apply(p, idx, to_explode)
#                     return to_explode
#             elif p[idx] >= 10:
#                 p[idx] = split(p[idx])
#                 raise Stop()
#
#     try:
#         _changed = bool(_helper(n, 1))
#     except Stop:
#         return n, True
#     return n, _changed
#
#
# def add(n1, n2):
#     """
#     >>> add([[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1])
#     [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]
#     >>> add([[[[7, 7], [7, 7]], [[8, 7], [8, 7]]], [[[7, 0], [7, 7]], 9]], [[[[4, 2], 2], 6], [8, 7]])
#     [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]
#     """
#     n = [n1, n2]
#     while True:
#         n, changed = reduce(n)
#         if not changed:
#             return n
#
#
# def magnitude(n):
#     """
#     >>> magnitude([[1,2],[[3,4],5]])
#     143
#     >>> magnitude([[[[0,7],4],[[7,8],[6,0]]],[8,1]])
#     1384
#     >>> magnitude([[[[1,1],[2,2]],[3,3]],[4,4]])
#     445
#     >>> magnitude([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]])
#     3488
#     """
#
#     def _magnitude(v):
#         if isinstance(v, list) and len(v) == 2:
#             return _magnitude(v[0]) * 3 + _magnitude(v[1]) * 2
#         elif isinstance(v, int):
#             return v
#         else:
#             raise Exception(f"What is {v}")
#
#     return _magnitude(n)


if __name__ == "__main__":
    """
    n = functools.reduce(add, read())
    pprint(magnitude(n))
    """

    numbers = read()
    # pprint(numbers)

    pprint(numbers[-1])
    print()
    print()
    pprint(list(dfs(numbers[-1])))
