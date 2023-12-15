package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"strconv"
	"strings"
)

type wire struct {
	mag int
	dir rune
}

func getDir(dir rune) (pt, bool) {
	switch dir {
	case 'U':
		return pt{0, 1}, true
	case 'D':
		return pt{0, -1}, true
	case 'L':
		return pt{-1, 0}, true
	case 'R':
		return pt{1, 0}, true
	default:
		return pt{0, 0}, false
	}
}

func allPoints(wires []wire) map[pt]int {
	var at pt
	dist := 0
	ret := map[pt]int{at: dist}
	for _, w := range wires {
		dir, _ := getDir(w.dir)
		for i := 0; i < w.mag; i++ {
			at = at.addPt(dir)
			dist++
			ret[at] = dist
		}
	}
	return ret
}

func day3() {
	file, err := os.Open("../input/day3.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	i := 0
	var wire1, wire2 []wire
	for scanner.Scan() {
		line := strings.Split(scanner.Text(), ",")
		for _, w := range line {
			dir := w[0]
			mag, _ := strconv.Atoi(w[1:])
			switch i {
			case 0:
				wire1 = append(wire1, wire{mag, rune(dir)})
			case 1:
				wire2 = append(wire2, wire{mag, rune(dir)})
			}
		}
		i++
	}

	pos1, pos2 := allPoints(wire1), allPoints(wire2)
	_ = pos2
	p1Closest, p2Closest := math.MaxInt32, math.MaxInt32 // 32 bits should do
	for p, d1 := range pos1 {
		if d2, ok := pos2[p]; ok && (p.r != 0 || p.c != 0) {
			// go is really testing my patience here jesus christ
			taxiDist := abs(p.r) + abs(p.c)
			p1Closest = min(p1Closest, taxiDist)

			actualDist := d1 + d2
			p2Closest = min(p2Closest, actualDist)
		}
	}

	fmt.Printf("closest distance (manhattan): %v\n", p1Closest)
	fmt.Printf("closest distance (actual): %v\n", p2Closest)
}
