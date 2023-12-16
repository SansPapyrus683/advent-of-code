package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"sort"
	"strings"
)

const p2DestroyAmt = 200

func slope(a, b pt) (int, int, int) {
	dr, dc := b.r-a.r, b.c-a.c
	div := abs(gcd(dr, dc))
	return dr / div, dc / div, div
}

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
	for a := range astLocs {
		canDetect := 0
		for b := range astLocs {
			if a == b {
				continue
			}
			dr, dc, _ := slope(a, b)
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

	type asteroid struct {
		dist float64
		loc  pt
	}
	slopeMap := make(map[float64][]asteroid)
	for a := range astLocs {
		if a == bestPt {
			continue
		}

		dr, dc, div := slope(bestPt, a)
		hyp := math.Sqrt(float64(dr*dr + dc*dc))
		ang := math.Asin(float64(dc) / hyp)
		if dr > 0 {
			ang = math.Pi + ang
		}

		slopeMap[ang] = append(slopeMap[ang], asteroid{hyp * float64(div), a})
	}

	type astSlope struct {
		ang float64
		pts []asteroid
	}
	var slopes []astSlope
	for a, b := range slopeMap {
		sort.Slice(b, func(i, j int) bool {
			return b[i].dist < b[j].dist
		})
		slopes = append(slopes, astSlope{a, b})
	}
	sort.Slice(slopes, func(i, j int) bool {
		return slopes[i].ang < slopes[j].ang
	})

	at := 0
	for ; slopes[at].ang < 0; at++ {
	} // at least i can do this
	var p2Asteroid pt
	for i := 0; i < p2DestroyAmt; i++ {
		for len(slopes[at].pts) == 0 {
			at = (at + 1) % len(slopes)
		}
		currLine := slopes[at].pts
		destroyed := currLine[0].loc
		slopes[at].pts = currLine[1:]
		at = (at + 1) % len(slopes)
		if i == p2DestroyAmt-1 {
			p2Asteroid = destroyed
		}
	}
	p2AstId := p2Asteroid.c*100 + p2Asteroid.r

	fmt.Printf("max detectable asteroids: %v\n", maxDetect)
	fmt.Printf("id of destroyed asteroid #%v: %v\n", p2DestroyAmt, p2AstId)
}
