forwards = {
    "#": 1,
    ".": 0,
}
backwards = {
    1: "#",
    0: ".",
}


def read():
    with open("20.txt") as f:
        algorithm, image = f.read().split("\n\n")

    algorithm = [forwards[c] for c in algorithm]
    image = {
        (x, y): forwards[c]
        for y, line in enumerate(image.splitlines())
        for x, c in enumerate(line.strip())
    }

    return algorithm, image


def _enhance_id(image, point, default):
    x, y = point
    bits = [
        image.get((x - 1, y - 1), default),
        image.get((x + 0, y - 1), default),
        image.get((x + 1, y - 1), default),
        image.get((x - 1, y + 0), default),
        image.get((x + 0, y + 0), default),
        image.get((x + 1, y + 0), default),
        image.get((x - 1, y + 1), default),
        image.get((x + 0, y + 1), default),
        image.get((x + 1, y + 1), default),
    ]
    return int("".join(str(bit) for bit in bits), 2)


def bounds(image):
    min_x = min(x for x, y in image.keys())
    max_x = max(x for x, y in image.keys())
    min_y = min(y for x, y in image.keys())
    max_y = max(y for x, y in image.keys())
    return (min_x, max_x, min_y, max_y)


def enhance(image, algorithm, default):
    (min_x, max_x, min_y, max_y) = bounds(image)

    points = (
        (x, y) for y in range(min_y - 2, max_y + 3) for x in range(min_x - 2, max_x + 3)
    )

    return {point: algorithm[_enhance_id(image, point, default)] for point in points}


def printify(image):
    (min_x, max_x, min_y, max_y) = bounds(image)
    return "\n".join(
        "".join(backwards[image[(x, y)]] for x in range(min_x, max_x + 1))
        for y in range(min_y, max_y + 1)
    )


def enhance_loop(image, algorithm, count):
    for i in range(count):
        image = enhance(image, algorithm, default=i % 2)
    return image


if __name__ == "__main__":
    algorithm, image = read()
    # print(image)
    # print(printify(image))

    twice = enhance_loop(image, algorithm, 2)
    print(printify(twice))
    print(sum(1 for bit in twice.values() if bit))

    fifty = enhance_loop(image, algorithm, 50)
    print(printify(fifty))
    print(sum(1 for bit in fifty.values() if bit))
