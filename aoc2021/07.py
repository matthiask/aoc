with open("07.txt") as f:
    INITIAL = [int(days) for days in f.read().strip().split(",")]


print(INITIAL)
MIN = min(INITIAL)
MAX = max(INITIAL)


def cost_linear(where):
    return sum(abs(pos - where) for pos in INITIAL)


costs = {where: cost_linear(where) for where in range(MIN, MAX)}
print(min(costs.values()))


fuel_per_distance = []
for idx in range(2000):
    fuel_per_distance.append((idx * (idx + 1)) // 2)

# print(fuel_per_distance)


def cost_sum(where):
    return sum(fuel_per_distance[abs(pos - where)] for pos in INITIAL)


costs = {where: cost_sum(where) for where in range(MIN, MAX)}
print(min(costs.values()))
