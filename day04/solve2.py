import re

def parse():
    with open("input.txt") as f:
        for line in f:
            yield [int(part) for part in re.split(r"[-,]", line.strip())]


def one_contains_other(start1, end1, start2, end2):
    return start1 <= start2 and end1 >= end2 or start1 >= start2 and end1 <= end2


def overlap(start1, end1, start2, end2):
    # https://nedbatchelder.com/blog/201310/range_overlap_in_two_compares.html
    return end1 >= start2 and end2 >= start1


if __name__ == "__main__":
    print(sum(1 for pairing in parse() if one_contains_other(*pairing)))
    print(sum(1 for pairing in parse() if overlap(*pairing)))
