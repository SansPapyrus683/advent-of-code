#!/usr/bin/env bash
function max {
    echo $(($1 > $2 ? $1 : $2))
}

function min {
    echo $(($1 < $2 ? $1 : $2))
}

function surface_area {
    echo $((2 * ($1 * $2 + $2 * $3 + $1 * $3)))
}

function vol {
    echo $(($1 * $2 * $3))
}

function longest_side {
    max "$(max "$1" "$2")" "$3"
}

total_wrapping=0
total_ribbon=0
while IFS= read -r box || [ "$box" ]; do
    IFS='x' read -ra dims <<<"$box"
    l=${dims[0]}
    w=${dims[1]}
    h=${dims[2]}

    sa=$(surface_area "$l" "$w" "$h")
    vol=$(vol "$l" "$w" "$h")
    slack=$((vol / $(longest_side "$l" "$w" "$h")))
    total_wrapping=$((total_wrapping + sa + slack))

    ribbon=$((2 * (l + w + h - $(longest_side "$l" "$w" "$h"))))
    total_ribbon=$((total_ribbon + ribbon + vol))
done <input/day2.txt

printf "total wrapping required: %i\n" $total_wrapping
printf "total ribbon required: %i\n" $total_ribbon
