IN = "......^.^^.....^^^^^^^^^...^.^..^^.^^^..^.^..^.^^^.^^^^..^^.^.^.....^^^^^..^..^^^..^^.^.^..^^..^^^.."


def next_row(row):
    def _grouped():
        s = "." + row + "."
        for i in range(1, len(s) - 1):
            # print(i, s[i - 1 : i + 2])
            yield s[i - 1 : i + 2]

    return "".join(
        "^"
        if group
        in {
            "^^.",
            ".^^",
            "^..",
            "..^",
        }
        else "."
        for group in _grouped()
    )


def expand(row, lines):
    yield row
    for _ in range(lines - 1):
        row = next_row(row)
        yield row


# print(sum(line.count(".") for line in grid))

print("\n".join(expand("..^^.", 3)))
print(sum(line.count(".") for line in expand(IN, 40)))
print(sum(line.count(".") for line in expand(IN, 400000)))
