import strutils
import sequtils
import sugar

let prog = readFile("input/day5.txt")
  .strip()
  .splitLines()
  .map(i => parseInt(i))

var
  tmpProg = prog
  at = 0
  steps = 0
while 0 <= at and at < tmpProg.len:
  let prev = at
  at += tmpProg[at]
  inc tmpProg[prev]
  inc steps

echo "# of steps to cmoplete (p1): $1" % [$steps]

tmpProg = prog
at = 0
steps = 0
while 0 <= at and at < tmpProg.len:
  let
    prev = at
    offset = tmpProg[at]
  at += offset
  tmpProg[prev] += (if offset >= 3: -1 else: 1)
  inc steps

echo "# of steps to cmoplete (p2): $1" % [$steps]

