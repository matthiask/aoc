import re
from itertools import product


IN = [*open("19.txt")]

molecule = IN[-1]
replacements = {}
for src, dst in (line.strip().split(" => ") for line in IN[:-2]):
    if src not in replacements:
        replacements[src] = [src]
    replacements[src].append(dst)

print(molecule)
print(replacements)

element = re.compile(r"[A-Z][a-z]*")
print(element.findall(molecule))


def replace(molecules):
    ret = set()
    for molecule in molecules:
        ret |= {
            "".join(elements)
            for elements in product(
                *[replacements.get(el, [el]) for el in element.findall(molecule)]
            )
        }
    return ret


print(len(replace([molecule])))
