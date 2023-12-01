program = [int(n) for n in open("05.txt").read().strip().split(",")]


def v(program, p, mode):
    if mode == 0:
        return program[program[p]]
    elif mode == 1:
        return program[p]
    raise Exception()


def run(program, inputs):
    ip = 0
    while True:
        # print(ip, program[:20])
        op = program[ip] % 100
        p1_mode = program[ip] // 100 % 10
        p2_mode = program[ip] // 1000 % 10
        # p3_mode = program[ip] // 10000 % 10
        if op == 1:
            program[program[ip + 3]] = v(program, ip + 1, p1_mode) + v(
                program, ip + 2, p2_mode
            )
            ip += 4
        elif op == 2:
            program[program[ip + 3]] = v(program, ip + 1, p1_mode) * v(
                program, ip + 2, p2_mode
            )
            ip += 4
        elif op == 3:
            program[program[ip + 1]] = inputs.pop(0)
            ip += 2
        elif op == 4:
            print("output", v(program, ip + 1, p1_mode))
            ip += 2
        elif op == 5:
            if v(program, ip + 1, p1_mode):
                ip = v(program, ip + 2, p2_mode)
            else:
                ip += 3
        elif op == 6:
            if not v(program, ip + 1, p1_mode):
                ip = v(program, ip + 2, p2_mode)
            else:
                ip += 3
        elif op == 7:
            program[program[ip + 3]] = (
                1 if v(program, ip + 1, p1_mode) < v(program, ip + 2, p2_mode) else 0
            )
            ip += 4
        elif op == 8:
            program[program[ip + 3]] = (
                1 if v(program, ip + 1, p1_mode) == v(program, ip + 2, p2_mode) else 0
            )
            ip += 4
        elif op == 99:
            return
        else:
            raise Exception(f"Unknown op {op}")


def run2(program):
    for noun in range(100):
        for verb in range(100):
            modified = program[:]
            modified[1] = noun
            modified[2] = verb
            value = run(modified)
            if value == 19690720:
                return 100 * noun + verb


print("part1", run(program[:], inputs=[1]))
print("part2", run(program[:], inputs=[5]))
