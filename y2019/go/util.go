package main

// honestly going by array row and column is usually easier than x & y so...
type pt struct {
	r int
	c int
}

func (a pt) addPt(b pt) pt {
	return pt{a.r + b.r, a.c + b.c}
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
	return gcd(b, a % b)
}
