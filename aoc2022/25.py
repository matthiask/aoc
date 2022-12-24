snafu_digits = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2,
}


def snafu_to_decimal(number):
    dec = 0
    for index, digit in enumerate(reversed(number)):
        dec += snafu_digits[digit] * 5**index
    return dec


def decimal_to_snafu(number):
    pass


if __name__ == "__main__":
    import sys

    inp = [*open(sys.argv[1] if len(sys.argv) > 1 else "25.txt")]
    # print(inp)

    summed = sum([snafu_to_decimal(line.strip()) for line in inp])
    print(summed)
