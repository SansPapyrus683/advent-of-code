#!/usr/bin/env bash

echo "this is going to take a while- check your email or smth"

declare -A lights
declare -A brightness
while IFS= read -r instr; do
    if [[ $instr =~ (toggle|turn on|turn off)\ ([0-9]+),([0-9]+)\ through\ ([0-9]+),([0-9]+) ]]; then
        x1=${BASH_REMATCH[2]}
        y1=${BASH_REMATCH[3]}
        x2=${BASH_REMATCH[4]}
        y2=${BASH_REMATCH[5]}

        for ((i = x1; i <= x2; i++)); do
            for ((j = y1; j <= y2; j++)); do
                pos=$i,$j
                case ${BASH_REMATCH[1]} in
                "toggle")
                    if [ "${lights[$pos]}" ]; then
                        unset "lights[$pos]"
                    else
                        lights[$pos]=1
                    fi
                    ((brightness[$pos] += 2))
                    ;;
                "turn on")
                    lights[$pos]=1
                    ((brightness[$pos]++))
                    ;;
                "turn off")
                    unset "lights[$pos]"
                    if [ "${brightness[$pos]}" ] && [ "${brightness[$pos]}" -gt 0 ]; then
                        ((brightness[$pos]--))
                    fi
                    ;;
                esac
            done
        done
    fi
done <input/day6.txt

tot_brightness=0
for i in "${brightness[@]}"; do
    ((tot_brightness += i))
done

printf "# of lights set: %i\n" ${#lights[@]}
printf "total brightness: %i\n" $tot_brightness
