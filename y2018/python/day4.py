from dateutil import parser
from datetime import timedelta
from enum import Enum
from collections import defaultdict
import re


class Action(Enum):
    SLEEP = 1
    WAKE = 2
    SHIFT = 3


logs = []
with open('input/day4.txt') as read:
    for log in read.readlines():
        time = log[log.find('[') + 1:log.find(']')]
        action = log[len(time) + 2:].strip()

        guard_string = r'Guard #(\d+) begins shift'
        time = parser.parse(time)
        if action == 'falls asleep':
            logs.append((time, Action.SLEEP))
        elif action == 'wakes up':
            logs.append((time, Action.WAKE))
        elif re.match(guard_string, action):
            guard_id = int(next(iter(re.findall(guard_string, action))))
            logs.append((time, Action.SHIFT, guard_id))

logs.sort()

shift_started = [None]  # first element for edge case
minutes_asleep = defaultdict(lambda: defaultdict(int))
sleep_time = {}
for log in logs:
    guard = shift_started[-1]
    if log[1] == Action.WAKE:
        start = sleep_time[guard]
        while start < log[0]:
            minutes_asleep[guard][start.minute] += 1
            start += timedelta(minutes=1)
    elif log[1] == Action.SLEEP:
        sleep_time[guard] = log[0]
    elif log[1] == Action.SHIFT:
        shift_started.append(log[2])

worst_guard = -1
most_slept = 0
for g, s in minutes_asleep.items():
    time_asleep = sum(s.values())
    if time_asleep > most_slept:
        worst_guard = g
        most_slept = time_asleep

worst_minute = -1
minute_most = 0
for minute, minute_amt in minutes_asleep[worst_guard].items():
    if minute_amt > minute_most:
        minute_most = minute_amt
        worst_minute = minute

print(f"minute slept on most for worst guard: {worst_guard * worst_minute}")

# guard, minute, and how long that minute was slept on
abs_worst_minute = (-1, -1, 0)
for g, s in minutes_asleep.items():
    for minute, minute_amt in s.items():
        if minute_amt > abs_worst_minute[2]:
            abs_worst_minute = (g, minute, minute_amt)

print(f"absolute worst minute: {abs_worst_minute[0] * abs_worst_minute[1]}")
