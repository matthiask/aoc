from collections import defaultdict


target = 29000000
houses = defaultdict(int)

for elf in range(1, target):
    for house in range(elf, 1000000, elf):
        houses[house] += elf * 10

    if houses[elf] >= target:
        print(elf)
        break


houses = defaultdict(int)
for elf in range(1, target):
    for idx in range(1, 51):
        houses[idx * elf] += elf * 11

    if houses[elf] >= target:
        print(elf)
        break
