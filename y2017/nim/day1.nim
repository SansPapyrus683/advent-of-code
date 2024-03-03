import strutils

let captcha = readFile("input/day1.txt").strip()
assert captcha.len() mod 2 == 0, "captcha length should be even"

let cLen = captcha.len()
var
  p1Tot = 0
  p2Tot = 0
for i in 0 ..< cLen:
  let currVal = int(captcha[i]) - int('0')
  let next1 = captcha[(i + 1) mod cLen]
  let next2 = captcha[(i + cLen div 2) mod cLen]
  p1Tot += int(captcha[i] == next1) * currVal
  p2Tot += int(captcha[i] == next2) * currVal

echo "solution to p1 captcha: $1" % [$p1Tot]
echo "solution to p2 captcha: $1" % [$p2Tot]
