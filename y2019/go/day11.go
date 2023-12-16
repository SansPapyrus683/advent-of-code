package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func paintShip(prog []int, startColor int) map[pt]int {
	robotDirs := []pt{
		{-1, 0}, {0, 1}, {1, 0}, {0, -1},
	}
	at := pt{0, 0}
	panels := map[pt]int{at: startColor}
	currDir := 1

	robot := startIntcode(prog)
	robot.ioMode = 1
	for !robot.finished {
		robot.inputQueue = append(robot.inputQueue, panels[at])
		robot.run()
		toPaint := robot.output[len(robot.output)-2]
		dir := robot.output[len(robot.output)-1]

		panels[at] = toPaint
		switch dir {
		case 0:
			currDir = (currDir - 1 + len(robotDirs)) % len(robotDirs)
		case 1:
			currDir = (currDir + 1) % len(robotDirs)
		}
		at = at.add(robotDirs[currDir])
	}

	return panels
}

func day11() {
	file, err := os.ReadFile("../input/day11.txt")
	if err != nil {
		log.Fatal(err)
	}

	var prog []int
	for _, i := range strings.Split(string(file), ",") {
		val, _ := strconv.Atoi(strings.TrimSpace(i))
		prog = append(prog, val)
	}

	p1Panels := paintShip(prog, 0)

	p2Panels := paintShip(prog, 1)
	minX, minY := 0, 0
	maxX, maxY := 0, 0
	for pt := range p2Panels {
		minX, minY = min(minX, pt.r), min(minY, pt.c)
		maxX, maxY = max(maxX, pt.r), max(maxY, pt.c)
	}

	canvas := make([][]int, maxY-minY+1)
	for r := range canvas {
		canvas[r] = make([]int, maxX-minX+1)
	}
	for pt, color := range p2Panels {
		x, y := pt.r-minX, pt.c-minY
		canvas[y][x] = color
	}

	fmt.Printf("# of panels painted in p1: %v\n", len(p1Panels))
	fmt.Println("and here's the reg identifier:")
	for i := len(canvas) - 1; i >= 0; i-- {
		for _, c := range canvas[i] {
			if c == 1 {
				fmt.Print("█")
			} else {
				fmt.Print(" ")
			}
		}
		fmt.Println()
	}
}
