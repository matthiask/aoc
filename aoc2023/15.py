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


def solve2():
    boxes = [{} for _ in range(256)]
    for s in IN.split(","):
        if s.endswith("-"):
            label = s[:-1]
            box = HASH(label)

            boxes[box].pop(label, None)

        else:
            label, focal_length = s.split("=")
            box = HASH(label)
            focal_length = int(focal_length)

            # Dicts are ordered :-)
            boxes[box][label] = focal_length

    focussing_power = 0
    for box_i, box in enumerate(boxes):
        for slot_i, focal_length in enumerate(box.values()):
            focussing_power += (box_i + 1) * (slot_i + 1) * focal_length
    pp(("part2", focussing_power))


solve2()
