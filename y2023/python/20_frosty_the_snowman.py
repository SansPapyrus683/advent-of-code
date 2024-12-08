import re
import sys
from collections import deque
from math import lcm

START = "broadcaster"
END = "rx"
PUSH_TIMES = 1000

reg_fmt = r"^([%&]?)([a-z]+) \-\> ([a-z,\s]+)$"
flip = {}
conj = {}
send_to = {}
for i in sys.stdin:
    if res := re.findall(reg_fmt, i):
        res = res[0]
        send_to[res[1]] = [r.strip() for r in res[2].split(",")]
        if res[0] == "&":
            conj[res[1]] = {}
        elif res[0] == "%":
            flip[res[1]] = False

targets = None
for r1, st1 in send_to.items():
    if END in st1:
        assert len(st1) == 1
        end_prev = conj[r1]
        targets = []
        for r2, st2 in send_to.items():
            if any(r in end_prev for r in st2):
                targets.append(r2)

    for r2 in st1:
        if r2 in conj:
            # there's probably a more memory efficient way
            conj[r2][r1] = False
assert targets is not None

target_vals = {t: -1 for t in targets}
times = 0
lo, hi = 0, 0
while times < PUSH_TIMES or any(v == -1 for v in target_vals.values()):
    lo += 1
    sig_queue = deque([(START, False)])
    while sig_queue:
        reg, sig = sig_queue.pop()
        for st in send_to[reg]:
            if sig:
                hi += 1
            else:
                lo += 1

            if st in flip:
                if not sig:
                    flip[st] = not flip[st]
                    sig_queue.append((st, flip[st]))
            elif st in conj:
                conj[st][reg] = sig
                nsig = any(not i for i in conj[st].values())
                if target_vals.get(st, 1) == -1 and not nsig:
                    target_vals[st] = times + 1

                sig_queue.append((st, nsig))

    if times == PUSH_TIMES - 1:
        print(f"god what was i thinking: {lo * hi}")
    times += 1

print(f"why did i look at the reddit thread: {lcm(*target_vals.values())}")
