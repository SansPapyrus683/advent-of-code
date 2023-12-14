package main

import (
	"fmt"
	"log"
	"os"
	"math"
	"strconv"
	"strings"
)

const maxConfig = 4
const p2Offset = 5  // {0,1,2,3,4}->{5,6,7,8,9} nice
const ampNum = 5

func toBase(n, b int) []int {
	if n == 0 {
		return []int{0}
	}

	var digits []int
	for n > 0 {
		digits = append(digits, n % b)
		n /= b
	}
	for i := 0; i < len(digits) / 2; i++ {
		j := len(digits) - i - 1
		digits[i], digits[j] = digits[j], digits[i]
	}
	return digits
}

func day7() {
	file, err := os.ReadFile("../input/day7.txt")
	if err != nil {
		log.Fatal(err)  // yk maybe i should remove this, but who really cares
	}

	var prog []int
	for _, i := range strings.Split(string(file), ",") {
		val, _ := strconv.Atoi(strings.TrimSpace(i))
		prog = append(prog, val)
	}

	upTo := int(math.Pow(float64(maxConfig + 1), float64(ampNum)))
	p1MaxOutput, p2MaxOutput := 0, 0
	for i := 0; i < upTo; i++ {
		config := toBase(i, maxConfig + 1)
		for len(config) < ampNum {
			config = append([]int{0}, config...)
		}
		
		unique := make(map[int]bool)
		for _, d := range config {
			unique[d] = true
		}
		if len(unique) != maxConfig + 1 {
			continue
		}
		
		output := 0
		for amp := 0; amp < ampNum; amp++ {
			intcodeAmp := startIntcode(prog)
			intcodeAmp.ioMode = 1
			intcodeAmp.inputQueue = []int{config[amp], output}
			intcodeAmp.run()
			output = intcodeAmp.output[0]
		}
		p1MaxOutput = max(p1MaxOutput, output)

		output = 0
		var amps []intcode
		for a := 0; a < ampNum; a++ {
			p := startIntcode(prog)
			p.ioMode = 1
			p.inputQueue = []int{config[a] + p2Offset}
			amps = append(amps, p)
		}
		for !amps[0].finished {
			for i := range amps {
				a := &amps[i]
				a.inputQueue = append(a.inputQueue, output)
				a.run()
				output = a.output[len(a.output)-1]
			}
		}
		p2MaxOutput = max(p2MaxOutput, output)
	}

	fmt.Printf("max boost (p1): %v\n", p1MaxOutput)
	fmt.Printf("max boost (p2): %v\n", p2MaxOutput)
}
