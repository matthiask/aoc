import sys
from hashlib import md5
from itertools import count


IN = sys.argv[1] if len(sys.argv) > 1 else "iwrupvqb"

for n in count(1):
    if md5(f"{IN}{n}".encode("ascii")).hexdigest().startswith("00000"):
        print(n)
        break

for n in count(1):
    if md5(f"{IN}{n}".encode("ascii")).hexdigest().startswith("000000"):
        print(n)
        break
