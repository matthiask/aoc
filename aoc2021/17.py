import re
from itertools import islice
from pprint import pprint


def read():
    with open("17.txt") as f:
        numbers = [int(number) for number in re.findall(r"([-0-9]+)", f.read())]
        return {
            "xmin": numbers[0],
            "xmax": numbers[1],
            "ymin": numbers[2],
            "ymax": numbers[3],
        }


def trajectory(x_velocity, y_velocity):
    """
    >>> list(islice(trajectory(4, 3), 3))
    [(4, 3), (7, 5), (9, 6)]
    >>> list(islice(trajectory(2, 0), 4))
    [(2, 0), (3, -1), (3, -3), (3, -6)]
    """
    x = 0
    y = 0
    while True:
        x += x_velocity
        y += y_velocity

        yield (x, y)

        # Drag
        x_velocity = max(0, x_velocity - 1)
        # Gravity
        y_velocity -= 1


def cut_off_at(points, bounds):
    """
    >>> list(cut_off_at(trajectory(10, 0), {"xmax": 20, "ymin": -1e9}))
    [(10, 0), (19, -1)]
    >>> list(cut_off_at(trajectory(10, 0), {"xmax": 1e9, "ymin": -10}))
    [(10, 0), (19, -1), (27, -3), (34, -6), (40, -10)]
    """
    for point in points:
        if point[0] > bounds["xmax"] or point[1] < bounds["ymin"]:
            break
        yield point


if __name__ == "__main__":
    pprint(read())
