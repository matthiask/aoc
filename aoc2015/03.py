IN = open("03.txt").read().strip()

directions = {
    ">": 1,
    "<": -1,
    "v": 1j,
    "^": -1j,
}


def visited(instructions):
    houses = [0]
    for c in instructions:
        houses.append(houses[-1] + directions[c])
    return set(houses)


print(len(visited(IN)))
print(len(visited(IN[0::2]) | visited(IN[1::2])))
