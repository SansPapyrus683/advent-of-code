package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

const p1Bound = 50
const p2Size = 100

func inBeam(prog []int, r, c int) bool {
	p := startIntcode(prog)
	p.ioMode = 1
	p.input = []int{c, r}
	p.run()
	return p.output[0] == 1
}

func day19() {
	file, err := os.ReadFile("../input/day19.txt")
	if err != nil {
		log.Fatal(err)
	}

	var prog []int
	for _, i := range strings.Split(string(file), ",") {
		val, _ := strconv.Atoi(strings.TrimSpace(i))
		prog = append(prog, val)
	}

	// man i sure do make alot of assumptions about the input here
	start := pt{-1, -1}
	p1Tracked := 0
	for r := 0; r < p1Bound; r++ {
		for c := 0; c < p1Bound; c++ {
			if inBeam(prog, r, c) {
				if !(r == 0 && c == 0) && (start == pt{-1, -1}) {
					start = pt{r, c}
				}
				p1Tracked++
			}
		}
	}

	rRange := [2]int{start.r, start.r}
	rowHist := map[int][2]int{start.c: rRange}
	var p2Pt pt
	for col := start.c + 1; ; col++ {
		for delta := 0; ; delta++ {
			if inBeam(prog, rRange[0]+delta, col) {
				rRange[0] += delta
				break
			}
		}
		for delta := 1; ; delta++ {
			if !inBeam(prog, rRange[1]+delta, col) {
				rRange[1] += delta - 1
				break
			}
		}

		// for some reason this actually copies the array?
		rowHist[col] = rRange

		if min(rRange[1]-rRange[0]+1, col-start.c+1) >= p2Size {
			startR, endR := rRange[0], rRange[0]+p2Size-1
			valid := true
			for prev := col - 1; prev > col-p2Size; prev-- {
				prevRange := rowHist[prev]
				if !(prevRange[0] <= startR && endR <= prevRange[1]) {
					valid = false
					break
				}
			}
			if valid {
				p2Pt = pt{startR, col - p2Size + 1}
				break
			}
		}
	}

	p2Id := 10000*p2Pt.c + p2Pt.r
	fmt.Printf("points in a %vx%v box: %v\n", p1Bound, p1Bound, p1Tracked)
	fmt.Printf("id of closest %vx%v box that fits: %v\n", p2Size, p2Size, p2Id)
}
