package main

import (
	"bufio"
	"errors"
	"fmt"
	"log"
	"os"
	"regexp"
)

const p1StepNum = 1000

type moon struct {
	x    int
	y    int
	z    int
	velX int
	velY int
	velZ int
}

func (m moon) getAxis(axis rune) (int, int, error) {
	switch axis {
	case 'x':
		return m.x, m.velX, nil
	case 'y':
		return m.y, m.velY, nil
	case 'z':
		return m.z, m.velZ, nil
	default:
		return 0, 0, errors.New(fmt.Sprintf("invalid axis %c", axis))
	}
}

func simDim(moons []moon, axis rune) error {
	type moonDim struct {
		pos *int
		vel *int
	}
	var moonDims []moonDim
	for i := range moons {
		moon := &moons[i]
		var dim moonDim
		// can't use getDim bc i need the pointers :sob:
		switch axis {
		case 'x':
			dim = moonDim{&moon.x, &moon.velX}
		case 'y':
			dim = moonDim{&moon.y, &moon.velY}
		case 'z':
			dim = moonDim{&moon.z, &moon.velZ}
		default:
			return errors.New(fmt.Sprintf("invalid axis %c", axis))
		}
		moonDims = append(moonDims, dim)
	}

	for i, m1 := range moonDims {
		for j, m2 := range moonDims {
			if j <= i {
				continue
			}
			if *m1.pos < *m2.pos {
				(*m1.vel)++
				(*m2.vel)--
			} else if *m1.pos > *m2.pos {
				(*m1.vel)--
				(*m2.vel)++
			}
		}
	}
	for _, m := range moonDims {
		(*m.pos) += *m.vel
	}

	return nil
}

func day12() {
	file, err := os.Open("../input/day12.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	var moons []moon
	planetFmt := regexp.MustCompile(`<x=(-?\d+), y=(-?\d+), z=(-?\d+)>`)
	for scanner.Scan() {
		planet := scanner.Text()
		match := planetFmt.FindStringSubmatch(planet)
		moons = append(moons, moon{
			betterAtoi(match[1]),
			betterAtoi(match[2]),
			betterAtoi(match[3]), 0, 0, 0, // screw you, go.
		})
	}

	p1Moons := make([]moon, len(moons))
	copy(p1Moons, moons)
	for i := 0; i < p1StepNum; i++ {
		for _, dim := range "xyz" {
			simDim(p1Moons, dim)
		}
	}

	p1Energy := 0
	for _, m := range p1Moons {
		pe := abs(m.x) + abs(m.y) + abs(m.z)
		ke := abs(m.velX) + abs(m.velY) + abs(m.velZ)
		p1Energy += pe * ke
	}

	p2Moons := make([]moon, len(moons))
	copy(p2Moons, moons)
	var axesRepeat []int
	for _, dim := range "xyz" {
		var start []pt // yeah i'm using my point class as a pair class, sue me
		for _, m := range p2Moons {
			pos, vel, _ := m.getAxis(dim)
			start = append(start, pt{pos, vel})
		}

		steps := 1
		for ; ; steps++ {
			simDim(p2Moons, dim)
			isStart := true
			for i, p := range start {
				pos, vel, _ := p2Moons[i].getAxis(dim)
				if pos != p.r || vel != p.c {
					isStart = false
					// break
				}
			}
			if isStart {
				break
			}
		}

		axesRepeat = append(axesRepeat, steps)
	}

	tilLoop := 1
	for _, r := range axesRepeat {
		tilLoop = tilLoop * r / gcd(tilLoop, r)
	}

	fmt.Printf("kinetic energy after %v steps: %v\n", p1StepNum, p1Energy)
	fmt.Printf("%v steps until we loop back\n", tilLoop)
}
