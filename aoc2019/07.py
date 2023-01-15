import sys
from itertools import permutations


program = [
    int(n)
    for n in open("07.txt" if len(sys.argv) < 2 else sys.argv[1])
    .read()
    .strip()
    .split(",")
]


def v(program, p, mode, rb):
    if mode == 0:
        # position mode
        return program[program[p]]
    elif mode == 1:
        # immediate mode
        return program[p]
    elif mode == 2:
        # relative mode
        return program[rb + program[p]]
    raise Exception()


def run(program):
    ip = 0
    rb = 0  # relative base
    while True:
        # print(ip, program[:20])
        op = program[ip] % 100
        p1_mode = program[ip] // 100 % 10
        p2_mode = program[ip] // 1000 % 10
        # p3_mode = program[ip] // 10000 % 10
        if op == 1:
            program[program[ip + 3]] = v(program, ip + 1, p1_mode, rb) + v(
                program, ip + 2, p2_mode, rb
            )
            ip += 4
        elif op == 2:
            program[program[ip + 3]] = v(program, ip + 1, p1_mode, rb) * v(
                program, ip + 2, p2_mode, rb
            )
            ip += 4
        elif op == 3:
            program[program[ip + 1]] = yield None
            ip += 2
        elif op == 4:
            yield v(program, ip + 1, p1_mode, rb)
            ip += 2
        elif op == 5:
            if v(program, ip + 1, p1_mode, rb):
                ip = v(program, ip + 2, p2_mode, rb)
            else:
                ip += 3
        elif op == 6:
            if not v(program, ip + 1, p1_mode, rb):
                ip = v(program, ip + 2, p2_mode, rb)
            else:
                ip += 3
        elif op == 7:
            program[program[ip + 3]] = (
                1
                if v(program, ip + 1, p1_mode, rb) < v(program, ip + 2, p2_mode, rb)
                else 0
            )
            ip += 4
        elif op == 8:
            program[program[ip + 3]] = (
                1
                if v(program, ip + 1, p1_mode, rb) == v(program, ip + 2, p2_mode, rb)
                else 0
            )
            ip += 4
        elif op == 9:
            rb += v(program, ip + 1, p1_mode, rb)
            ip += 2
        elif op == 99:
            return
        else:
            raise Exception(f"Unknown op {op}")


def run_once(settings):
    signal = 0
    for setting in settings:
        p = run(program[:])
        p.send(None)
        p.send(setting)
        signal = p.send(signal)
    return signal


def run_loop(settings):
    signal = 0


print("part1")
print(max(run_once(permutation) for permutation in permutations([0, 1, 2, 3, 4])))
