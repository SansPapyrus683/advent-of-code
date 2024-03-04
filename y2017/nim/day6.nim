import strutils
import sequtils
import sugar
import tables

var blocks = readFile("input/day6.txt").splitWhitespace().map(i => parseInt(i))

# no way you can have a hashtable of lists
var seen: Table[seq[int], int] = {blocks: 0}.toTable
while true:
  var toRedist = (0, 0)
  for ind, val in blocks:
    if val > toRedist[1]:
      toRedist = (ind, val)

  blocks[toRedist[0]] = 0
  for i in 1..toRedist[1]:
    inc blocks[(toRedist[0] + i) mod blocks.len]

  if blocks in seen:
    break
  seen[blocks] = seen.len

echo "# of cycles b4 smth's seen again: $1" % [$seen.len]
echo "loop size: $1" % [$(seen.len - seen[blocks])]

