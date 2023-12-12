import re


def has_aba(s: str) -> bool:
    for i in range(3, len(s)):
        if s[i - 3] == s[i] and s[i - 2] == s[i - 1] and s[i - 1] != s[i]:
            return True
    return False


def aba_and_bab(outside: list[str], inside: list[str]) -> bool:
    for o in outside:
        for i in range(2, len(o)):
            if o[i] == o[i - 2] and o[i] != o[i - 1]:
                for ins in inside:
                    if f"{o[i - 1]}{o[i]}{o[i - 1]}" in ins:
                        return True
    return False


with open('day7.txt') as read:
    ips = []
    for l in read.readlines():
        ips.append(l.rstrip())

tls_valid = 0
ssl_valid = 0
for v, a in enumerate(ips):
    supports_tls = False

    out = re.split(r"\[[a-z]*]", a)
    in_ = re.findall(r"\[([^]]+)]", a)
    for seg in out:  # i mean only alphabet anyways
        if has_aba(seg):
            for brack_seg in in_:
                if has_aba(brack_seg):
                    supports_tls = False
                    break
            else:
                supports_tls = True
            break

    tls_valid += 1 if supports_tls else 0
    ssl_valid += 1 if aba_and_bab(out, in_) else 0

print(f"tls valid amt: {tls_valid}")
print(f"ssl valid amt: {ssl_valid}")
