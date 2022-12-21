def fuel(fuel):
    required = [fuel]
    while True:
        req = required[-1] // 3 - 2
        if req > 0:
            required.append(req)
        else:
            break
    return sum(required[1:])


lines = open("01.txt").read().strip().split("\n")
print("part1", sum(int(number) // 3 - 2 for number in lines))
print("part2", sum(fuel(int(number)) for number in lines))
