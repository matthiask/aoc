W = 25
H = 6

if __name__ == "__main__":
    import sys

    sif = open(sys.argv[1] if len(sys.argv) > 1 else "08.txt").read().strip()

    layers = [sif[i : i + W * H] for i in range(0, len(sif), W * H)]
    # print(layers)

    min_0 = sorted(layers, key=lambda layer: layer.count("0"))[0]
    print("part1", min_0.count("1") * min_0.count("2"))
