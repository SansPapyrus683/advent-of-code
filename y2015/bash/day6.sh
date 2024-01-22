#!/usr/bin/env bash

while IFS= read -r instr; do
    if [[ $instr =~ (toggle|turn on|turn off)\ ([0-9]+),([0-9]+)\ through\ ([0-9]+),([0-9]+) ]]; then
        case ${BASH_REMATCH[1]} in
        "toggle") ;;
        "turn on") ;;
        "turn off") ;;
        esac
    fi
done <input/day6.txt
