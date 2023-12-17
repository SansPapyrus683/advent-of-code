package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func typingIntcode(day int) {
	file, err := os.ReadFile(fmt.Sprintf("../input/day%v.txt", day))
	if err != nil {
		log.Fatal(err)
	}

	var prog []int
	for _, i := range strings.Split(string(file), ",") {
		val, _ := strconv.Atoi(strings.TrimSpace(i))
		prog = append(prog, val)
	}

	p := startIntcode(prog)
	p.ioMode = 2
	p.run()
}
