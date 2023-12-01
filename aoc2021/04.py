from itertools import chain
from pprint import pprint


WINS = []
# Horizontally
WINS.extend(list(range(start, start + 5)) for start in range(0, 25, 5))
# Vertically
WINS.extend(list(range(start, start + 25, 5)) for start in range(5))


with open("04.txt") as f:
    numbers = [int(number) for number in next(f).strip().split(",")]
    next(f)

    boards = []
    while True:
        boards.append(
            tuple(
                chain.from_iterable(
                    [int(number) for number in next(f).strip().split()]
                    for _i in range(5)
                )
            )
        )
        try:
            next(f)
        except StopIteration:
            break


pprint(numbers)
pprint(boards)
pprint(WINS)


def part1():
    drawn = set()
    for number in numbers:
        drawn.add(number)
        for board in boards:
            for win in WINS:
                if {board[pos] for pos in win} <= drawn:
                    print("part1:", sum(bn for bn in board if bn not in drawn) * number)
                    return


part1()


def part2():
    winning_boards = set()
    drawn = set()
    for number in numbers:
        drawn.add(number)
        for board in boards:
            if board in winning_boards:
                continue

            for win in WINS:
                if {board[pos] for pos in win} <= drawn:
                    if len(boards) - 1 == len(winning_boards):
                        # Last board!
                        print(
                            "part2:",
                            sum(bn for bn in board if bn not in drawn) * number,
                        )
                        return
                    winning_boards.add(board)
                    break


part2()
