from hashlib import md5
from itertools import count, islice


IN = b"reyedfim"


def part1():
    def sixth_char_of_zero_prefix_hashes():
        for i in count():
            d = md5(IN + str(i).encode("ascii")).hexdigest()
            if d.startswith("00000"):
                yield d[5]

    print("".join(islice(sixth_char_of_zero_prefix_hashes(), 8)))


def part2():
    pw = [""] * 8
    for i in count():
        d = md5(IN + str(i).encode("ascii")).hexdigest()
        if d.startswith("00000") and "0" <= d[5] <= "7":
            pos = int(d[5])
            char = d[6]
            if not pw[pos]:
                pw[pos] = char
                if all(pw):
                    break
            print(d, pw)
    print("".join(pw))


# part1()
part2()
