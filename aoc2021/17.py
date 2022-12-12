import re
from itertools import count
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


def trajectory(x_velocity, y_velocity, bounds):
    """
    >>> list(trajectory(10, 0, {"xmin": 0, "xmax": 20, "ymin": -1e9}))
    [(10, 0), (19, -1)]
    >>> list(trajectory(10, 0, {"xmin": 0, "xmax": 1e9, "ymin": -10}))
    [(10, 0), (19, -1), (27, -3), (34, -6), (40, -10)]
    """
    x = 0
    y = 0
    while True:
        x += x_velocity
        y += y_velocity

        if x > bounds["xmax"]:
            # Too far to the right
            break
        elif y < bounds["ymin"]:
            # Too far down
            break
        elif x < bounds["xmin"] and x_velocity == 0:
            # Unreachable, no x velocity anymore
            break

        yield (x, y)

        # Drag
        x_velocity = max(0, x_velocity - 1)
        # Gravity
        y_velocity -= 1


def find_min_x_velocity(xmin):
    """
    >>> find_min_x_velocity(10)
    4
    >>> find_min_x_velocity(5050)
    100
    """

    for i in count(1):
        # Gauss.
        if i * (i + 1) // 2 >= xmin:
            return i


def find_x_velocities(bounds):
    min_xv = find_min_x_velocity(bounds["xmin"])

    x_velocities = set()

    for x_velocity in range(min_xv, bounds["xmax"] + 1):
        # print(f"Testing {x_velocity}...")
        for point in trajectory(x_velocity, 0, bounds | {"ymin": -1000}):
            if bounds["xmin"] <= point[0] <= bounds["xmax"]:
                x_velocities.add(x_velocity)

    return sorted(x_velocities)


def new_part1():
    bounds = read()
    print("part1")
    # Not needed, but still. Lowest possible x velocity is as good as any.
    print("x velocity", find_min_x_velocity(bounds["xmin"]))

    # Since the dy values are the same when going up as when coming down
    # again we only have to look at the last segment (from zero to ymin),
    # subtract one from the difference and apply the Gauss formula to
    # sum up all y segments.
    y_velocity = -bounds["ymin"] - 1
    print("y velocity", y_velocity)
    print("highest y point:", y_velocity * (y_velocity + 1) // 2)


def new_part2():
    bounds = read()
    found = 0
    for x_velocity in find_x_velocities(bounds):
        for y_velocity in range(bounds["ymin"], abs(bounds["ymin"])):
            # print(f"Checking {x_velocity},{y_velocity}")
            for x, y in trajectory(x_velocity, y_velocity, bounds):
                if (
                    bounds["xmin"] <= x <= bounds["xmax"]
                    and bounds["ymin"] <= y <= bounds["ymax"]
                ):
                    found += 1
                    break

    print("part2")
    print(found)


if __name__ == "__main__":
    # pprint(read())
    # part1()

    new_part1()
    new_part2()
