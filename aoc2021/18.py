import functools
import re
from dataclasses import dataclass
from pprint import pprint
from typing import Any, Union


@dataclass
class Leaf:
    parent: "Branch"
    value: int

    def magnitude(self):
        return self.value

    def unparse(self):
        return self.value


@dataclass
class Branch:
    parent: Union[None, "Branch"] = None
    left: Union[Leaf, "Branch"] = None
    right: Union[Leaf, "Branch"] = None

    def magnitude(self):
        return self.left.magnitude() * 3 + self.right.magnitude() * 2

    def unparse(self):
        return [self.left.unparse(), self.right.unparse()]


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


def unparse(node):
    return node.unparse()


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


def find_explodable(node):
    """
    >>> a,b,c = find_explodable(parse_number("[[[[[9, 8], 1], 2], 3], 4]")); (a,unparse(b),c.value)
    (None, [9, 8], 1)
    >>> find_explodable(parse_number("[[[[9,8],1],2],3]")) is None
    True
    """

    previous_leaf = None
    explodable = None
    next_leaf = None

    for n, depth in dfs(node):
        if (
            depth == 4
            and isinstance(n, Branch)
            # and isinstance(n.left, Leaf)
            # and isinstance(n.right, Leaf)
        ):
            explodable = n

        elif explodable is None and isinstance(n, Leaf):
            previous_leaf = n

        elif explodable is not None and n.parent is not explodable and isinstance(n, Leaf):
            next_leaf = n
            break

    if explodable:
        return previous_leaf, explodable, next_leaf


def substitute_with(node, new):
    if node.parent.left is node:
        node.parent.left = new
    elif node.parent.right is node:
        node.parent.right = new
    else:
        raise Exception()


def explode(previous_leaf, node, next_leaf):
    """
    >>> p = parse_number("[[[[[9,8],1],2],3],4]")
    >>> explode(*find_explodable(p))
    >>> unparse(p)
    [[[[0, 9], 2], 3], 4]
    >>> p = parse_number("[[[[1,[7,7]],2],3],4]")
    >>> explode(*find_explodable(p))
    >>> unparse(p)
    [[[[8, 0], 9], 3], 4]
    >>> p = parse_number("[[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]")
    >>> explode(*find_explodable(p))
    >>> unparse(p)
    [[3, [2, [8, 0]]], [9, [5, [7, 0]]]]
    """
    if previous_leaf:
        previous_leaf.value += node.left.value
    if next_leaf:
        next_leaf.value += node.right.value
    substitute_with(node, Leaf(parent=node.parent, value=0))


def split(node):
    """
    >>> p = parse_number("[11,8]")
    >>> split(find_splittable(p))
    >>> unparse(p)
    [[5, 6], 8]
    """
    new = Branch(parent=node.parent)
    left = node.value // 2
    new.left = Leaf(new, left)
    new.right = Leaf(new, node.value - left)
    substitute_with(node, new)


def simplify(node):
    """
    >>> unparse(simplify(parse_number("[[7, [[8, 4], 9], 1], 1]")))
    [[7, 1], 1]
    """
    while True:
        if explodable := find_explodable(node):
            explode(*explodable)
            continue
        if splittable := find_splittable(node):
            split(splittable)
            continue
        break
    return node


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
    return node.magnitude()


def add(n1, n2):
    """
    >>> unparse(add(parse_number("[[[[4, 3], 4], 4], [7, [[8, 4], 9]]]"), parse_number("[1, 1]")))
    [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]
    >>> unparse(add(parse_number("[[[[7, 7], [7, 7]], [[8, 7], [8, 7]]], [[[7, 0], [7, 7]], 9]]"), parse_number("[[[[4, 2], 2], 6], [8, 7]]")))
    [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]
    >>> unparse(add(parse_number("[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]"), parse_number("[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]")))
    [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]
    """

    n = Branch(parent=None)
    n1.parent = n2.parent = n
    n.left = n1
    n.right = n2
    simplify(n)
    return n


if __name__ == "__main__":
    numbers = read()

    n = functools.reduce(add, numbers)
    print(unparse(n))
    pprint(magnitude(n))

    # pprint(numbers)
    # pprint(numbers[-1])
    # print()
    # print()
    # pprint(list(dfs(numbers[-1])))
