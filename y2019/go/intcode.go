package main

import (
	"errors"
	"fmt"
	"strconv"
)

const (
	OP_ADD = 1 + iota
	OP_MUL
	OP_INPUT
	OP_OUTPUT
	OP_JIT  // jump if true
	OP_JIF  // jump if false
	OP_LT
	OP_EQ
)
const OP_STOP = 99

type intcode struct {
	at   int
	prog []int
}

func startIntcode(prog []int) intcode {
	cpyProg := make([]int, len(prog))
	copy(cpyProg, prog)
	return intcode{prog: cpyProg}
}

// who knows if this function is bad practice or not
func opId(op int) int {
	return op % 100
}

func (i *intcode) run() {
	i.at = 0
run:
	for i.at < len(i.prog) {
		op := i.prog[i.at]
		switch opId(op) {
		case OP_ADD, OP_MUL, OP_LT, OP_EQ:
			i.opArithmetic()
		case OP_INPUT, OP_OUTPUT:
			i.opIO()
		case OP_JIT, OP_JIF:
			i.opBranch()
		case OP_STOP:
			break run
		default:
			panic(fmt.Sprintf("wtf is opcode %v", op))
		}
	}
}

// true for pos, false for imm; positions start from 0
func isPos(op int, pos int) bool {
	strOp := strconv.Itoa(op)
	for i := 2; i < len(strOp); i++ {
		if i-2 == pos {
			return strOp[len(strOp)-i-1] == '0'
		}
	}
	return true
}

func (i *intcode) getParamAt(pos int) int {
	ret := i.prog[i.at + pos + 1]
	if isPos(i.prog[i.at], pos) {
		return i.prog[ret]
	}
	return ret
}

func (i *intcode) opArithmetic() error {
	param1, param2 := i.getParamAt(0), i.getParamAt(1)
	storeAt := i.prog[i.at+3]

	var val int
	switch opId(i.prog[i.at]) {
	case OP_ADD:
		val = param1 + param2
	case OP_MUL:
		val = param1 * param2
	case OP_LT:
		if param1 < param2 {
			val = 1
		}
	case OP_EQ:
		if param1 == param2 {
			val = 1
		}
	default:
		return errors.New("invalid operation")
	}

	i.prog[storeAt] = val
	i.at += 4
	return nil
}

func (i *intcode) opIO() error {
	switch opId(i.prog[i.at]) {
	case OP_INPUT:
		var input int
		fmt.Scanf("%d", &input)
		i.prog[i.prog[i.at + 1]] = input
	case OP_OUTPUT:
		fmt.Println(i.getParamAt(0))
	default:
		return errors.New("invalid operation")
	}
	
	i.at += 2
	return nil
}

func (i *intcode) opBranch() error {
	param1, param2 := i.getParamAt(0), i.getParamAt(1)

	switch opId(i.prog[i.at]) {
	case OP_JIT:
		if param1 != 0 {
			i.at = param2
			i.at += 3
		}
	case OP_JIF:
		if param1 == 0 {
			i.at = param2
		} else {
			i.at += 3
		}
	default:
		return errors.New("invalid operation")
	}
	return nil
}
