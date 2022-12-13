from ast import literal_eval
from functools import cmp_to_key
from itertools import chain, zip_longest
from pprint import pprint


def read(filename):
    with open(filename) as f:
        pairs = f.read().strip().split("\n\n")

    return [[literal_eval(part) for part in pair.split("\n")] for pair in pairs]


sentinel = object()


def check_ordering(left_list, right_list):
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

            result = check_ordering(left, right)
            if result in {True, False}:
                return result


def test():
    pairs = read("13-test.txt")

    for pair in pairs:
        pprint((check_ordering(*pair), pair))
        print()
    # pprint(pairs)


def part1():
    pairs = read("13.txt")
    pprint(sum(idx + 1 for idx, pair in enumerate(pairs) if check_ordering(*pair)))


def cmp_ordering(left, right):
    return -1 if check_ordering(left, right) else 1


def part2():
    all_packets = [
        [[2]],
        [[6]],
    ] + list(chain.from_iterable(read("13.txt")))
    # pprint(all_packets)

    all_packets = sorted(all_packets, key=cmp_to_key(cmp_ordering))
    # print(all_packets)

    idx1 = 1 + all_packets.index([[2]])
    idx2 = 1 + all_packets.index([[6]])
    pprint(idx1 * idx2)


if __name__ == "__main__":
    # test()
    part1()
    part2()
