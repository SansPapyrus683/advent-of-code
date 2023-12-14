package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

func day10() {
	file, err := os.Open("../input/day10.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	var asteroids []string
	for scanner.Scan() {
		row := strings.TrimSpace(scanner.Text())
		asteroids = append(asteroids, row)
	}

	astLocs := make(map[pt]bool)
	for r := range asteroids {
		for c := range asteroids[r] {
			if asteroids[r][c] == '#' {
				astLocs[pt{r, c}] = true
			}
		}
	}

	maxDetect := 0
	var bestPt pt
	for a, _ := range astLocs {
		canDetect := 0
		for b, _ := range astLocs {
			if a == b {
				continue
			}
			dr := b.r - a.r
			dc := b.c - a.c
			div := abs(gcd(dr, dc))
			dr, dc = dr / div, dc / div

			at := pt{a.r + dr, a.c + dc}
			blocked := false
			for at.inGrid(len(asteroids), len(asteroids[0])) && at != b {
				if astLocs[at] {
					blocked = true
					break
				}
				at.r += dr
				at.c += dc
			}
			if !blocked {
				canDetect++
			}
		}
		
		if canDetect > maxDetect {
			maxDetect = canDetect
			bestPt = a
		}
	}

	for a, _ := range astLocs {
		if a == bestPt {
			continue
		}
	}

	fmt.Printf("max detectable asteroids: %v\n", maxDetect)
}
