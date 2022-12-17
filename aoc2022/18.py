with open("18.txt") as f:
    puzzle_input = f.read()
test_input = """\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""


def parse(inp):
    return {tuple(int(c) for c in line.strip().split(",")) for line in inp.splitlines()}


_adjacent = [
    (0, 0, +1),
    (0, 0, -1),
    (0, +1, 0),
    (0, -1, 0),
    (+1, 0, 0),
    (-1, 0, 0),
]


def adjacent_coordinates(point):
    return [tuple(a + b for a, b in zip(point, offset)) for offset in _adjacent]


def surface_area(cubes):
    surface = 6 * len(cubes)
    for cube in cubes:
        adjacent = sum(1 for point in adjacent_coordinates(cube) if point in cubes)
        surface -= adjacent
    return surface


if __name__ == "__main__":
    from pprint import pprint

    pprint(parse(test_input))
    pprint(adjacent_coordinates((2, 2, 2)))

    print("part1 test", surface_area(parse(test_input)))
    print("part1", surface_area(parse(puzzle_input)))
