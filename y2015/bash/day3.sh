#!/usr/bin/env bash
input=$(xargs <input/day3.txt)

x=0
y=0
declare -A visited1
visited1[$x, $y]=1

for ((i = 0; i < ${#input}; i++)); do
    case ${input:i:1} in
    '^') ((y++)) ;;
    'v') ((y--)) ;;
    '>') ((x++)) ;;
    '<') ((x--)) ;;
    esac
    visited1[$x, $y]=1
done

read -r x1 y1 x2 y2 <<<"0 0 0 0"
declare -A visited2
visited2[$x1, $y1]=1
visited2[$x2, $y2]=1
for ((i = 0; i < ${#input}; i++)); do
    santas_turn=$((i % 2 == 0))
    case ${input:i:1} in
    '^') ((santas_turn ? y1++ : y2++)) ;;
    'v') ((santas_turn ? y1-- : y2--)) ;;
    '>') ((santas_turn ? x1++ : x2++)) ;;
    '<') ((santas_turn ? x1-- : x2--)) ;;
    esac
    visited2[$x1, $y1]=1
    visited2[$x2, $y2]=1
done

printf "# of squares visited by santa: %i\n" ${#visited1[@]}
printf "# of squares visited by santa/robo santa: %i\n" ${#visited2[@]}
