program = [int(n) for n in open("02.txt").read().strip().split(",")]


def run(program):
    for ip in range(0, 9999, 4):
        op, n1, n2, tg = program[ip : ip + 4]
        if op == 1:
            program[tg] = program[n1] + program[n2]
        elif op == 2:
            program[tg] = program[n1] * program[n2]
        elif op == 99:
            # print(program)
            return program[0]
        else:
            raise Exception()


def run2(program):
    for noun in range(100):
        for verb in range(100):
            modified = program[:]
            modified[1] = noun
            modified[2] = verb
            value = run(modified)
            if value == 19690720:
                return 100 * noun + verb


part1 = program[:]
part1[1] = 12
part1[2] = 2
print("part1", run(part1))
print("part2", run2(program))
