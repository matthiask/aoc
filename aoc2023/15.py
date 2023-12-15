from pprint import pp

from tools import open_input


IN = open_input("15").read().strip()


def HASH(string):  # noqa: N802
    current_value = 0
    for s in string:
        current_value = ((current_value + ord(s)) * 17) % 256
    return current_value


# print("HASH", HASH("HASH"))
# pp([(s, HASH(s)) for s in IN.split(",")])

pp(("part1", sum(map(HASH, IN.split(",")))))
