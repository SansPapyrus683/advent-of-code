package main

import (
	"errors"
)

const (
	OP_ADD = 1 + iota
	OP_MUL
)
const OP_STOP = 99

type intcode struct {
	at int
	prog []int
}

func startIntcode(prog []int) intcode {
	cpyProg := make([]int, len(prog))
	copy(cpyProg, prog)
	return intcode{prog: cpyProg}
}

func (i *intcode) run() {
	i.at = 0
run:
	for i.at < len(i.prog) {
		op := i.prog[i.at]
		switch op {
		case OP_ADD: i.opArithmetic(op)
		case OP_MUL: i.opArithmetic(op)
		case OP_STOP: break run
		}
	}
}

func (i *intcode) opArithmetic(op int) error {
	ind1 := i.prog[i.at + 1]
	ind2 := i.prog[i.at + 2]
	store := i.prog[i.at + 3]
	var val int
	switch op {
	case OP_ADD: val = i.prog[ind1] + i.prog[ind2]
	case OP_MUL: val = i.prog[ind1] * i.prog[ind2]
	default: return errors.New("invalid operation")
	}
	i.prog[store] = val
	i.at += 4
	return nil
}
