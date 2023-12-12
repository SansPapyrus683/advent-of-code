from hashlib import md5
from itertools import count

DOOR_ID = "wtnhxymk"
START = "00000"
PW_LEN = 8

pw1 = []
pw2 = [None for _ in range(PW_LEN)]
for i in count(0):
    hash_ = md5((DOOR_ID + str(i)).encode()).hexdigest()
    if hash_.startswith(START):
        if len(pw1) < PW_LEN:
            pw1.append(hash_[len(START)])

        if hash_[len(START)].isdigit():
            pos = int(hash_[len(START)])
            if 0 <= pos < PW_LEN and pw2[pos] is None:
                char = hash_[len(START) + 1]
                pw2[pos] = char

    if len(pw1) == PW_LEN and all(pw2):
        print(f"part 1 pw: {''.join(pw1)}")
        print(f"part 2 pw: {''.join(pw2)}")
        break
