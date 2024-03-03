import strutils
import sequtils
import sugar  # wtf

let sheet = readFile("input/day2.txt")
  .strip()
  .splitLines()
  .map(r => r.splitWhitespace().map(i => parseInt(i)))
let checksum = sheet
  .map(r => minmax(r))
  .map(mm => mm[1] - mm[0])
  .foldl(a + b)  # what the actual frick

var rowSum = 0
for row in sheet:
  for v, i in row:
    for j in row[v + 1..^1]:
      if i mod j == 0 or j mod i == 0:
        let quotient = if i mod j == 0: i div j else: j div i
        rowSum += quotient

echo "checksum: $1" % [$checksum]
echo "sum of rows: $1" % [$rowSum]
