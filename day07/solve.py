import re
from collections import defaultdict


folder_sizes = defaultdict(int)
cumulative_folder_sizes = defaultdict(int)

def parse(lines):
    cwd = []
    for line in lines:
        if line.startswith("$ cd /"):
            cwd = []
        elif line.startswith("$ cd .."):
            cwd = cwd[:-1]
        elif line.startswith("$ cd "):
            cwd.append(line[5:])
        elif line.startswith("$ ls"):
            pass
        elif line.startswith("dir "):
            pass
        elif (match := re.match(r"^([0-9]+) (.*)$", line)):
            fsize = int(match.groups()[0])
            folder_sizes["/".join(cwd)] += fsize

            for idx in range(len(cwd) + 1):
                cumulative_folder_sizes["/".join(cwd[:idx])] += fsize
        else:
            raise Exception(f"Unknown: {line!r}")


def part1():
    return sum(size for folder, size in cumulative_folder_sizes.items() if size <= 100000)


if __name__ == "__main__":
    from pprint import pprint

    with open("input.txt") as f:
        lines = [line.strip() for line in f]

    parse(lines)

    # pprint(lines)
    # pprint(folder_sizes)
    pprint(cumulative_folder_sizes)

    print(part1())
