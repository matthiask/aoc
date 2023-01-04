import re


IN = [line.strip() for line in open("08.txt")]


def parse(s):
    """
    >>> parse('""')
    ''
    >>> parse(r'"abc"')
    'abc'
    >>> parse(r'"aaa\"aaa"')
    'aaa"aaa'
    >>> parse('"\\x27"')
    "'"
    >>> parse(r'"\x5em\"squulpy"')
    '^m"squulpy'
    """
    s = s[1:-1].replace("\\\\", "\\").replace(r"\"", '"')
    s = re.sub(r"\\x([0-9a-f]{2})", lambda m: chr(int(m.group(1), 16)), s, flags=re.I)
    return s


def unparse(s):
    """
    >>> unparse("") == '""'
    True
    >>> unparse('""') == r'"\\"\\""'
    True
    >>> unparse(r'"aaa\"aaa"') == r'"\\"aaa\\\\\\"aaa\\""'
    True
    >>> unparse('"x"') == r'"\\"x\\""'
    True
    """

    s = s.replace("\\", "\\\\")
    s = s.replace('"', r"\"")
    return f'"{s}"'


code_characters = sum(map(len, IN))
memory_characters = sum(map(len, map(parse, IN)))
print(code_characters - memory_characters)


unparsed_characters = sum(map(len, map(unparse, IN)))
print(unparsed_characters - code_characters)
