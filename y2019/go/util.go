package main

import (
	"strconv"
)

func betterAtoi(s string) int {
	ret, _ := strconv.Atoi(s) // JUST THROW AN ERROR FOR CHRIST'S SAKE, GO!
	return ret
}

// honestly going by array row and column is usually easier than x & y so...
type pt struct {
	r int
	c int
}

func (a pt) add(b pt) pt {
	return pt{a.r + b.r, a.c + b.c}
}

func (a pt) neighbors4Raw() []pt {
	var ret []pt
	for _, delta := range []pt{{0, -1}, {0, 1}, {1, 0}, {-1, 0}} {
		ret = append(ret, a.add(delta))
	}
	return ret
}

func (a pt) neighbors4(rMax, cMax int) []pt {
	var ret []pt
	for _, n := range a.neighbors4Raw() {
		if n.inGrid(rMax, cMax) {
			ret = append(ret, n)
		}
	}
	return ret
}

func (a pt) inGrid(rMax, cMax int) bool {
	return 0 <= a.r && a.r < rMax && 0 <= a.c && a.c < cMax
}

func abs(n int) int {
	if n < 0 {
		return -n
	}
	return n
}

func sign(n int) int {
	switch {
	case n < 0:
		return -1
	case n == 0:
		return 0
	case n > 0:
		return 1
	}
	panic("what the hell did you do")
}

func gcd(a, b int) int {
	if b == 0 {
		return a
	}
	return gcd(b, a%b)
}
