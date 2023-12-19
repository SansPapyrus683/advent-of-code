package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

const simAmt = 100
const msgLen = 8
const p2OffsetLen = 7
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
	p1Msg := ""
	for i := 0; i < msgLen; i++ {
		p1Msg += strconv.Itoa(p1Signal[i])
	}

	msgOffset := 0
	for i := 0; i < p2OffsetLen; i++ {
		msgOffset = msgOffset*10 + signal[i]
	}
	p2Len := len(signal) * p2RepeatAmt
	if msgOffset < p2Len/2 || p2Len%2 == 1 {
		panic("sorry i can't solve p2 with your input lol")
	}

	coefs := make([]int, p2Len-msgOffset)
	for i := range coefs {
		coefs[i] = 1
	}
	for i := 0; i < simAmt-1; i++ {
		for j := 1; j < len(coefs); j++ {
			coefs[j] = (coefs[j] + coefs[j-1]) % 10
		}
	}

	p2Msg := ""
	for i := msgOffset; i < msgOffset+msgLen; i++ {
		dig := 0
		for j := i; j < p2Len; j++ {
			dig = (dig + coefs[j-i]*signal[j%len(signal)]) % 10
		}
		p2Msg += strconv.Itoa(dig)
	}

	fmt.Printf("p1 msg: %v\n", p1Msg)
	fmt.Printf("p2 msg: %v\n", p2Msg)
}
