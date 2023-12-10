import re


def locations(intervals):
    for maps_block in input_maps.split("\n\n"):
        mappings = [
            [int(x) for x in rules.split()] for rules in maps_block.split("\n")[1:]
        ]
        images = []
        while intervals:
            x, y = intervals.pop()
            for mapping in mappings:
                a, b, delta = mapping
                c = b + delta - 1
                t = b - a
                if b <= x <= y <= c:
                    images.append((x - t, y - t))
                    break
                elif b <= x <= c < y:
                    images.append((x - t, c - t))
                    intervals.append((c + 1, y))
                    break
                elif x < b <= y <= c:
                    images.append((b - t, y - t))
                    intervals.append((x, b - 1))
                    break
            else:
                images.append((x, y))
        intervals = images
    return intervals


with open("05.txt") as f:
    input_seeds, input_maps = f.read().strip().split("\n\n", 1)

# ========= PART 1 ==========
seed_data = [int(x) for x in re.findall(r"\d+", input_seeds)]
print(min(min(locations([(x, x) for x in seed_data]))))

# ========= PART 2 ==========
seed_intervals = [(x, x + d - 1) for x, d in zip(seed_data[::2], seed_data[1::2])]
print(min(min(locations(seed_intervals))))
