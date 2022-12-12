def read(filename="13.txt"):
    with open(filename) as f:
        pairs = f.read().strip().split("\n\n")
