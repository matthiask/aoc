IN = [*open("02.txt")]
IN = [list(map(int, line.strip().split("x"))) for line in IN]


def wrapping(box):
    sides = (
        box[0] * box[1],
        box[1] * box[2],
        box[0] * box[2],
    )
    return 2 * sum(sides) + min(sides)


def ribbon(box):
    half_perimeters = (
        box[0] + box[1],
        box[1] + box[2],
        box[0] + box[2],
    )
    volume = box[0] * box[1] * box[2]
    return 2 * min(half_perimeters) + volume


print(sum(map(wrapping, IN)))
print(sum(map(ribbon, IN)))
