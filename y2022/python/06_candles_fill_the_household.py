P1_LEN = 4
P2_LEN = 14

msg = input()

p1_char_amt = -1
p2_char_amt = -1
for i in range(len(msg)):
    if p1_char_amt == -1 and len(set(msg[i:i + P1_LEN])) == P1_LEN:
        p1_char_amt = i + P1_LEN

    if p2_char_amt == -1 and len(set(msg[i:i + P2_LEN])) == P2_LEN:
        p2_char_amt = i + P1_LEN

print(f"holy crap #8 for p1: {p1_char_amt}")
print(f"i probably could've been faster if my ide didn't lag: {p2_char_amt}")
