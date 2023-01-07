import re
from hashlib import md5
from itertools import count


salt = b"ahsbgdzn"
# salt = b"abc"
three_re = re.compile(r"((.)\2\2)")
five_re = re.compile(r"((.)\2\2\2\2)")


def md5_1(i):
    return md5(salt + str(i).encode("ascii")).hexdigest()


# @lru_cache(maxsize=None)
def md5_2(i):
    d = md5_1(i)
    for _ in range(2016):
        d = md5(d.encode("ascii")).hexdigest()
    return d


def find(alg):
    keys = []
    q = {}
    for i in count():
        d = alg(i)
        if m := three_re.search(d):
            q[i] = m[1]
            # print(q)
        if m := five_re.search(d):
            for j in range(i - 1000, i):
                if q.get(j) == m[1][:3]:
                    keys.append(j)
                    if len(keys) == 64:
                        print(j)
                        return


find(md5_1)
find(md5_2)
