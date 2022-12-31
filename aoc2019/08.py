import sys


W = 25
H = 6

sif = open(sys.argv[1] if len(sys.argv) > 1 else "08.txt").read().strip()

layers = [sif[i : i + W * H] for i in range(0, len(sif), W * H)]
# print(layers)

min_0 = sorted(layers, key=lambda layer: layer.count("0"))[0]
print("part1", min_0.count("1") * min_0.count("2"))


def bw(pixels):
    return next(p for p in pixels if p != "2")


def print_image(pixels):
    for y in range(H):
        sys.stdout.write("\n")
        for x in range(W):
            sys.stdout.write("#" if pixels[x + y * W] == "1" else " ")
    print()


pixels = [bw(p) for p in zip(*layers)]
print_image(pixels)
