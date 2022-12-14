def find_distinct_characters_of_length(signal, length):
    groups = [signal[i:] for i in range(length)]
    for idx, group in enumerate(zip(*groups)):
        if len(group) == len(set(group)):
            return idx + length


if __name__ == "__main__":
    with open("06.txt") as f:
        signal = f.read()

    print(find_distinct_characters_of_length(signal, 4))
    print(find_distinct_characters_of_length(signal, 14))
