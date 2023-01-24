from utils import open_input


def score(chars):
    """
    >>> score("{}")
    1
    >>> score("{{{}}}")
    3
    >>> score("{{},{}}")
    3
    >>> score("{{{},{},{{}}}}")
    6
    >>> score("{<{},{},{{}}>}")
    1
    >>> score("{<a>,<a>,<a>,<a>}")
    1
    >>> score("{{<a>},{<a>},{<a>},{<a>}}")
    5
    >>> score("{{<!>},{<!>},{<!>},{<a>}}")
    2
    """

    score = 0
    idx = 0
    length = len(chars)
    depth = 0
    non_canceled_garbage_characters = 0

    while idx < length:
        if chars[idx] == "{":
            idx += 1
            depth += 1
        elif chars[idx] == "}":
            score += depth
            depth -= 1
            idx += 1
        elif chars[idx] == "!":
            # Skip next
            idx += 2
        elif chars[idx] == "<":
            idx += 1

            while True:
                if chars[idx] == "!":
                    idx += 2
                elif chars[idx] == ">":
                    idx += 1
                    break
                else:
                    idx += 1
                    non_canceled_garbage_characters += 1
        else:
            idx += 1

    print("part1", score)
    print("part2", non_canceled_garbage_characters)


score(open_input("09").read().strip())
