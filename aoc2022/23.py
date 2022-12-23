"""
       N
      +j
 W -1  0 +1 E
      -j
       S
"""
from collections import defaultdict, deque
from itertools import chain


directions = ["N", "S", "W", "E"]
# First direction is orthogonal, others are diagonal
consider = {
    "N": [1j, -1 + 1j, 1 + 1j],
    "W": [-1, -1 + 1j, -1 - 1j],
    "S": [-1j, -1 - 1j, 1 - 1j],
    "E": [1, 1 + 1j, 1 - 1j],
}
all_directions = set(chain.from_iterable(consider.values()))


def elf(x, y):
    return [complex(x, y), deque(directions)]


def propose(elves, loc, directions):
    try:
        # Do not propose to move at all if no other elves nearby
        if all(loc + offset not in elves for offset in all_directions):
            return None
        for direction in directions:
            if all(loc + offset not in elves for offset in consider[direction]):
                return loc + consider[direction][0]
    finally:
        # Always rotate first direction considered.
        directions.rotate(-1)
    return None


def parse(inp):
    return {
        complex(x, y): deque(directions)
        for y, line in enumerate(reversed(inp.splitlines()))
        for x, c in enumerate(line.strip())
        if c == "#"
    }


def round(elves):
    elves_and_proposals = [
        (propose(elves, loc, directions), loc, directions)
        for loc, directions in elves.items()
    ]
    proposed = defaultdict(int)
    for row in elves_and_proposals:
        proposed[row[0]] += 1
    allowed = {loc for loc, count in proposed.items() if count == 1}

    elves = {}
    for proposal, loc, directions in elves_and_proposals:
        if proposal in allowed:
            elves[proposal] = directions
        else:
            elves[loc] = directions
    return elves


def bounding_box(elves):
    locs = list(elves)
    x = [loc.real for loc in locs]
    y = [loc.imag for loc in locs]
    return [int(v) for v in [min(x), max(x), min(y), max(y)]]


def bounding_box_area(elves):
    xmin, xmax, ymin, ymax = bounding_box(elves)
    return (xmax - xmin + 1) * (ymax - ymin + 1)


def pretty(elves):
    xmin, xmax, ymin, ymax = bounding_box(elves)
    print(
        "\n".join(
            "".join(
                "#" if complex(x, y) in elves else "."
                for x in range(xmin - 1, xmax + 2)
            )
            for y in range(ymax + 1, ymin - 2, -1)
        )
    )
    print()


if __name__ == "__main__":
    import sys

    inp = open(sys.argv[1] if len(sys.argv) > 1 else "23.txt").read()

    elves = parse(inp)
    # pprint(elves)
    # pprint(round(elves))

    for i in range(10):
        elves = round(elves)
        print(f"End of Round {i + 1}")
        pretty(elves)
    print("part1", bounding_box_area(elves) - len(elves))

    elves = parse(inp)
    rounds = 0
    locs = set(elves)
    while True:
        elves = round(elves)
        new_locs = set(elves)
        rounds += 1
        if locs == new_locs:
            print("part2", rounds)
            break
        locs = new_locs

    """
    locs = set(elves)
    while True:
        print("moving...")
        print("bounding box:", bounding_box(elves))
        print("empty:", bounding_box(elves) - len(elves))
        elves = round(elves)
        new_locs = set(elves)
        if locs == new_locs:
            break
        locs = new_locs
    """
