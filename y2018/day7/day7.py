import re
import heapq

P2_BASE_TIME = 60
P2_WORKER_NUM = 5

step_fmt = r'Step ([A-Z]) must be finished before step ([A-Z]) can begin\.'
do_after = {}
all_steps = set()
with open('day7.txt') as read:
    for limit in read.readlines():
        before, after = next(iter(re.findall(step_fmt, limit)))
        if before not in do_after:
            do_after[before] = []
        do_after[before].append(after)
        all_steps.add(before)
        all_steps.add(after)

before_num = {}
for after in do_after.values():
    for s in after:
        if s not in before_num:
            before_num[s] = 0
        before_num[s] += 1
before_num_copy = before_num.copy()

# sauce: https://www.geeksforgeeks.org/lexicographically-smallest-topological-ordering
frontier = [s for s in all_steps if s not in before_num]
heapq.heapify(frontier)

visited_num = 0
order = []
while frontier:
    curr = heapq.heappop(frontier)
    order.append(curr)
    for after in do_after.get(curr, []):
        before_num[after] -= 1
        if before_num[after] == 0:
            heapq.heappush(frontier, after)
    visited_num += 1

print(f"step order: {''.join(order)}")

before_num = before_num_copy
first = order[0]
done = set()
time_left = {}
for s in order:
    if s not in before_num and len(time_left) < P2_WORKER_NUM:
        time_left[s] = P2_BASE_TIME + ord(s) - ord('A') + 1

time = 0
while len(done) < len(all_steps):
    finished = []
    for s in time_left:
        time_left[s] -= 1
        if time_left[s] == 0:
            finished.append(s)

    for s in finished:
        done.add(s)
        for a in do_after.get(s, []):
            before_num[a] -= 1
        del time_left[s]

    for s, num in before_num.items():
        dupe = s in done or s in time_left
        if not dupe and num == 0 and len(time_left) < P2_WORKER_NUM:
            time_left[s] = P2_BASE_TIME + ord(s) - ord('A') + 1
    time += 1

print(f"min time to complete all steps: {time}")
