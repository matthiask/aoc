from collections import defaultdict


people = set()
happiness = defaultdict(dict)
IN = [*open("13.txt")]

for line in IN:
    parts = line.strip().strip(".").split()
    print(parts)

    people.add(parts[0])
    people.add(parts[10])
    value = int(parts[3]) * (1 if parts[2] == "gain" else -1)
    happiness[parts[0]][parts[10]] = value

print(people)
print(happiness)
