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
	OP_JIT // jump if true
	OP_JIF // jump if false
	OP_LT
	OP_EQ
	OP_RB
)
const OP_STOP = 99

type intcode struct {
	at       int
	prog     []int
	relBase  int
	finished bool

	// 0 = integer io, 1 = give/get an array, 2 = ascii
	ioMode     int
	inputQueue []int
	output     []int
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
	if i.finished {
		return
	}
run:
	for i.at < len(i.prog) {
		op := i.prog[i.at]
		switch opId(op) {
		case OP_ADD, OP_MUL, OP_LT, OP_EQ:
			i.opArithmetic()
		case OP_INPUT, OP_OUTPUT:
			wait, _ := i.opIO()
			if wait {
				return
			}
		case OP_JIT, OP_JIF:
			i.opBranch()
		case OP_RB:
			i.opRelBase()
		case OP_STOP:
			break run
		default:
			panic(fmt.Sprintf("wtf is opcode %v", op))
		}
	}
	i.finished = true
}

// true for pos, false for imm; positions start from 0
func paramMode(op int, pos int) int {
	strOp := strconv.Itoa(op)
	for i := 2; i < len(strOp); i++ {
		if i-2 == pos {
			return int(strOp[len(strOp)-i-1] - '0')
		}
	}
	return 0
}

func (i *intcode) readMem(at int) int {
	for len(i.prog) <= at {
		i.prog = append(i.prog, 0)
	}
	return i.prog[at]
}

func (i *intcode) writeMem(at int, val int) {
	for len(i.prog) <= at {
		i.prog = append(i.prog, 0)
	}
	i.prog[at] = val
}

func (i *intcode) getMemLoc(pos int) int {
	ret := i.readMem(i.at + pos + 1)
	switch paramMode(i.prog[i.at], pos) {
	case 0:
		return ret
	case 2:
		return ret + i.relBase
	}
	return -1 // too lazy to do error handling here
}

func (i *intcode) getParamAt(pos int) int {
	ret := i.readMem(i.at + pos + 1)
	switch paramMode(i.prog[i.at], pos) {
	case 0:
		return i.readMem(ret)
	case 1:
		return ret
	case 2:
		return i.readMem(ret + i.relBase)
	}
	return -1
}

func (i *intcode) opArithmetic() error {
	param1, param2 := i.getParamAt(0), i.getParamAt(1)
	storeAt := i.getMemLoc(2)

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

	i.writeMem(storeAt, val)
	i.at += 4
	return nil
}

func (i *intcode) opIO() (bool, error) {
	switch opId(i.prog[i.at]) {
	case OP_INPUT:
		var input int

		switch i.ioMode {
		case 0:
			fmt.Scanf("%d", &input)
		case 1:
			if len(i.inputQueue) == 0 {
				return true, nil
			}
			input, i.inputQueue = i.inputQueue[0], i.inputQueue[1:]
		default:
			return false, errors.New("invalid io mode!")
		}

		i.writeMem(i.getMemLoc(0), input)
	case OP_OUTPUT:
		output := i.getParamAt(0)

		switch i.ioMode {
		case 0:
			fmt.Println(output)
		case 1:
			i.output = append(i.output, output)
		default:
			return false, errors.New("invalid io mode")
		}
	default:
		return false, errors.New("invalid operation")
	}

	i.at += 2
	return false, nil
}

func (i *intcode) opBranch() error {
	param1, param2 := i.getParamAt(0), i.getParamAt(1)

	switch opId(i.prog[i.at]) {
	case OP_JIT:
		if param1 != 0 {
			i.at = param2
		} else {
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

func (i *intcode) opRelBase() error {
	param1 := i.getParamAt(0)

	switch opId(i.prog[i.at]) {
	case OP_RB:
		i.relBase += param1
	default:
		return errors.New("invalid operation")
	}

	i.at += 2
	return nil
}
