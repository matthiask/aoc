import sys
from pprint import pprint


def read():
    with open("13.txt") as f:
        coords, instructions = f.read().split("\n\n")

    coords = {
        tuple([int(coord) for coord in line.split(",")]) for line in coords.split("\n")
    }

    instructions = [
        (axis, int(where))
        for axis, where in (
            line.split()[2].split("=") for line in instructions.strip().split("\n")
        )
    ]

    return coords, instructions


# pprint(coords)
# pprint(instructions)


def fold(coords, instruction):
    """
    >>> fold([[1, 1], [9, 1]], ["x", 7])
    [[1, 1], [5, 1]]
    """

    axis, where = instruction

    if axis == "x":
        # where - (x - where) = 2 * where - x
        return {(x if x < where else 2 * where - x, y) for x, y in coords}
    else:
        return {(x, y if y < where else 2 * where - y) for x, y in coords}


def part1():
    coords, instructions = read()

    folded = fold(coords, instructions[0])
    return len(folded)


def part2():
    coords, instructions = read()
    for instruction in instructions:
        coords = fold(coords, instruction)

    max_x = max(coord[0] for coord in coords) + 1
    max_y = max(coord[1] for coord in coords) + 1
    pprint(coords)

    for y in range(max_y):
        for x in range(max_x):
            sys.stdout.write("#" if (x, y) in coords else " ")
        sys.stdout.write("\n")


if __name__ == "__main__":
    pprint(part1())
    part2()
