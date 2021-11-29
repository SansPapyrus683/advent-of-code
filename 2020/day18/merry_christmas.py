"""
so this actually isn't what i used to solve the problem
for p1 i actually went through the trouble of making a 
crappy expression parser with no input validation
and for p2 i just googled expression parser and 
messed around with the precedence function
i got this idea from a friend (who used it to solve the thing himself),
and then proceeded to implement it myself
"""
import re


class P1Number:
    """
    for p1numbers, - is really *
    this way, python's normal precedence operators can do all the work
    """
    def __init__(self, val: int) -> None:
        self.val = val

    def __add__(self, other: "P1Number") -> "P1Number":
        return P1Number(self.val + other.val)

    def __sub__(self, other: "P1Number") -> "P1Number":
        return P1Number(self.val * other.val)


class P2Number:
    """
    same logic as p1numbers, but this time
    + is replaced with /
    """
    def __init__(self, val: int) -> None:
        self.val = val

    def __sub__(self, other: "P2Number") -> "P2Number":
        return P2Number(self.val * other.val)

    def __truediv__(self, other: "P2Number") -> "P2Number":
        return P2Number(self.val + other.val)
    
    __floordiv__ = __truediv__  # not needed, just puts my heart at ease


with open('to_you.txt') as read:
    expressions = [line.rstrip() for line in read.readlines()]
    # wrap the numbers in class instantiation thigns
    p1_expr = [
        re.sub(r"\d", lambda m: f"P1Number({m.group(0)})", e).replace('*', '-')
        for e in expressions
    ]
    p2_expr = [
        re.sub(r"\d", lambda m: f"P2Number({m.group(0)})", e).replace('*', '-').replace('+', '/')
        for e in expressions
    ]

p1_total = sum(eval(e).val for e in p1_expr)
p2_total = sum(eval(e).val for e in p2_expr)
print(f"what kind of sadist teacher assigns this homework: {p1_total}")
print(f"but hey, i guess that's the american education system for ya: {p2_total}")
