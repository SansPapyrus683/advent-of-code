import strutils
import sequtils
import algorithm
import sets

proc validPhrases1(phrase: string): bool = 
  var found: HashSet[string]
  for p in phrase.splitWhitespace():
    if p in found:
      return false
    found.incl(p)
  return true

proc validPhrases2(phrase: string): bool =
  var found: HashSet[string]
  for p in phrase.splitWhitespace():
    var pChars = toSeq(p.items)
    sort(pChars, system.cmp)

    let sortedP = $pChars
    if sortedP in found:
      return false
    found.incl(sortedP)
  return true

var valid1 = 0
var valid2 = 0
readFile("input/day4.txt")
  .strip()
  .splitLines()
  .apply(proc(p: string) =
    valid1 += (if validPhrases1(ref p): 1 else: 0)
    valid2 += (if validPhrases2(ref p): 1 else: 0))

echo "# of valid passphrases (p1): ", valid1
echo "# of valid passphrases (p2): ", valid2

