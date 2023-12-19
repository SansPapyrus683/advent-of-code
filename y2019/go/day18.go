package main

import (
	"bufio"
	"container/heap"
	"fmt"
	"log"
	"os"
	"slices"
	"strings"
	"unicode"
)

const me = '@'
const wall = '#'

// short for "neptune state", not "neighboring state"
type nState struct {
	at  string
	inv string
}

func (ns nState) addKey(key rune) nState {
	keys := append([]rune(ns.inv), key)
	slices.Sort(keys)
	ns.inv = string(keys)
	return ns
}

func (ns nState) canTake(key rune, prereqs map[rune]bool) bool {
	met := 0
	for _, c := range ns.inv {
		if c == key {
			return false
		}
		if prereqs[c] {
			met++
		}
	}
	return met == len(prereqs)
}

func day18() {
	file, err := os.Open("../input/day18.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	var grid [][]rune
	for scanner.Scan() {
		grid = append(grid, []rune(scanner.Text()))
	}

	var start pt
	for ri := range grid {
		for ci, c := range grid[ri] {
			if c == me {
				start = pt{ri, ci}
			}
		}
	}

	prStack := make(map[rune]int)
	prereqs := make(map[rune]map[rune]bool)
	keyPos := map[rune]pt{me: start}
	visited := make(map[pt]bool)
	var findPrereqs func(pt)
	findPrereqs = func(at pt) {
		currChar := grid[at.r][at.c]
		if currChar == wall || visited[at] {
			return
		}
		visited[at] = true

		if unicode.IsLower(currChar) {
			prStackCopy := make(map[rune]bool)
			for k, v := range prStack {
				if v > 0 {
					prStackCopy[k] = true
				}
			}
			prereqs[currChar] = prStackCopy
			keyPos[currChar] = at
		}
		isRelevant := unicode.IsLetter(currChar)
		if isRelevant {
			prStack[unicode.ToLower(currChar)]++
		}

		for _, n := range at.neighbors4(len(grid), len(grid[0])) {
			findPrereqs(n)
		}
		if isRelevant {
			prStack[unicode.ToLower(currChar)]--
		}
	}
	findPrereqs(start)

	keyDist := make(map[rune]map[rune]int)
	for k, p := range keyPos {
		keyDist[k] = make(map[rune]int)
		visited = make(map[pt]bool)
		frontier := []pt{p}
		visited[p] = true
		for i := 0; len(keyDist[k]) < len(prereqs); i++ {
			var nextUp []pt
			for _, at := range frontier {
				currChar := grid[at.r][at.c]
				if unicode.IsLower(currChar) {
					keyDist[k][currChar] = i
				}
				for _, n := range at.neighbors4(len(grid), len(grid[0])) {
					if !visited[n] && grid[n.r][n.c] != wall {
						visited[n] = true
						nextUp = append(nextUp, n)
					}
				}
			}
			frontier = nextUp
		}
	}

	// dijkstra's for p1
	frontier := make(PriorityQueue[nState], 0)
	minDist := make(map[nState]int)
	sState := nState{string(me), ""}
	minDist[sState] = 0
	heap.Push(&frontier, &Item[nState]{value: sState, priority: 0})
	var p1AllKeys int
	for len(frontier) > 0 {
		tempCurr := heap.Pop(&frontier).(*Item[nState])
		if minDist[tempCurr.value] != -tempCurr.priority {
			continue
		}
		curr := tempCurr.value
		if len(curr.inv) == len(prereqs) {
			p1AllKeys = minDist[curr]
			break
		}

		for newK, pr := range prereqs {
			if !curr.canTake(newK, pr) {
				continue
			}

			nextState := curr.addKey(newK)
			nextState.at = string(newK)
			nextCost := minDist[curr] + keyDist[rune(curr.at[0])][newK]
			if alr, ok := minDist[nextState]; !ok || nextCost < alr {
				minDist[nextState] = nextCost
				nItem := Item[nState]{value: nextState, priority: -nextCost}
				heap.Push(&frontier, &nItem)
			}
		}
	}

	quadrants := map[pt]int{
		{-1, -1}: 0, {-1, 1}: 1, {1, 1}: 2, {1, -1}: 3,
	}
	keyQuads := make(map[rune]int)
	for k, p := range keyPos {
		if k == me {
			continue
		}
		dr := sign(p.r - start.r)
		dc := sign(p.c - start.c)
		keyQuads[k] = quadrants[pt{dr, dc}]
	}

	frontier = make(PriorityQueue[nState], 0)
	minDist = make(map[nState]int)
	sState = nState{strings.Repeat(string(me), len(quadrants)), ""}
	minDist[sState] = 0
	heap.Push(&frontier, &Item[nState]{value: sState, priority: 0})
	var p2AllKeys int
	for len(frontier) > 0 {
		tempCurr := heap.Pop(&frontier).(*Item[nState])
		if minDist[tempCurr.value] != -tempCurr.priority {
			continue
		}
		curr := tempCurr.value
		if len(curr.inv) == len(prereqs) {
			p2AllKeys = minDist[curr]
			break
		}

		// look ik like 99% of this is just copied from above
		// but trust me making it a function is probably going to be worse
		for newK, pr := range prereqs {
			if !curr.canTake(newK, pr) {
				continue
			}

			nextState := curr.addKey(newK)
			quad := keyQuads[newK]
			nextState.at = strSet(nextState.at, quad, newK)
			nextCost := minDist[curr] + keyDist[rune(curr.at[quad])][newK]
			if curr.at[quad] == me {
				nextCost -= 2
			}
			if alr, ok := minDist[nextState]; !ok || nextCost < alr {
				minDist[nextState] = nextCost
				nItem := Item[nState]{value: nextState, priority: -nextCost}
				heap.Push(&frontier, &nItem)
			}
		}
	}

	fmt.Printf("min # of steps for you: %v\n", p1AllKeys)
	fmt.Printf("min # of steps for the robots: %v\n", p2AllKeys)
}
