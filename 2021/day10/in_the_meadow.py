from statistics import median

OPENING = "([{<"
CLOSING = ")]}>"
P1_SCORES = {c: s for c, s in zip(CLOSING, [3, 57, 1197, 25137])}
P2_SCORES = {c: s for c, s in zip(OPENING, [1, 2, 3, 4])}
CORR_OPENING = {c: o for c, o in zip(CLOSING, OPENING)}

with open("building_snowmen.txt") as read:
    nav_subs = [r.strip() for r in read.readlines()]

total_error = 0
closing_scores = []
for s in nav_subs:
    curr_openings = []
    for c in s:
        if c in OPENING:
            curr_openings.append(c)
        elif c in CLOSING:
            if not curr_openings or CORR_OPENING[c] != curr_openings[-1]:
                total_error += P1_SCORES[c]
                break
            else:
                curr_openings.pop()
    else:
        score = 0
        for c in reversed(curr_openings):
            score = (score * 5) + P2_SCORES[c]
        closing_scores.append(score)

assert len(closing_scores) % 2 == 1, "there should be an odd # of scores for p2"
print(f"you could tell eric was running out of ideas for flavor text: {total_error}")
print(f"thank god for stats.median: {median(closing_scores)}")
