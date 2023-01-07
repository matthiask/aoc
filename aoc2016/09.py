import re


IN = open("09.txt").read().strip()
marker_re = re.compile(r"([^(]*)\((\d+)x(\d+)\)")


def part1(in_):
    out = ""
    while in_:
        m = marker_re.search(in_)
        out += m[1]
        length = int(m[2])
        repeat = int(m[3])

        in_ = in_[m.end() :]
        out += in_[:length] * repeat
        in_ = in_[length:]
    return out


def only_len_part1(in_):
    out = 0
    while in_:
        m = marker_re.search(in_)
        out += len(m[1])
        length = int(m[2])
        repeat = int(m[3])

        in_ = in_[m.end() :]
        out += length * repeat
        in_ = in_[length:]
    return out


print(len(part1(IN)))
print(only_len_part1(IN))
