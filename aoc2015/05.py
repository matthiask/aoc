import re


IN = [*open("05.txt")]


def nice1(s):
    """
    >>> nice1("ugknbfddgicrmopn")
    True
    >>> nice1("haegwjzuvuyypxyu")
    False
    """
    if len(re.sub(r"[^aeiou]", "", s)) < 3:
        return False

    if not re.search(r"(.)\1", s):
        return False

    if re.search(r"(ab|cd|pq|xy)", s):
        return False

    return True


def nice2(s):
    """
    >>> nice2("qjhvhtzxzqqjkmpb")
    True
    >>> nice2("xxyxx")
    True
    >>> nice2("uurcxstgmygtbstg")
    False
    """
    if not re.search(r"(..).*\1", s):
        return False
    if not re.search(r"(.).\1", s):
        return False
    return True


print(sum(1 for s in IN if nice1(s)))
print(sum(1 for s in IN if nice2(s)))
