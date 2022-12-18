from itertools import chain, product


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
    return {tuple(a + b for a, b in zip(point, offset)) for offset in _adjacent}


def surface_area(cubes):
    surface = 6 * len(cubes)
    for cube in cubes:
        adjacent = sum(1 for point in adjacent_coordinates(cube) if point in cubes)
        surface -= adjacent
    return surface


def _expand(cubes, edge_cubes, bubble):
    # print("Checking", bubble)
    seen = set()
    while True:
        expanded = False
        unchecked_adjacent = (
            set(chain.from_iterable(adjacent_coordinates(cube) for cube in bubble))
            - seen
        )

        for potential_cube in unchecked_adjacent:
            if potential_cube in cubes:
                # print("Adjacent cube is solid", potential_cube)
                continue
            if potential_cube in edge_cubes:
                # print("Encountered edge cube", potential_cube)
                return None

            expanded = True
            bubble.add(potential_cube)

        seen |= unchecked_adjacent

        if not expanded:
            # print("No additional expansion, returning", bubble)
            return bubble
        # print("Expanding", bubble)


def find_bubbles(cubes):
    xmin = min(point[0] for point in cubes)
    ymin = min(point[1] for point in cubes)
    zmin = min(point[2] for point in cubes)
    xmax = max(point[0] for point in cubes)
    ymax = max(point[1] for point in cubes)
    zmax = max(point[2] for point in cubes)

    all_cubes = set(
        product(
            range(xmin, xmax + 1),
            range(ymin, ymax + 1),
            range(zmin, zmax + 1),
        )
    )
    all_inner_cubes = set(
        product(
            range(xmin + 1, xmax),
            range(ymin + 1, ymax),
            range(zmin + 1, zmax),
        )
    )
    edge_cubes = all_cubes - all_inner_cubes

    # print("edge_cubes", sorted(edge_cubes))
    print("Set sizes", len(all_cubes), len(all_inner_cubes), len(edge_cubes))

    bubbles = set()
    for possible_bubble_start in sorted(all_inner_cubes - cubes):
        # print("Started at", possible_bubble_start, "found", _expand(cubes, edge_cubes, {possible_bubble_start}))

        if bubble := _expand(cubes, edge_cubes, {possible_bubble_start}):
            bubbles.add(tuple(sorted(bubble)))
    return bubbles


if __name__ == "__main__":
    from pprint import pprint

    pprint(parse(test_input))
    pprint(adjacent_coordinates((2, 2, 2)))

    print("part1 test", surface_area(parse(test_input)))
    cubes = parse(puzzle_input)
    print("part1", surface_area(cubes))

    print("\npart2 test")
    cubes = parse(test_input)
    bubbles = find_bubbles(cubes)
    print([(len(bubble), surface_area(bubble)) for bubble in bubbles])
    print(surface_area(cubes) - sum(surface_area(bubble) for bubble in bubbles))

    print("\npart2")
    cubes = parse(puzzle_input)
    bubbles = find_bubbles(cubes)
    print([(len(bubble), surface_area(bubble)) for bubble in bubbles])
    print(surface_area(cubes) - sum(surface_area(bubble) for bubble in bubbles))
