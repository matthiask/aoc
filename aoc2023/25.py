import re
from pprint import pprint

from tools import open_input


def parse_wires():
    wires = set()
    for line in open_input("25"):
        p, *other = re.split(r"[ :]+", line.strip())
        for o in other:
            wires.add(tuple(sorted((p, o))))
    return wires


def graph():
    # python3 25.py  | dot -Tsvg -ooutput.svg -Kneato
    print("graph {")
    for from_, to_ in parse_wires():
        print(f"{from_} -- {to_}")
    print("}")


exclude_test = {
    ("hfx", "pzl"),
    ("bvb", "cmg"),
    ("jqt", "nvn"),
}
exclude_prod = {
    ("zcp", "zjm"),
    ("nsk", "rsg"),
    ("jks", "rfg"),
}


def grow(components, current):
    while True:
        new = set(current)
        for c in current:
            new |= components[c]
        if new == current:
            return new
        print(current)
        current = new


def solve():
    wires = parse_wires() - exclude_prod

    components = {}
    for wire in wires:
        components.setdefault(wire[0], set()).add(wire[1])
        components.setdefault(wire[1], set()).add(wire[0])
    pprint(components)

    set1 = grow(components, {"hfx"})
    set2 = grow(components, {"pzl"})

    pprint(set1)
    pprint(set2)
    print(len(set1) * len(set2))


solve()
