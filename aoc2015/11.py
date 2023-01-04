import re
import string
from itertools import count


base = 26
nu_digits = (string.digits + string.ascii_lowercase)[:base]
pw_digits = string.ascii_lowercase

fw = dict(zip(nu_digits, pw_digits))
bw = dict(zip(pw_digits, nu_digits))


def convert(s, mapping):
    return "".join(mapping[c] for c in s)


def to_base(num):
    digits = []
    while True:
        num, q = divmod(num, base)
        digits.append(nu_digits[q])
        if not num:
            return "".join(reversed(digits))


def is_valid(pw):
    """
    >>> is_valid("hijklmmn")
    False
    >>> is_valid("abbceffg")
    False
    >>> is_valid("abbcegjk")
    False
    >>> is_valid("abcdffaa")
    True
    >>> is_valid("ghjaabcc")
    True
    """
    if re.search(r"[iol]", pw):
        return False

    pairs = re.findall(r"(.)\1", pw)
    if len(set(pairs)) < 2:
        return False

    ords = [ord(c) for c in pw]
    for c1, c2, c3 in zip(ords, ords[1:], ords[2:]):
        if c1 == c2 - 1 and c1 == c3 - 2:
            return True

    return False


# current = int(convert("hepxcrrq", bw), base)
current = int(convert("hepxxyzz", bw), base)

for i in count(current + 1):
    pw = convert(to_base(i), fw)
    if is_valid(pw):
        print(pw)
        break
