package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

const bug = '#'

func gridToState(grid [][]bool) string {
	var ret []byte
	for _, r := range grid {
		for _, c := range r {
			if c {
				ret = append(ret, '1')
			} else {
				ret = append(ret, '0')
			}
		}
	}
	return string(ret)
}

func day24p1() {
	file, err := os.Open("../input/day24.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	var grid [][]bool
	for scanner.Scan() {
		row := scanner.Text()
		grid = append(grid, nil)
		for _, c := range row {
			// probably a better way to write this, but idc
			grid[len(grid)-1] = append(grid[len(grid)-1], c == bug)
		}
	}

	visited := make(map[string]bool)
	for !visited[gridToState(grid)] {
		visited[gridToState(grid)] = true

		newGrid := make([][]bool, len(grid))
		for r := range newGrid {
			newGrid[r] = make([]bool, len(grid[0]))
		}
		for ri, r := range grid {
			for ci, c := range r {
				nBugs := 0
				neighbors := pt{ri, ci}.neighbors4(len(grid), len(grid[0]))
				for _, n := range neighbors {
					if grid[n.r][n.c] {
						nBugs++
					}
				}
				if c {
					newGrid[ri][ci] = nBugs == 1
				} else {
					newGrid[ri][ci] = nBugs == 1 || nBugs == 2
				}
			}
		}

		grid = newGrid
	}

	bdRating := 0
	for ri, r := range grid {
		for ci, c := range r {
			cell := ri*len(grid[0]) + ci
			if c {
				bdRating += 1 << cell
			}
		}
	}

	fmt.Printf("biodiversity rating of first dupe state: %v\n", bdRating)
}
