from hashlib import md5


start = (0, 0)
end = (3, 3)
passcode = b"dmypynyp"
door_open = "bcdef"


def visitable(point, path):
    d = md5(passcode + path).hexdigest()
    up, down, left, right = (c in door_open for c in d[:4])

    x, y = point
    if y > 0 and up:
        yield ((x, y - 1), path + b"U")
    if y < 3 and down:
        yield ((x, y + 1), path + b"D")
    if x > 0 and left:
        yield ((x - 1, y), path + b"L")
    if x < 3 and right:
        yield ((x + 1, y), path + b"R")


def part1():
    todo = [(start, b"")]

    while True:
        next_todo = []
        for point, path in todo:
            if point == end:
                return path
            next_todo.extend(visitable(point, path))
        todo = next_todo

        if not todo:
            return "No solution"


def part2():
    paths = set()
    todo = [(start, b"")]

    while True:
        next_todo = []
        for point, path in todo:
            if point == end:
                paths.add(path)
            else:
                next_todo.extend(visitable(point, path))
        todo = next_todo

        if not todo:
            break

    return max(map(len, paths))


print(part1())
print(part2())
