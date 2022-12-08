from itertools import repeat


def visible_trees(forest, x_iterable, y_iterable):
    height = -1
    visible = set()
    for x, y in zip(x_iterable, y_iterable):
        if forest[y][x] > height:
            height = forest[y][x]
            visible.add((x, y))
        # print({"x": x, "y": y, "height": height, "visible": visible, "cur": forest[y][x]})
    return visible


def part1(forest):
    forest_x = len(forest[0])
    forest_y = len(forest)

    forest_x_range = list(range(0, len(forest[0])))
    forest_y_range = list(range(0, len(forest)))

    # Edges are all visible
    visible = set()

    for x in forest_x_range:
        visible |= visible_trees(
            forest, 
            repeat(x),
            forest_y_range,
        )
        visible |= visible_trees(
            forest, 
            repeat(x),
            forest_y_range[::-1],
        )
    for y in forest_y_range:
        visible |= visible_trees(
            forest, 
            forest_x_range,
            repeat(y),
        )
        visible |= visible_trees(
            forest, 
            forest_x_range[::-1],
            repeat(y),
        )
    return len(visible)


if __name__ == "__main__":
    from pprint import pprint

    with open("input.txt") as f:
        forest = [list(map(int, list(line.strip()))) for line in f]

    # pprint(forest)
    # pprint((forest_x, forest_y))

    pprint(part1(forest))
