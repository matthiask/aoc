from itertools import combinations


def part1(data):
    valid = 0
    imin, imax = 200_000_000_000_000, 400_000_000_000_000
    for l1, l2 in combinations(data, 2):
        xp1, yp1, _, xv1, yv1, _ = l1
        xp2, yp2, _, xv2, yv2, _ = l2

        if yv1 * xv2 == yv2 * xv1:
            continue
        t1 = (yv2 * (xp1 - xp2) - xv2 * (yp1 - yp2)) / (yv1 * xv2 - xv1 * yv2)
        t2 = (yv1 * (xp2 - xp1) - xv1 * (yp2 - yp1)) / (yv2 * xv1 - xv2 * yv1)
        if t1 < 0 or t2 < 0:
            continue
        ix = xp1 + t1 * xv1
        iy = yp1 + t1 * yv1

        if imin <= ix <= imax and imin <= iy <= imax:
            valid += 1
    return valid


import sympy as sym


def part2(data):
    a = [[l[0], l[1], l[2]] for l in data[:4]]
    b = [[l[3], l[4], l[5]] for l in data[:4]]

    t0, t1, t2, t3, l1, l2 = sym.symbols("t0, t1, t2, t3, l1, l2")
    eqs = [
        sym.Eq(
            (a[2][i] - a[0][i]) + t2 * b[2][i] - t0 * b[0][i],
            l1 * ((a[1][i] - a[0][i]) + t1 * b[1][i] - t0 * b[0][i]),
        )
        for i in range(3)
    ]
    eqs += [
        sym.Eq(
            (a[3][i] - a[0][i]) + t3 * b[3][i] - t0 * b[0][i],
            l2 * ((a[1][i] - a[0][i]) + t1 * b[1][i] - t0 * b[0][i]),
        )
        for i in range(3)
    ]
    s = sym.solve(eqs, [t0, t1, t2, t3, l1, l2])[0]
    rock = [
        (s[1] * (a[0][i] + s[0] * b[0][i]) - s[0] * (a[1][i] + s[1] * b[1][i]))
        / (s[1] - s[0])
        for i in [0, 1, 2]
    ]
    return sum(rock)


from re import findall


def main():
    data = [
        [int(d) for d in findall(r"(-?\d+)", line)]
        for line in open("24.txt").read().splitlines()
    ]

    print("Part 1:", part1(data))
    print("Part 2:", part2(data))


if __name__ == "__main__":
    main()
