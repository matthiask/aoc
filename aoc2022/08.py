import operator
from functools import reduce
from itertools import repeat
from pprint import pprint


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


def visibility(forest, x_iterable, y_iterable):
    xy = zip(x_iterable, y_iterable)
    x, y = next(xy)
    starting_height = forest[y][x]
    visibility = 0
    for x, y in xy:
        visibility += 1
        if forest[y][x] >= starting_height:
            break
    return visibility


def part2(forest):
    x_max = len(forest[0])
    y_max = len(forest)

    scores = {}

    for y in range(y_max):
        for x in range(x_max):
            score = []
            # Down
            score.append(
                visibility(
                    forest,
                    repeat(x),
                    range(y, y_max),
                )
            )
            # Up
            score.append(
                visibility(
                    forest,
                    repeat(x),
                    range(y, -1, -1),
                )
            )
            # Left
            score.append(
                visibility(
                    forest,
                    range(x, -1, -1),
                    repeat(y),
                )
            )
            # Right
            score.append(
                visibility(
                    forest,
                    range(x, x_max),
                    repeat(y),
                )
            )
            scores[(x, y)] = (reduce(operator.mul, score), score)

    pprint(scores)
    return max(scores.values())


if __name__ == "__main__":
    with open("08.txt") as f:
        forest = [list(map(int, list(line.strip()))) for line in f]

    # pprint(forest)
    # pprint((forest_x, forest_y))

    pprint(part1(forest))
    pprint(part2(forest))
