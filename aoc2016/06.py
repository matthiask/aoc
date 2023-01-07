from collections import Counter


IN = [*open("06.txt")]
pos = [Counter(res) for res in zip(*IN)]
print("".join(p.most_common(1)[0][0] for p in pos))
print("".join(p.most_common()[-1][0] for p in pos))
