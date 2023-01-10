from itertools import cycle, islice


IN = [int(n) for n in open("16.txt").read().strip()]


def pattern(pos):
    """
    >>> list(islice(pattern(0), 12))
    [1, 0, -1, 0, 1, 0, -1, 0, 1, 0, -1, 0]
    >>> list(islice(pattern(1), 12))
    [0, 1, 1, 0, 0, -1, -1, 0, 0, 1, 1, 0]
    >>> list(islice(pattern(2), 12))
    [0, 0, 1, 1, 1, 0, 0, 0, -1, -1, -1, 0]
    """
    ret = []
    for p in [0, 1, 0, -1]:
        ret.extend([p] * (pos + 1))
    return islice(cycle(ret), 1, None)


def fft(numbers):
    def _gen():
        for pos in range(len(numbers)):
            yield abs(sum(a * b for a, b in zip(numbers, pattern(pos)))) % 10

    return list(_gen())


def test():
    numbers = [int(n) for n in "12345678"]
    for phase in range(10):
        print("phase", phase, "number", "".join(map(str, numbers)))
        numbers = fft(numbers)


def part1():
    numbers = IN[:]
    for _ in range(100):
        numbers = fft(numbers)
    print("".join(map(str, numbers))[:8])


test()
part1()
