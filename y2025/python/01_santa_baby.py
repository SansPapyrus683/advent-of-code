import sys

MOD = 100

lock = 50
pw1 = 0
pw2 = 0
for rot in sys.stdin:
    dir_, amt = rot[0], int(rot[1:])
    if dir_ == "L":
        use = min(amt, lock)
        amt -= use
        lock -= use
        pw2 += (lock == 0 and use > 0) + (amt // MOD)
        lock = (lock - amt) % MOD

    elif dir_ == "R":
        use = min(amt, MOD - lock)
        amt -= use
        lock = (lock + use) % MOD
        # the use > 0 condition is unneeded bc if lock = 0 then it's 100
        pw2 += (lock == 0) + (amt // MOD)
        lock = (lock + amt) % MOD

    pw1 += lock == 0

print(f"you can brute force this btw: {pw1}")
print(f"but like i prefer fast solutions so... {pw2}")
