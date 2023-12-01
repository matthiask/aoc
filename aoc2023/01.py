import re

from tools import open_input


IN = [*open_input("01")]


def extract1(line):
    digits = re.sub(r"[^0-9]", "", line)
    return int(digits[0] + digits[-1])


digits = {str(i): i for i in range(1, 10)}
digits |= {
    s: i + 1
    for i, s in enumerate("one two three four five six seven eight nine".split())
}


def extract2(line):
    first_index = 99999
    first_value = 0
    last_index = -1
    last_value = 0
    for s, i in digits.items():
        idx = line.find(s)
        if 0 <= idx < first_index:
            first_index = idx
            first_value = i
        idx = line.rfind(s)
        if idx > last_index:
            last_index = idx
            last_value = i
    print(line.strip(), first_value, last_value)
    return first_value * 10 + last_value


print(sum(extract2(line) for line in IN))
