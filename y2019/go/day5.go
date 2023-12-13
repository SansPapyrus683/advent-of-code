package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func day5() {
	file, err := os.ReadFile("../input/day5.txt")
	if err != nil {
		log.Fatal(err)
	}

	var prog []int
	for _, i := range strings.Split(string(file), ",") {
		val, _ := strconv.Atoi(strings.TrimSpace(i))
		prog = append(prog, val)
	}

	fmt.Println("intcode started!")
	fmt.Println("type in 1 for the answer to p1, or 5 for the answer to p2")
	p := startIntcode(prog)
	p.run()
}
