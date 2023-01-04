import re


def expand(s):
    groups = re.findall(r"((.)\2*)", s)
    return "".join(f"{len(g)}{g[0]}" for g, _ in groups)


def iterate(s, times):
    for _ in range(times):
        s = expand(s)
    return s


print(len(iterate("1321131112", 40)))
print(len(iterate("1321131112", 50)))
