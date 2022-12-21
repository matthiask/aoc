from itertools import product


range_ = [254032, 789860]
repeats = {f"{i}{i}" for i in range(2, 10)}

descending = set()
for i in range(2, 10):
    for j in range(i + 1, 10):
        descending.add(f"{j}{i}")


def generator():
    numbers = (
        "".join(map(str, digits))
        for digits in product(
            range(2, 10),
            range(2, 10),
            range(2, 10),
            range(2, 10),
            range(2, 10),
            range(2, 10),
        )
    )
    numbers = (
        number for number in numbers if any(repeat in number for repeat in repeats)
    )
    numbers = (number for number in numbers if all(d not in number for d in descending))
    numbers = (number for number in numbers if range_[0] <= int(number) <= range_[1])
    return numbers


print(sum(1 for _ in generator()))


def only_two(number):
    for repeat in repeats:
        if repeat in number:
            three = repeat + repeat[0]
            if three not in number:
                return True
    return False


print(sum(1 for _ in filter(only_two, generator())))
