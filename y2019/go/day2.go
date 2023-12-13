package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

const p1Noun = 12
const p1Verb = 2
const p2Desired = 19690720

func day2() {
	file, err := os.ReadFile("../input/day2.txt")
	if err != nil {
		log.Fatal(err)
	}

	var prog []int
	for _, i := range strings.Split(string(file), ",") {
		val, _ := strconv.Atoi(strings.TrimSpace(i))
		prog = append(prog, val)
	}

	var p1Ans int
	var p2Ans int
	for noun := 0; noun < 100; noun++ {
		for verb := 0; verb < 100; verb++ {
			prog[1] = noun
			prog[2] = verb
			testProg := startIntcode(prog)
			testProg.run()

			if noun == p1Noun && verb == p1Verb {
				p1Ans = testProg.prog[0]
			}
			if testProg.prog[0] == p2Desired {
				p2Ans = 100*noun + verb
			}
		}
	}

	fmt.Printf("register 0 val w/ %v and %v: %v\n", p1Noun, p1Verb, p1Ans)
	fmt.Printf("comb that gives %v: %v\n", p2Desired, p2Ans)
}
