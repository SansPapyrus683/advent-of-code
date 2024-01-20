#!/usr/bin/env bash
input=$(xargs <input/day1.txt)

floor=0
basement=-1
for ((i = 0; i < ${#input}; i++)); do
  char=${input:$i:1}
  if [ "$char" = "(" ]
  then
    floor=$((floor + 1))
  elif [ "$char" = ")" ]
  then
    floor=$((floor - 1))
  fi

  if [ $floor -eq -1 ] && [ $basement -eq -1 ]
  then
    basement=$((i + 1))
  fi
done

printf "santa's final floor: %i\n" $floor
printf "he first enters the basement at char %i\n" $basement
