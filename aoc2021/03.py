from collections import defaultdict


with open("03.txt") as f:
    lines = [line.strip() for line in f]


def one_freq(lines):
    freq = defaultdict(int)
    nums = len(lines)
    for line in lines:
        for idx, char in enumerate(line):
            if char == "1":
                freq[idx] += 1
    return {idx: f / nums for idx, f in freq.items()}


def most_common(freq, idx):
    return "1" if freq[idx] >= 0.5 else "0"


freq = one_freq(lines)
gamma = "".join(most_common(freq, idx) for idx in range(12))
epsilon = gamma.replace("0", "x").replace("1", "0").replace("x", "1")


print("part1:", int(gamma, 2) * int(epsilon, 2))


def find_ratings():
    mc_lines = lines[:]
    lc_lines = lines[:]

    for idx in range(12):
        if len(mc_lines) > 1:
            mc = most_common(one_freq(mc_lines), idx)
            mc_lines = [line for line in mc_lines if line[idx] == mc]
        if len(lc_lines) > 1:
            mc = most_common(one_freq(lc_lines), idx)
            lc_lines = [line for line in lc_lines if line[idx] != mc]

    return mc_lines[0], lc_lines[0]


ratings = find_ratings()
print("part2:", int(ratings[0], 2) * int(ratings[1], 2))
