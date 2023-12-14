package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

const root = "COM"
const you = "YOU"
const santa = "SAN"

func day6() {
	file, err := os.Open("../input/day6.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	orbits := make(map[string][]string)
	for scanner.Scan() {
		o := strings.Split(scanner.Text(), ")")
		// who thought this was a good way to append to a list
		orbits[o[0]] = append(orbits[o[0]], o[1])
	}

	totDepth := 0
	var calcDepths func(string, []string)
	var myPath, santaPath []string
	calcDepths = func(at string, prev []string) {
		totDepth += len(prev)
		prev = append(prev, at)

		switch at {
		case you:
			myPath = make([]string, len(prev))
			copy(myPath, prev)
		case santa:
			santaPath = make([]string, len(prev))
			copy(santaPath, prev)
		}

		for _, o := range orbits[at] {
			calcDepths(o, prev)
		}
	}
	calcDepths(root, []string{})

	var minDist int
	// i could start from the back, but that's too hard to implement
	for i := 0; ; i++ {
		if myPath[i] == santaPath[i] {
			// probably a better way than just tacking on -4 at the end
			minDist = len(myPath) - i + len(santaPath) - i - 4
		} else {
			break
		}
	}

	fmt.Printf("total # of orbits: %v\nn", totDepth)
	fmt.Printf("min # of orbit transfers: %v\n", minDist)
}
