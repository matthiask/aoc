from pprint import pp

from tools import open_input


IN = open_input("14").read().strip().split("\n")
W = len(IN[0])
H = len(IN)


def parse_dish():
    cubes = {complex(x, y) for y in range(H) for x in range(W) if IN[y][x] == "#"}
    balls = {complex(x, y) for y in range(H) for x in range(W) if IN[y][x] == "O"}
    return cubes, balls


def print_dish(cubes, balls):
    print(
        "\n".join(
            "".join(
                "O"
                if complex(x, y) in balls
                else "#"
                if complex(x, y) in cubes
                else "."
                for x in range(W)
            )
            for y in range(H)
        )
    )


def tilt(cubes, balls, direction, check):
    new_balls = set()

    if direction == -1j:
        balls = sorted(balls, key=lambda ball: ball.imag, reverse=False)
    if direction == -1:
        balls = sorted(balls, key=lambda ball: ball.real, reverse=False)
    if direction == 1j:
        balls = sorted(balls, key=lambda ball: ball.imag, reverse=True)
    if direction == 1:
        balls = sorted(balls, key=lambda ball: ball.real, reverse=True)

    for ball in balls:
        while (
            check(ball)
            and ball + direction not in cubes
            and ball + direction not in new_balls
        ):
            ball += direction
        new_balls.add(ball)
    return frozenset(new_balls)


def load(balls):
    return int(sum(H - ball.imag for ball in balls))


def solve1():
    cubes, balls = parse_dish()
    # pp(balls)
    print_dish(cubes, balls)
    new_balls = tilt(cubes, balls, -1j, lambda ball: ball.imag > 0)
    print()
    print_dish(cubes, new_balls)
    pp(("load", load(new_balls)))


def solve2():
    cubes, balls = parse_dish()

    balls_to_cycle = {}

    cycles = 1000000000
    c = 0
    while c < cycles:
        balls = tilt(cubes, balls, -1j, lambda ball: ball.imag > 0)
        balls = tilt(cubes, balls, -1, lambda ball: ball.real > 0)
        balls = tilt(cubes, balls, 1j, lambda ball: ball.imag < H - 1)
        balls = tilt(cubes, balls, 1, lambda ball: ball.real < W - 1)

        if balls in balls_to_cycle:
            start = balls_to_cycle[balls]
            end = c
            c += int((cycles - end) / (end - start)) * (end - start)
            print(f"Cycle found at {end} (started at {start}), skipping ahead to {c}")
        else:
            balls_to_cycle[balls] = c

        # print(balls)

        c += 1

    print_dish(cubes, balls)
    pp(("load", load(balls)))


solve1()
solve2()
