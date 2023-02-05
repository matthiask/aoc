def read():
    groups = open("01.txt").read().strip().split("\n\n")
    return [[int(line) for line in group.split("\n")] for group in groups]


def main():
    groups = read()
    carrying = [sum(group) for group in groups]
    print(max(carrying))

    print(sum(sorted(carrying, reverse=True)[:3]))


if __name__ == "__main__":
    main()
