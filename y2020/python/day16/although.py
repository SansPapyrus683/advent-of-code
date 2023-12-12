requirements = []
theirs = []
req_num = 0
wanted_reqs = []
with open('its_been_said.txt') as read:
    state = None
    for line in read.readlines():
        line = line.strip()
        if line == 'your ticket:':  # this parsing is really hacky but hey, perfect day1.txt!
            state = False

        elif line == 'nearby tickets:':
            state = True

        elif ':' in line:
            if line.startswith('departure'):
                wanted_reqs.append(req_num)
            line = [r.strip() for r in line[line.find(':') + 1:].split('or')]
            reqs = []
            for r in line:
                reqs.append([int(i) for i in r.split('-')])
            requirements.append(reqs)
            req_num += 1

        elif ',' in line:
            if state is not None and not state:
                mine = [int(i) for i in line.split(',')]
            else:
                theirs.append([int(i) for i in line.split(',')])
assert len({len(t) for t in theirs}) == 1, "all tickets should be consistent my guy"

valid_tickets = []
error_rate = 0
for t in theirs:
    overall_valid = True
    for field in t:
        if not any(any(range_[0] <= field <= range_[1] for range_ in req) for req in requirements):
            error_rate += field
            overall_valid = False
    if overall_valid:
        valid_tickets.append(t)
print("where did we have the time to write down so many tickets lol: %i" % error_rate)

possible = [[] for _ in range(len(valid_tickets[0]))]
for v, r in enumerate(requirements):
    for i in range(len(valid_tickets[0])):
        # if all of the numbers in row i satisfy the range requirements, add it
        if all(any(range_[0] <= t[i] <= range_[1] for range_ in r) for t in valid_tickets):
            possible[i].append(v)

assigned = [None for _ in range(len(valid_tickets[0]))]
while any(a is None for a in assigned):
    for v, p in enumerate(possible):
        if len(p) == 1:  # ok, we've narrowed it down to a single possibility
            to_assign = p[0]
            assigned[v] = to_assign
            for other in possible:
                if to_assign in other:
                    other.remove(to_assign)

prod = 1
for v, a in enumerate(assigned):
    if a in wanted_reqs:
        prod *= mine[v]
print("and maybe you could just ask one of the locals who's bilingual too: {prod}")
