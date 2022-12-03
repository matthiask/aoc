import string

priorities = {
    thing: index + 1
    for index, thing in enumerate(string.ascii_lowercase + string.ascii_uppercase)
}


def read():
    with open("input.txt") as f:
        for line in f:
            yield line.strip()


def compartments(lines):
    for line in lines:
        half = len(line) // 2
        yield set(line[:half]), set(line[half:])


def common_priority(compartments):
    same = list(compartments[0] & compartments[1])
    assert len(same) == 1
    return priorities[same[0]]


def group_three(lines):
    while lines:
        group, lines = lines[:3], lines[3:]
        yield group


def common_priority_group(groups):
    for group in groups:
        same = list(set(group[0]) & set(group[1]) & set(group[2]))
        assert len(same) == 1
        yield priorities[same[0]]


if __name__ == "__main__":
    # print(read())
    # print(priorities)
    # print(list(compartments(read())))

    print(sum(common_priority(pack) for pack in compartments(read())))

    print(sum(common_priority_group(group_three(list(read())))))
