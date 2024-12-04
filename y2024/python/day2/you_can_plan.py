def safe(report: list[int]) -> int:
    diffs = []
    gt = []
    lt = []
    for i in range(len(report) - 1):
        diffs.append(abs(report[i] - report[i + 1]))
        gt.append(report[i + 1] > report[i])
        lt.append(report[i + 1] < report[i])
    return all(1 <= d <= 3 for d in diffs) and (all(gt) or all(lt))


reports = []
with open("on_me.txt") as read:
    for r in read:
        reports.append([int(i) for i in r.split()])

strict_safe = 0
tol_safe = 0
for r in reports:
    strict_safe += safe(r)
    tol_safe += any(safe(r[:i] + r[i + 1:]) for i in range(len(r)))

print(f"ok we're somewhat back: {strict_safe}")
print(f"though these points are only due to server problems haha: {tol_safe}")
