package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

const part = '#' // character for scaffolding idk
const robot = '^'

func day17() {
	file, err := os.ReadFile("../input/day17.txt")
	if err != nil {
		log.Fatal(err)
	}

	var prog []int
	for _, i := range strings.Split(string(file), ",") {
		val, _ := strconv.Atoi(strings.TrimSpace(i))
		prog = append(prog, val)
	}

	p := startIntcode(prog)
	p.ioMode = 1
	p.run()
	output := ""
	for _, char := range p.output {
		output += string(char)
	}

	grid := strings.Split(strings.TrimSpace(output), "\n")
	isPart := func(p pt) bool {
		inGrid := p.inGrid(len(grid), len(grid[0]))
		if inGrid {
			return grid[p.r][p.c] == part || grid[p.r][p.c] == robot
		}
		return false
	}

	alignSum := 0
	distReq := 0
	var robPos pt
	for r := range grid {
		for c := range grid[0] {
			if grid[r][c] != part && grid[r][c] != robot {
				continue
			}
			if grid[r][c] == robot {
				robPos = pt{r, c}
			}

			distReq++

			filled := 0
			for _, n := range (pt{r, c}.neighbors4Raw()) {
				if isPart(n) {
					filled++
				}
			}
			if filled == 4 {
				alignSum += r * c
				distReq++ // intersections are travelled over twice
			}
		}
	}

	type move struct { // sometimes i just hate static typing in general
		isTurn bool
		turn   rune
		dist   int
	}
	var moves []move

	dirs := []pt{{-1, 0}, {0, 1}, {1, 0}, {0, -1}}
    at := robPos
	currDir := 0
	travelled := 1 // 1 for the one the robot is curretly on
	// this search makes alot of assumptions about the grid so beware
	for travelled < distReq {
		delta := dirs[currDir]
		n := at.add(delta)
		if isPart(n) {
			dist := 1
			for isPart(n.add(delta)) {
				dist++
				n = n.add(delta)
			}
			at = n
			travelled += dist
			moves = append(moves, move{isTurn: false, dist: dist})
		} else {
			left := (currDir - 1 + len(dirs)) % len(dirs)
			if isPart(at.add(dirs[left])) {
				moves = append(moves, move{true, 'L', 0})
				currDir = left
				continue
			}
			right := (currDir + 1) % len(dirs)
			if isPart(at.add(dirs[right])) {
				moves = append(moves, move{true, 'R', 0})
				currDir = right
			}
		}
	}

	fmt.Printf("sum of alignment parameters: %v\n", alignSum)

	fmt.Println("and here's all the moves needed:")
	for i, m := range moves {
		if m.isTurn {
			fmt.Print(string(m.turn))
		} else {
			fmt.Print(m.dist)
		}
		if i < len(moves)-1 {
			fmt.Print(",")
		}
	}
	fmt.Println()

	prog[0] = 2
	p = startIntcode(prog)
	p.ioMode = 2
	p.run()
}
