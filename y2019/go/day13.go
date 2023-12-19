package main

import (
	"fmt"
	"log"
	"os"
	"slices"
	"strconv"
	"strings"
)

func toBoard(output []int) ([][]int, int) {
	maxR, maxC := 0, 0
	for i := 0; i < len(output); i += 3 {
		c, r := output[i], output[i+1]
		maxR, maxC = max(maxR, r), max(maxC, c)
	}

	board := make([][]int, maxR+1)
	for r := range board {
		board[r] = make([]int, maxC+1)
	}
	score := -1
	for i := 0; i < len(output); i += 3 {
		c, r, tid := output[i], output[i+1], output[i+2]
		if r == 0 && c == -1 {
			score = tid
		} else {
			board[r][c] = tid
		}
	}

	return board, score
}

func printBoard(board [][]int, score int) {
	tidToChar := map[int]rune{0: ' ', 1: '█', 2: '#', 3: '_', 4: '●'}
	for r := range board {
		for _, c := range board[r] {
			fmt.Print(string(tidToChar[c]))
		}
		fmt.Println()
	}
	if score != -1 {
		fmt.Printf("Score: %v\n", score)
	}
}

func day13() {
	file, err := os.ReadFile("../input/day13.txt")
	if err != nil {
		log.Fatal(err)
	}

	var prog []int
	for _, i := range strings.Split(string(file), ",") {
		val, _ := strconv.Atoi(strings.TrimSpace(i))
		prog = append(prog, val)
	}

	p := startIntcode(prog)
	p.ioMode = 1
	p.run()

	board, _ := toBoard(p.output)
	blockNum := 0
	for r := range board {
		for _, c := range board[r] {
			if c == 2 {
				blockNum++
			}
		}
	}

	prog[0] = 2 // insert 2 quarters or smth idk
	p = startIntcode(prog)
	p.ioMode = 1
	var score int
	input := -2
	for !p.finished {
		if slices.Contains([]int{-1, 0, 1}, input) {
			p.input = append(p.input, input)
		}
		p.run()

		board, score = toBoard(p.output)
		var paddle, ball pt
		for ri := range board {
			for ci, c := range board[ri] {
				switch c {
				case 3:
					paddle = pt{ri, ci}
				case 4:
					ball = pt{ri, ci}
				}
			}
		}

		// printBoard(board, score)  // if you wanna...

		switch {
		case paddle.c < ball.c:
			input = 1
		case paddle.c > ball.c:
			input = -1
		case paddle.c == ball.c:
			input = 0
		}
	}

	fmt.Printf("# of blocks: %v\n", blockNum)
	fmt.Printf("final score: %v\n", score)
}
