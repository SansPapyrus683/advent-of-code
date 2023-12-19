package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

const compNum = 50
const natInd = 255

func day23() {
	file, err := os.ReadFile("../input/day23.txt")
	if err != nil {
		log.Fatal(err)
	}

	var prog []int
	for _, i := range strings.Split(string(file), ",") {
		val, _ := strconv.Atoi(strings.TrimSpace(i))
		prog = append(prog, val)
	}

	net := make([]intcode, compNum)
	for i := 0; i < compNum; i++ {
		net[i] = startIntcode(prog)
		net[i].ioMode = 1
		net[i].input = append(net[i].input, i)
		net[i].run()
	}

	var nat [][]int
	yHist := make(map[int]bool)
	yDupe := -1

	idleStreak := 5 // arbitrarily chosen, 2 or 3 broke my program lol
	currIdleRun := 0
transmit:
	for {
		noOut := true
		for i := range net {
			p := &net[i]
			if len(p.output) > 0 {
				noOut = false
			}
			for o := 0; o < len(p.output); o += 3 {
				ind, x, y := p.output[o], p.output[o+1], p.output[o+2]
				if ind == natInd {
					nat = append(nat, []int{x, y})
					continue
				}
				net[ind].input = append(net[ind].input, []int{x, y}...)
			}
			p.output = nil

			if len(p.input) == 0 {
				p.input = append(p.input, -1)
			}
			p.run()
		}
		if noOut {
			currIdleRun++
		}

		if currIdleRun == idleStreak {
			currIdleRun = 0
			packet := nat[len(nat)-1]
			if yHist[packet[1]] {
				yDupe = packet[1]
				break transmit
			}
			yHist[packet[1]] = true
			net[0].input = append(net[0].input, packet...)
		}
	}

	fmt.Printf("first packet sent to %v: %v\n", natInd, nat[0][1])
	fmt.Printf("first dupe y value send by the nat: %v\n", yDupe)
}
