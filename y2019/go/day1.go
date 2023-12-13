package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
)

func fuelNeeded(mod int) int {
	return max(mod/3-2, 0)
}

func day1() {
	file, err := os.Open("../input/day1.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	var modules []int
	for scanner.Scan() {
		m, _ := strconv.Atoi(scanner.Text())
		modules = append(modules, m)
	}

	p1Fuel := 0
	p2Fuel := 0
	for _, m := range modules {
		p1Fuel += fuelNeeded(m)
		for m > 0 {
			p2Fuel += fuelNeeded(m)
			m = fuelNeeded(m)
		}
	}

	fmt.Printf("amt of fuel for p1: %v\n", p1Fuel)
	fmt.Printf("amt of fuel for p2: %v\n", p2Fuel)
}
