import math
import strutils
import std/tables

const INPUT = 347991

const DIRS = [
  (0, 1), (-1, 0), (0, -1), (1, 0),
  (1, 1), (-1, 1), (-1, -1), (1, -1),
]

proc cellVal(n: int): (int, int) =
  var
    k = int(ceil((sqrt(float(n)) - 1) / 2))
    t = 2 * k + 1
    m = t * t
  
  dec t
  if n >= m - t:
    return (k - (m - n), -k)
  else:
    m -= t

  if n >= m - t:
    return (-k, -k + (m - n))
  else:
    m -= t

  return if n >= m - t: (-k + (m - n), k) else: (k, k - (m - n - t))

let cellPos = cellVal(INPUT)
let dist = cellPos[0].abs() + cellPos[1].abs()
echo "manhattan distance of cell #$1: $2" % [$INPUT, $dist]

var seen = {(0, 0): 1}.toTable
var at = 2
while true:
  let pos = cellVal(at)
  var posTotal = 0
  for d in DIRS:
    let n = (pos[0] + d[0], pos[1] + d[1])
    posTotal += seen.getOrDefault(n, 0)

  if posTotal > INPUT:
    echo "first value greater than $1: $2" % [$INPUT, $posTotal]
    break

  seen[pos] = posTotal
  inc at
