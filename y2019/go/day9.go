package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

// yes, this is basically the same thing as day 5.
func day9() {
	file, err := os.ReadFile("../input/day9.txt")
	if err != nil {
		log.Fatal(err)
	}

	var prog []int
	for _, i := range strings.Split(string(file), ",") {
		val, _ := strconv.Atoi(strings.TrimSpace(i))
		prog = append(prog, val)
	}

	fmt.Println("intcode for day 9 started!")
	fmt.Println("type in 1 for the answer to p1, or 2 for the answer to p2")
	p := startIntcode(prog)
	p.run()
}
