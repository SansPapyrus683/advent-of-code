import strutils
import sequtils
import sugar
import re
import tables
import sets
import options

proc evenWeight(
  root: string, supporting: Table[string, (int, seq[string])]
): (int, Option[int]) =
  let info = supporting[root]
  if info[1].len == 0:
    return (info[0], none(int))
  
  var
    branches: Table[int, seq[int]]
    toAdjust = none(int)
  for t in info[1]:
    let (weight, adj) = evenWeight(t, supporting)
    if not (weight in branches):
      branches[weight] = @[]
    branches[weight].add(supporting[t][0])
    if adj.isSome:
      toAdjust = adj
  
  case branches.len:
    of 1:
      for w, a in branches.pairs:
        return (w * a.len + info[0], toAdjust)

    of 2:
      if toAdjust.isSome:
        raise newException(ValueError, "bad tree idk man")
      
      let
        tmp = branches.pairs.toSeq
        bad = if tmp[0][1].len == 1: 0 else: 1
        good = 1 - bad
        badDelta = tmp[good][0] - tmp[bad][0]
        changeTo = tmp[bad][1][0] + badDelta
        newWeight = tmp[good][0] * (tmp[good][1].len + 1)

      return (newWeight + info[0], some(changeTo))
    else:
        raise newException(ValueError, "bad tree idk man")

let tower = readFile("input/day7.txt").splitLines()

let
  progFmt = re"^([a-z]+) \((\d+)\) -> ([a-z,\s]+)$"
  progLeafFmt = re"^([a-z]+) \((\d+)\)$"
var supporting: Table[string, (int, seq[string])]
for t in tower:
  var matches1: array[3, string]  # alright this part is pretty cursed lowk
  var matches2: array[2, string]
  if t.find(progFmt, matches1) >= 0:
    supporting[matches1[0]] = (
      parseInt(matches1[1]),
      matches1[2].split(",").map(s => s.strip())
    )
  elif t.find(progLeafFmt, matches2) >= 0:
    supporting[matches2[0]] = (parseInt(matches2[1]), @[])

var notBottom: HashSet[string]
for _, above in supporting.values:
  above.apply(proc(t: string) = notBottom.incl(t))

for t in supporting.keys:
  if not (t in notBottom):
    echo "bottom of tower: $1" % [t]
    let (_, newWeight) = evenWeight(t, supporting)
    if isSome(newWeight):
      echo "adjusted weight to fix crap: $1" % [$newWeight.get]
    else:
      echo "lmao your input must be wrong the tower's alr balanced"
