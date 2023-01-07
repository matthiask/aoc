import re


IN = [*open("03.txt")]
IN = [tuple(int(dim) for dim in re.findall(r"\d+", line)) for line in IN]
# print(IN)

print(sum(1 for sides in IN if sum(sides) / 2 > max(sides)))


def part2(in_):
    while in_:
        group, in_ = in_[:3], in_[3:]
        for i in range(3):
            yield tuple(g[i] for g in group)


print(sum(1 for sides in part2(IN) if sum(sides) / 2 > max(sides)))
