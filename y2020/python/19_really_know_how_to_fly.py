import sys


def matches(msg: str, rules: [str], rule_num: int = 0):
    rule = rules[rule_num]
    if type(rule) == str:
        if msg.startswith(rule):
            return [msg[len(rule):]]
        return []
    elif type(rule) == list:
        valid = []
        for subrule_seq in rule:
            remains = [msg]
            for subr in subrule_seq:
                leftovers = []
                for r in remains:
                    leftovers.extend(matches(r, rules, subr))
                remains = leftovers
            valid.extend(remains)
        return valid
    else:
        raise ValueError("your rules don't follow my rules lol")


da_rules = {}
messages = []
parsing_rules = True
for line in sys.stdin:
    line = line.strip()
    if not line:
        parsing_rules = False
        continue
    elif parsing_rules:
        line = line.split(':')
        rule_num = int(line[0])
        da_rules[rule_num] = []
        rule = line[1]
        if any(c.isalpha() for c in rule):
            da_rules[rule_num] = rule[rule.find('"') + 1:rule.rfind('"')]
        else:
            for subrule in rule.split('|'):
                da_rules[rule_num].append([int(i) for i in subrule.split()])
    else:
        messages.append(line)

all_matching = [m for m in messages if '' in matches(m, da_rules, 0)]
print(f"what kind of message only has a's and b's: {len(all_matching)}")

da_rules[8] = [[42], [42, 8]]
da_rules[11] = [[42, 31], [42, 11, 31]]
all_matching = [m for m in messages if '' in matches(m, da_rules, 0)]
print(f"seems kinda... limited, but who am i to judge: {len(all_matching)}")
