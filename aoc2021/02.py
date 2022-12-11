def parse(line):
    match line.split():
        case ("forward", v):
            return (int(v), 0)
        case ("down", v):
            return (0, int(v))
        case ("up", v):
            return (0, -int(v))
        case _:
            raise Exception


with open("02.txt") as f:
    ops = [parse(line.strip()) for line in f]


pos = [0, 0]
for op in ops:
    pos[0] += op[0]
    pos[1] += op[1]

print("part1:", pos[0] * pos[1])


pos = [0, 0]
aim = 0
for op in ops:
    # Fine to run both since op[0] OR op[1] is always zero
    pos[0] += op[0]
    pos[1] += aim * op[0]
    aim += op[1]

print("part2:", pos[0] * pos[1])
