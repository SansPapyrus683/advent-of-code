package main

import (
	"fmt"
	"log"
	"os"
	"strings"
	"math"
)

const width = 25
const height = 6

func day8() {
	file, err := os.ReadFile("../input/day8.txt")
	if err != nil {
		log.Fatal(err)
	}

	img := strings.TrimSpace(string(file))
	minZeros := math.MaxInt32
	p1Ans := 0
	var layers [][][]int
	for at := 0; at < len(img); {
		digits := make(map[int]int)
		var layer [][]int = make([][]int, height)

		for r := 0; r < height; r++ {
			for c := 0; c < width; c++ {
				pixel := int(img[at] - '0')
				layer[r] = append(layer[r], pixel)
				digits[pixel]++
				at++
			}
		}
		layers = append(layers, layer)
		
		if digits[0] < minZeros {
			minZeros = digits[0]
			p1Ans = digits[1] * digits[2]
		}
	}

	var output [][]int = make([][]int, height)
	for r := 0; r < height; r++ {
		for c := 0; c < width; c++ {
			for _, l := range layers {
				if l[r][c] != 2 {
					output[r] = append(output[r], l[r][c])
					break
				}
			}
		}
	}

	fmt.Printf("# of 1's * # of 2's: %v\n", p1Ans)
	fmt.Println("message:")
	for _, r := range output {
		for _, c := range r {
			if c == 0 {
				fmt.Print(" ")
			} else {
				fmt.Print("█")
			}
		}
		fmt.Println()
	}
}
