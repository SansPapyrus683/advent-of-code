package main

import (
	"fmt"
	"strconv"
)

const pwLower = 273025
const pwUpper = 767253

func nonDec(pw int) bool {
	strPw := strconv.Itoa(pw)
	for i := 0; i < len(strPw)-1; i++ {
		if strPw[i] > strPw[i+1] {
			return false
		}
	}
	return true
}

func isValidP1(pw int) bool {
	if !nonDec(pw) {
		return false
	}
	strPw := strconv.Itoa(pw)
	for i := 0; i < len(strPw)-1; i++ {
		if strPw[i] == strPw[i+1] {
			return true
		}
	}
	return false
}

func isValidP2(pw int) bool {
	if !nonDec(pw) {
		return false
	}
	strPw := strconv.Itoa(pw)
	for i := 0; i < len(strPw)-1; i++ {
		if strPw[i] == strPw[i+1] {
			before := i == 0 || strPw[i] != strPw[i-1]
			after := i == len(strPw)-2 || strPw[i] != strPw[i+2]
			if before && after {
				return true
			}
		}
	}
	return false
}

func day4() {
	validNum1, validNum2 := 0, 0
	for pw := pwLower; pw <= pwUpper; pw++ {
		if isValidP1(pw) {
			validNum1++
		}
		if isValidP2(pw) {
			validNum2++
		}
	}

	fmt.Printf("# of valid pws (p1): %v\n", validNum1)
	fmt.Printf("# of valid pws (p2): %v\n", validNum2)
}
