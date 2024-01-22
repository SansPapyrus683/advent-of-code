#!/usr/bin/env bash

file=input/day5.txt

# holy crap grep is so much faster (i mean i expected that but still)
# basically copied from https://github.com/einarjon/adventofcode.sh/blob/main/2015/05.sh
p1=$(grep -E "[aeiou].*[aeiou].*[aeiou]" $file | grep -E "(.)\1" | grep -E -v -c "(ab|cd|pq|xy)")
p2=$(grep -E "(..).*\1" $file | grep -E -c "(.).\1")

printf "# of nice strings in p1: %i\n" "$p1"
printf "# of nice strings in p2: %i\n" "$p2"
