package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

const simAmt = 100
const outLen = 8
const p2RepeatAmt = 10000

func p1FFT(signal []int) []int {
	var ret []int
	coefs := [...]int{0, 1, 0, -1}
	for i := range signal {
		tot := 0
		for j, val := range signal {
			coef := coefs[(j+1)/(i+1)%4]
			tot += val * coef
		}
		ret = append(ret, abs(tot)%10)
	}
	return ret
}

func day16() {
	file, err := os.ReadFile("../input/day16.txt")
	if err != nil {
		log.Fatal(err)
	}

	var signal []int
	for _, c := range strings.TrimSpace(string(file)) {
		signal = append(signal, int(c-'0'))
	}

	var p1Signal = make([]int, len(signal))
	copy(p1Signal, signal)
	for i := 0; i < simAmt; i++ {
		p1Signal = p1FFT(p1Signal)
	}
	var p1Output string
	for i := 0; i < outLen; i++ {
		p1Output += strconv.Itoa(p1Signal[i])
	}

	fmt.Printf("p1 msg (i'll get around to p2 sometime never): %v\n", p1Output)
}
