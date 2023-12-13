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
	}
}
