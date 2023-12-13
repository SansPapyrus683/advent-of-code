package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

const P1_NOUN = 12
const P1_VERB = 2
const P2_DESIRED = 19690720

func day2() {
	file, err := os.ReadFile("../input/day2.txt")
	if err != nil {
		log.Fatal(err)
	}

	var prog []int
	for _, i := range strings.Split(string(file), ",") {
		val, _ := strconv.Atoi(i)
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

			if noun == P1_NOUN && verb == P1_VERB {
				p1Ans = testProg.prog[0]
			}
			if testProg.prog[0] == P2_DESIRED {
				p2Ans = 100 * noun + verb
			}
		}
	}

	fmt.Printf("register 0 val w/ %v and %v: %v\n", P1_NOUN, P1_VERB, p1Ans)
	fmt.Printf("comb that gives %v: %v\n", P2_DESIRED, p2Ans)
}
