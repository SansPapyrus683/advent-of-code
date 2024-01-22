#!/usr/bin/env bash

function p1_nice {
    if [[ $1 =~ ab|cd|pq|xy ]]; then
        return 1
    fi
    
    vowels=0
    double_req=0
    for ((i = 0; i < ${#1}; i++)); do
        char=${1:i:1}
        if [[ $char =~ [aeiou] ]]; then
            ((vowels++))
        fi
        if [ "$i" -gt 0 ] && [ "$char" = "${1:i - 1:1}" ]; then
            double_req=1
        fi
    done
    # bash returns the last evaluated expression i think
    [ "$vowels" -ge 3 ] && [ "$double_req" -eq 1 ]
}

function p2_nice {
    declare -A pairs
    pair_req=0
    sandwich_req=0
    for ((i = 0; i < ${#1}; i++)); do
        char=${1:i:1}
        if [ "$i" -ge 3 ]; then
            can_add=${1:i - 3:2}
            pairs[$can_add]=1
            if [ "${pairs[${1:i - 1:2}]}" = 1 ]; then
                pair_req=1
            fi
        fi
        if [ "$i" -gt 1 ] && [ "$char" = "${1:i - 2:1}" ]; then
            sandwich_req=1
        fi
    done
    [ "$sandwich_req" -eq 1 ] && [ "$pair_req" -eq 1 ]
}

p1_nice_num=0
p2_nice_num=0
while IFS= read -r string || [ "$string" ]; do
    if p1_nice "$string"; then
        ((p1_nice_num++))
    fi
    if p2_nice "$string"; then
        ((p2_nice_num++))
    fi
done <input/day5.txt

printf "# of nice strings in p1: %i\n" "$p1_nice_num"
printf "# of nice strings in p2: %i\n" "$p2_nice_num"
