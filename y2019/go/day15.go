package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func newPos(at pt, dir int) pt {
	switch dir {
	case 1:
		at.r--
	case 2:
		at.r++
	case 3:
		at.c--
	case 4:
		at.c++
	}
	return at
}

func day15() {
	file, err := os.ReadFile("../input/day15.txt")
	if err != nil {
		log.Fatal(err)
	}

	var prog []int
	for _, i := range strings.Split(string(file), ",") {
		val, _ := strconv.Atoi(strings.TrimSpace(i))
		prog = append(prog, val)
	}

	movePrio := []int{1, 4, 2, 3} // NESW -> always turns right
	cells := make(map[pt]bool)
	turnLeft := func(cd int) int {
		return (cd - 1 + len(movePrio)) % len(movePrio)
	}
	turnRight := func(cd int) int {
		return (cd + 1) % len(movePrio)
	}

	p := startIntcode(prog)
	p.ioMode = 1

	start := pt{0, 0}
	at := start
	currDir := 0
	oxygen := pt{-1, -1}
	for {
	moveSearch:
		for testD := turnRight(currDir); ; testD = turnLeft(testD) {
			move := movePrio[testD]
			p.input = append(p.input, move)
			p.run()
			output := p.output[len(p.output)-1]

			next := newPos(at, move)
			switch output {
			case 0:
				cells[next] = false
			case 2:
				oxygen = next
				fallthrough
			case 1:
				currDir = testD
				cells[next] = true
				at = next
				break moveSearch
			default:
				panic(fmt.Sprintf("what is this output of %v", output))
			}
		}

		if at == start {
			break
		}
	}

	frontier := []pt{oxygen}
	oxyDist := map[pt]int{oxygen: 0}
	maxDist := 0
	for len(frontier) > 0 {
		var nextUp []pt
		for _, curr := range frontier {
			maxDist = max(maxDist, oxyDist[curr])
			for _, n := range curr.neighbors4Raw() {
				if _, ok := oxyDist[n]; cells[n] && !ok {
					oxyDist[n] = oxyDist[curr] + 1
					nextUp = append(nextUp, n)
				}
			}
		}
		frontier = nextUp
	}

	fmt.Printf("dist to oxygen unit: %v\n", oxyDist[start])
	fmt.Printf("min time for room to fill (might be wrong): %v\n", maxDist)
}
