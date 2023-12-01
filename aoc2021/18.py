import copy
import re
from itertools import product
from pprint import pprint


class Leaf:
    def __init__(self, parent, value):
        self.parent = parent
        self.value = value

    def magnitude(self):
        return self.value

    def unparse(self):
        return self.value


class Branch:
    def __init__(self, parent, left=None, right=None):
        self.parent = parent
        self.left = left
        self.right = right

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
        elif is_left and token == ",":
            is_left = False
        elif is_left and node.left is None:
            node.left = Leaf(node, int(token))
        elif not is_left and node.right is None:
            node.right = Leaf(node, int(token))
        else:
            raise Exception()
    return node


def parse(line):
    line = re.sub(r"\s+", "", line)
    tokens = filter(None, re.split(r"([\[\]\,])", line))
    next(tokens)  # Discard first "[", outermost node is always a branch
    return _parse_branch(tokens, None)


def unparse(node):
    return node.unparse()


def read(file="18.txt"):
    numbers = []
    with open(file) as f:
        for line in (line.strip() for line in f):
            numbers.append(parse(line))
    return numbers


def find_splittable(node):
    """
    >>> find_splittable(parse("[9,[2,1]]")) is None
    True
    >>> find_splittable(parse("[9,[2,11]]")).value
    11
    """
    try:
        return next(n for n, depth in dfs(node) if isinstance(n, Leaf) and n.value > 9)
    except StopIteration:
        pass
    return None


def find_explodable(node):
    """
    >>> a,b,c = find_explodable(parse("[[[[[9, 8], 1], 2], 3], 4]")); (a,unparse(b),c.value)
    (None, [9, 8], 1)
    >>> find_explodable(parse("[[[[9,8],1],2],3]")) is None
    True
    >>> a,b,c = find_explodable(parse("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")); (a.value,unparse(b),c.value)
    (1, [7, 3], 6)
    """

    previous_leaf = None
    explodable = None
    next_leaf = None

    dfs_iter = dfs(node)

    for n, depth in dfs_iter:
        if (
            depth == 4 and isinstance(n, Branch)
            # The following is always true:
            # and isinstance(n.left, Leaf)
            # and isinstance(n.right, Leaf)
        ):
            explodable = n
            break

        elif explodable is None and isinstance(n, Leaf):
            previous_leaf = n

    if explodable:
        for n, _depth in dfs_iter:
            if n.parent is not explodable and isinstance(n, Leaf):
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
    >>> p = parse("[[[[[9,8],1],2],3],4]")
    >>> explode(*find_explodable(p))
    >>> unparse(p)
    [[[[0, 9], 2], 3], 4]
    >>> p = parse("[[[[1,[7,7]],2],3],4]")
    >>> explode(*find_explodable(p))
    >>> unparse(p)
    [[[[8, 0], 9], 3], 4]
    >>> p = parse("[[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]")
    >>> explode(*find_explodable(p))
    >>> unparse(p)
    [[3, [2, [8, 0]]], [9, [5, [7, 0]]]]
    >>> p = parse("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")
    >>> explode(*find_explodable(p))
    >>> unparse(p)
    [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]
    >>> p = parse("[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]")
    >>> a,b,c = find_explodable(p); (a.value,unparse(b),c.value)
    (0, [6, 7], 1)
    >>> explode(*find_explodable(p))
    >>> unparse(p)
    [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]
    """
    if previous_leaf:
        previous_leaf.value += node.left.value
    if next_leaf:
        next_leaf.value += node.right.value
    substitute_with(node, Leaf(parent=node.parent, value=0))


def split(node):
    """
    >>> p = parse("[11,8]")
    >>> split(find_splittable(p))
    >>> unparse(p)
    [[5, 6], 8]
    >>> p = parse("[[[[0,7],4],[[7,8],[0,13]]],[1,1]]")
    >>> split(find_splittable(p))
    >>> unparse(p)
    [[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]]
    """
    new = Branch(parent=node.parent)
    left = node.value // 2
    new.left = Leaf(new, left)
    new.right = Leaf(new, node.value - left)
    substitute_with(node, new)


def simplify(node):
    """
    >>> unparse(simplify(parse("[[7, [[8, 4], 9]], 1]")))
    [[7, [[8, 4], 9]], 1]
    """
    while True:
        # print(unparse(node))

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
    >>> magnitude(parse("[[1,2],[[3,4],5]]"))
    143
    >>> magnitude(parse("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"))
    1384
    >>> magnitude(parse("[[[[1,1],[2,2]],[3,3]],[4,4]]"))
    445
    >>> magnitude(parse("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"))
    3488
    """
    return node.magnitude()


def add(n1, n2):
    """
    >>> unparse(add(parse("[[[[4,3],4],4],[7,[[8,4],9]]]"), parse("[1,1]")))
    [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]
    >>> unparse(add(parse("[[[[7, 7], [7, 7]], [[8, 7], [8, 7]]], [[[7, 0], [7, 7]], 9]]"), parse("[[[[4, 2], 2], 6], [8, 7]]")))
    [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]
    >>> unparse(add(parse("[[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]"), parse("[[[5,[7,4]],7],1]")))
    [[[[7, 7], [7, 7]], [[8, 7], [8, 7]]], [[[7, 0], [7, 7]], 9]]
    >>> unparse(add(parse("[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]"), parse("[[[[4,2],2],6],[8,7]]")))
    [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]
    """

    assert n1.parent is None
    assert n2.parent is None

    n = Branch(parent=None)
    n1.parent = n2.parent = n
    n.left = n1
    n.right = n2
    # print(unparse(n))
    simplify(n)
    # print(unparse(n))
    return n


def largest():
    numbers = read("18.txt")
    magnitudes = set()
    for n1, n2 in product(numbers, numbers):
        magnitudes.add(magnitude(add(copy.deepcopy(n1), copy.deepcopy(n2))))
        magnitudes.add(magnitude(add(copy.deepcopy(n2), copy.deepcopy(n1))))
    return max(magnitudes)


if __name__ == "__main__":
    n, *numbers = read("18.txt")
    for n2 in numbers:
        n = add(n, n2)

        pprint(unparse(n))
        pprint(magnitude(n))

    pprint(largest())

    # n = functools.reduce(add, numbers)
    # print(unparse(n))
    # pprint(magnitude(n))

    # pprint(numbers)
    # pprint(numbers[-1])
    # print()
    # print()
    # pprint(list(dfs(numbers[-1])))

    # numbers = read("18-test.txt")
    # print(unparse(functools.reduce(add, numbers)))

    # print(parse("[[7,[[8,4],9]],1]"))
    # print(unparse(simplify(parse("[[7,[[8,4],9]],1]"))))
