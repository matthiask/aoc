from itertools import chain


IN = [*open("08.txt")]
W = 50
H = 6
pixels = [["." for _ in range(W)] for _ in range(H)]


for line in IN:
    match line.strip().split():
        case ("rect", dim):
            w, h = (int(d) for d in dim.split("x"))
            for y in range(h):
                for x in range(w):
                    pixels[y][x] = "#"

        case ("rotate", "row", row, "by", offset):
            row = int(row[2:])
            offset = int(offset) % W
            old = pixels[row][:]
            pixels[row] = old[-offset:] + old[:-offset]

        case ("rotate", "column", column, "by", offset):
            column = int(column[2:])
            offset = int(offset)
            old = [row[column] for row in pixels]
            new = old[-offset:] + old[:-offset]

            for index, c in enumerate(new):
                pixels[index][column] = c

        case _:
            1 / 0


print(list(chain.from_iterable(pixels)).count("#"))
print("\n".join("".join(row) for row in pixels))
