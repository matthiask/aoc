def read():
    with open("01.txt") as f:
        lines = f.read().splitlines()

    group = []
    for line in lines:
        if line:
            group.append(int(line))
        else:
            yield group
            group = []
    if group:
        yield group


def main():
    groups = list(read())
    carrying = [sum(group) for group in groups]
    print(max(carrying))

    print(sum(sorted(carrying, reverse=True)[:3]))


if __name__ == "__main__":
    main()
