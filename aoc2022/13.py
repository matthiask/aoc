from itertools import zip_longest
from pprint import pprint


def read(filename):
    with open(filename) as f:
        pairs = f.read().strip().split("\n\n")

    return [[eval(part) for part in pair.split("\n")] for pair in pairs]


sentinel = object()


def check(left_list, right_list):
    # print(f"Checking {left_list} vs {right_list}...")
    for left, right in zip_longest(left_list, right_list, fillvalue=sentinel):
        if left is sentinel:
            # Left list runs out of items first
            return True

        elif right is sentinel:
            # Right list runs out of items first
            return False

        elif isinstance(left, int) and isinstance(right, int):
            if left == right:
                continue

            return left < right

        else:
            if not isinstance(left, list):
                left = [left]
            if not isinstance(right, list):
                right = [right]

            result = check(left, right)
            if result in {True, False}:
                return result


def test():
    pairs = read("13-test.txt")

    for pair in pairs:
        pprint((check(*pair), pair))
        print()
    # pprint(pairs)


def part1():
    pairs = read("13.txt")
    pprint(sum(idx + 1 for idx, pair in enumerate(pairs) if check(*pair)))


if __name__ == "__main__":
    # test()
    part1()
