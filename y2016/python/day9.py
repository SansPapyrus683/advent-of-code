from queue import LifoQueue


def paren_end(text: str, start: int) -> int:
    parens = LifoQueue()
    parens.put("(")
    end = start
    while not parens.empty():
        end += 1
        if text[end] == "(":
            parens.put("(")
        elif text[end] == ")":
            parens.get()
    return end


def complete_decompress(string: str) -> int:
    at = 0
    decomp_len = 0
    while at < len(string):
        ch = string[at]
        if ch == "(":
            end = paren_end(string, at)
            char_num, repeat_amt = [int(i) for i in string[at + 1:end].split("x")]
            # recurse until all the parenthesis are decompressed
            decomp_len += complete_decompress(
                string[end + 1:end + char_num + 1]
            ) * repeat_amt
            at = end + char_num
        else:
            decomp_len += 1
        at += 1
    return decomp_len


with open("input/day9.txt") as read:
    comp = read.readline().strip()

# p1 doesn't need recursion, i just put it out here
char_at = 0
decomp = ""
while char_at < len(comp):
    c = comp[char_at]
    if c == "(":
        end = paren_end(comp, char_at)
        charsAfter, repeatNum = [int(i) for i in comp[char_at + 1:end].split("x")]
        decomp += comp[end + 1:end + charsAfter + 1] * repeatNum
        char_at = end + charsAfter
    else:
        decomp += c
    char_at += 1

print(f"p1 decompressed len: {len(decomp)}")
print(f"p2 decompressed len: {complete_decompress(comp)}")
