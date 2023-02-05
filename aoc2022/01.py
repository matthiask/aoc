def read_groups():
    groups = open("01.txt").read().strip().split("\n\n")
    return [sum(int(line) for line in group.split("\n")) for group in groups]


def main():
    groups = read_groups()
    print(max(groups))
    print(sum(sorted(groups, reverse=True)[:3]))


if __name__ == "__main__":
    main()
