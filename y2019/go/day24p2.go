package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

const side = 5
const simSteps = 200

type bugPos struct {
	p pt
	z int
}

func (p bugPos) neighbors() []bugPos {
	m := side / 2  // just a shorthand
	if (p.p == pt{m, m}) {
		return nil
	}

	initN := p.p.neighbors4(side, side)
	var ret []bugPos
	for _, n := range initN {
		if (n != pt{m, m}) {
			ret = append(ret, bugPos{n, p.z})
		}
	}

	if p.p.r == 0 {
		ret = append(ret, bugPos{pt{m - 1, m}, p.z + 1})
	}
	if p.p.r == side - 1 {
		ret = append(ret, bugPos{pt{m + 1, m}, p.z + 1})
	}
	if p.p.c == 0 {
		ret = append(ret, bugPos{pt{m, m - 1}, p.z + 1})
	}
	if p.p.c == side - 1 {
		ret = append(ret, bugPos{pt{m, m + 1}, p.z + 1})
	}
	
	switch {
	case p.p.c == m && p.p.r == m - 1:
		for i := 0; i < side; i++ {
			ret = append(ret, bugPos{pt{0, i}, p.z - 1})
		}
	case p.p.c == m && p.p.r == m + 1:
		for i := 0; i < side; i++ {
			ret = append(ret, bugPos{pt{side - 1, i}, p.z - 1})
		}
	case p.p.r == m && p.p.c == m - 1:
		for i := 0; i < side; i++ {
			ret = append(ret, bugPos{pt{i, 0}, p.z - 1})
		}
	case p.p.r == m && p.p.c == m + 1:
		for i := 0; i < side; i++ {
			ret = append(ret, bugPos{pt{i, side - 1}, p.z - 1})
		}
	}

	return ret
}

func day24p2() {
	file, err := os.Open("../input/day24.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	var grid []string
	for scanner.Scan() {
		grid = append(grid, scanner.Text())
		if len(grid[len(grid)-1]) != side {
			panic("invalid # of columns for some row")
		}
	}
	if len(grid) != side {
		panic("invalid # of rows")
	}

	bugs := make(map[bugPos]bool)
	for r := 0; r < side; r++ {
		for c := 0; c < side; c++ {
			if grid[r][c] == bug {
				bugs[bugPos{pt{r, c}, 0}] = true
			}
		}
	}

	for s := 1; s <= simSteps; s++ {
		newBugs := make(map[bugPos]bool)
		for d := -s; d <= s; d++ {
			for r := 0; r < side; r++ {
				for c := 0; c < side; c++ {
					curr := bugPos{pt{r, c}, d}
					nBugs := 0
					for _, n := range curr.neighbors() {
						if bugs[n] {
							nBugs++
						}
					}

					if bugs[curr] {
						if nBugs == 1 {
							newBugs[curr] = true
						}
					} else {
						if nBugs == 1 || nBugs == 2 {
							newBugs[curr] = true
						}
					}
				}
			}
		}
		bugs = newBugs
	}

	fmt.Printf("# of bugs after %v steps: %v\n", simSteps, len(bugs))
}
