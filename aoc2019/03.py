import sys


filename = sys.argv[1] if len(sys.argv) > 1 else "03.txt"


def points(path):
    segments = path.split(",")
    points = []
    x = y = 0
    for segment in segments:
        direction = segment[0]
        steps = range(int(segment[1:]))

        for _i in steps:
            if direction == "R":
                x += 1
            elif direction == "L":
                x -= 1
            elif direction == "U":
                y += 1
            elif direction == "D":
                y -= 1
            else:
                raise Exception
            points.append((x, y))
    return points


def distance(point):
    return abs(point[0]) + abs(point[1])


def steps(points1, points2, intersections):
    for intersection in intersections:
        yield points1.index(intersection) + points2.index(intersection) + 2


path1, path2 = open(filename).read().strip().split("\n")
points1 = points(path1)
points2 = points(path2)
intersections = set(points1) & set(points2)

print("part1", min(distance(point) for point in intersections))
print("part2", min(steps(points1, points2, intersections)))
