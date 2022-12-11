from collections import defaultdict


freq = defaultdict(int)

with open("08.txt") as f:
    for line in f:
        digits = line.strip().split(" | ")[1].split()
        for d in digits:
            freq[len(d)] += 1


print(freq)
print(freq[2] + freq[4] + freq[3] + freq[7])
