IN = [*open("18.txt")]
on = {
    complex(x, y)
    for y, line in enumerate(IN)
    for x, c in enumerate(line.strip())
    if c == "#"
}
dim = 100


def surrounding(p):
    """
    >>> list(surrounding(complex(1, 1)))
    [0j, 1j, 2j, (1+0j), (1+2j), (2+0j), (2+1j), (2+2j)]
    """
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            if i == 0 and j == 0:
                continue
            x = p.real + i
            y = p.imag + j
            if 0 <= x < dim and 0 <= y < dim:
                yield complex(x, y)


def next(on):
    all_ = (complex(x, y) for y in range(100) for x in range(100))
    all_ = ((p, p in on, sum(1 for s in surrounding(p) if s in on)) for p in all_)
    # print(list(all_))
    return {
        p
        for p, is_on, surrounding_on in all_
        if (is_on and 2 <= surrounding_on <= 3) or (not is_on and surrounding_on == 3)
    }


if __name__ == "__main__":
    p1 = set(on)
    for _ in range(100):
        p1 = next(p1)
    print(len(p1))

    always_on = {0, 99, 99j, 99 + 99j}
    p2 = on | always_on
    for _ in range(100):
        p2 = next(p2) | always_on
    print(len(p2))
