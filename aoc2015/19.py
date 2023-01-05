import re
import sys


IN = [*open("19.txt" if len(sys.argv) < 2 else sys.argv[1])]

element_re = re.compile(r"[A-Z][a-z]*")
molecule = IN[-1].strip()
replacements = {}
for src, dst in (line.strip().split(" => ") for line in IN[:-2]):
    if src not in replacements:
        replacements[src] = []
    replacements[src].append(dst)


# print(molecule)
# print(replacements)
# print(element_re.findall(molecule))


def replace_one(molecule):
    ret = set()
    elements = element_re.findall(molecule)
    for index, element in enumerate(elements):
        if (r := replacements.get(element)) is not None:
            e = elements[:]
            for repl in r:
                e[index] = repl
                ret.add("".join(e))
    return ret


print(len(replace_one(molecule)))
