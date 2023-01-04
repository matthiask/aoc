from collections import defaultdict
from itertools import permutations


people = set()
happiness = defaultdict(lambda: defaultdict(int))
IN = [*open("13.txt")]

for line in IN:
    parts = line.strip().strip(".").split()
    # print(parts)

    people.add(parts[0])
    people.add(parts[10])
    value = int(parts[3]) * (1 if parts[2] == "gain" else -1)
    happiness[parts[0]][parts[10]] = value


def happiness_sum(permutation):
    sum = 0
    for p1, p2 in zip(permutation, permutation[1:] + (permutation[0],)):
        sum += happiness[p1][p2] + happiness[p2][p1]
    return sum


print(max(happiness_sum(permutation) for permutation in permutations(people)))
people.add("Myself")
print(max(happiness_sum(permutation) for permutation in permutations(people)))

# print(people)
# print(happiness)
# print(sum(1 for _ in permutations(people)))
