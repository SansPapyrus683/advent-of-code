package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
	"strconv"
)

func getDir(dir rune) (int, int, bool) {
	switch rune {
	case 'U': return (0, 1, true)
	case 'D': return (0, -1, true)
	case 'L': return (-1, 0, true)
	case 'R': return (1, 0, true)
	default: return (0, 0, false)
	}
}

type wire struct {
	mag int
	dir rune
}

func day3() {
	file, err := os.Open("../input/day3.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScannier(file)
	i := 0
	var wire1 []wire
	var wire2 []wire
	for scanner.Scan() {
		line := strings.Split(scanner.Text(), ",")
		for _, w := range line {
			dir := w[0]
			mag, _ := strconv.Atoi(w[1:])
			switch i {
			case 0: wire1 = append(wire1, wire{mag, rune(dir)})
			case 1: wire2 = append(wire2, wire{mag, rune(dir)})
			}
		}
		i++
	}
}
