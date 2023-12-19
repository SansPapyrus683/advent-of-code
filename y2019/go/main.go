package main

import "fmt"

// ok bc golang is stupid it can't have multiple mains...
func main() {
	var day int
	fmt.Scanf("%d", &day)

	switch day {
	case 1:
		day1()
	case 2:
		day2()
	case 3:
		day3()
	case 4:
		day4()
	case 5:
		day5()
	case 6:
		day6()
	case 7:
		day7()
	case 8:
		day8()
	case 9:
		day9()
	case 10:
		day10()
	case 11:
		day11()
	case 12:
		day12()
	case 13:
		day13()
	case 14:
		day14()
	case 15:
		day15()
	case 16:
		day16()
	case 17:
		day17()
	case 18:
		day18()
	case 19:
		day19()
	case 20:
		day20()
	case 23:
		day23()
	case 24:
		day24p1()
		day24p2()
	case 21, 25:
		typingIntcode(day)
	default:
		fmt.Println("invalid day (or my lazy bum hasn't done it yet)")
		fmt.Println("if you're looking for day 22, it's in python lol")
	}
}
