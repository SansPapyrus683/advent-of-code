package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"unicode"
)

const path = '.'
const blocked = '#'
const mazeStart, mazeEnd = "AA", "ZZ"

func day20() {
	file, err := os.Open("../input/day20.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	var grid []string
	for scanner.Scan() {
		grid = append(grid, " "+scanner.Text()+" ")
	}

	// did i really need 100 lines JUST to parse input? yeah...
	rowOuts := make(map[int]bool)
	for ri := range grid {
		var fill []int
		for ci, c := range grid[ri] {
			if c == path || c == blocked {
				fill = append(fill, ci)
			}
		}
		if len(fill) > 0 {
			rowOuts = map[int]bool{fill[0]: true, fill[len(fill)-1]: true}
			break
		}
	}
	colOuts := make(map[int]bool)
	for ci := range grid[0] {
		var fill []int
		for ri := range grid {
			if grid[ri][ci] == path || grid[ri][ci] == blocked {
				fill = append(fill, ri)
			}
		}
		if len(fill) > 0 {
			colOuts = map[int]bool{fill[0]: true, fill[len(fill)-1]: true}
			break
		}
	}

	inner, outer := make(map[pt]string), make(map[pt]string)
	for ri := range grid {
		for ci, c := range grid[ri] {
			if c != path {
				continue
			}
			prev := unicode.IsLetter(rune(grid[ri][ci-1]))
			next := unicode.IsLetter(rune(grid[ri][ci+1]))
			if prev || next {
				var name string
				if prev {
					name = string(grid[ri][ci-2]) + string(grid[ri][ci-1])
				} else {
					name = string(grid[ri][ci+1]) + string(grid[ri][ci+2])
				}
				if rowOuts[ci] {
					outer[pt{ri, ci}] = name
				} else {
					inner[pt{ri, ci}] = name
				}
			}
		}
	}
	for ci := range grid[0] {
		for ri := range grid {
			if grid[ri][ci] != path {
				continue
			}
			prev := unicode.IsLetter(rune(grid[ri-1][ci]))
			next := unicode.IsLetter(rune(grid[ri+1][ci]))
			if prev || next {
				var name string
				if prev {
					name = string(grid[ri-2][ci]) + string(grid[ri-1][ci])
				} else {
					name = string(grid[ri+1][ci]) + string(grid[ri+2][ci])
				}
				if colOuts[ri] {
					outer[pt{ri, ci}] = name
				} else {
					inner[pt{ri, ci}] = name
				}
			}
		}
	}

	inRev, outRev := make(map[string]pt), make(map[string]pt)
	for p, id := range inner {
		inRev[id] = p
	}
	for p, id := range outer {
		outRev[id] = p
	}
	start, end := outRev[mazeStart], outRev[mazeEnd]
	delete(outRev, mazeStart)
	delete(outRev, mazeEnd)

	p1Frontier := []pt{start}
	p1Visited := map[pt]bool{start: true}
	p1Dist := 0
p1Search:
	for ; len(p1Frontier) > 0; p1Dist++ {
		var nextUp []pt
		for _, p := range p1Frontier {
			if p == end {
				break p1Search
			}

			for _, n := range p.neighbors4(len(grid), len(grid[0])) {
				if !p1Visited[n] && grid[n.r][n.c] == path {
					p1Visited[n] = true
					nextUp = append(nextUp, n)
				}
			}
			if id, ok := inner[p]; ok && !p1Visited[outRev[id]] {
				nextUp = append(nextUp, outRev[id])
			} else if id, ok := outer[p]; ok && !p1Visited[inRev[id]] {
				nextUp = append(nextUp, inRev[id])
			}
		}
		p1Frontier = nextUp
	}

	type pt3 struct {
		p pt
		z int
	}
	p2Frontier := []pt3{{start, 0}}
	p2Visited := map[pt3]bool{{start, 0}: true}
	p2Dist := 0
	// really wish i could do both parts in a single bfs :sob:
p2Search:
	for ; len(p2Frontier) > 0; p2Dist++ {
		var nextUp []pt3
		for _, p := range p2Frontier {
			if p.p == end && p.z == 0 {
				break p2Search
			}

			for _, n := range p.p.neighbors4(len(grid), len(grid[0])) {
				next := pt3{n, p.z}
				if !p2Visited[next] && grid[n.r][n.c] == path {
					p2Visited[next] = true
					nextUp = append(nextUp, next)
				}
			}
			if id, ok := inner[p.p]; ok {
				next := pt3{outRev[id], p.z + 1}
				if !p2Visited[next] {
					p2Visited[next] = true
					nextUp = append(nextUp, next)
				}
			} else if id, ok := outer[p.p]; ok && p.z > 0 {
				next := pt3{inRev[id], p.z - 1}
				if !p2Visited[next] {
					p2Visited[next] = true
					nextUp = append(nextUp, next)
				}
			}
		}
		p2Frontier = nextUp
	}

	fmt.Printf("shortest dist for p1: %v\n", p1Dist)
	fmt.Printf("shortest dist for p2: %v\n", p2Dist)
}
