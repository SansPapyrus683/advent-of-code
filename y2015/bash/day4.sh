#!/usr/bin/env bash
key=yzbqklnj

p1_found=-1
p2_found=-1
num_at=282749
echo "don't expect this code to finish lol"
while [ $p1_found -eq -1 ] || [ $p2_found -eq -1 ]; do
    hash=$(echo -n "$key""$num_at" | md5sum)
    if [[ $hash =~ ^00000 && $p1_found == -1 ]]; then
        p1_found=$num_at
    fi
    if [[ $hash =~ ^000000 && $p2_found == -1 ]]; then
        p2_found=$num_at
    fi
    ((num_at++))
done

printf "p1 lowest number: %i\n" $p1_found
printf "p2 lowest number: %i\n" $p2_found
