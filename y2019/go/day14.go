package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"regexp"
	"strings"
)

const p2OreAmt = 1000000000000

type ingredient struct {
	amt  int
	name string
}

func parseIngredient(s string) ingredient {
	ingFmt := regexp.MustCompile(`(\d+) ([A-Z]+)`)
	match := ingFmt.FindStringSubmatch(strings.TrimSpace(s))
	return ingredient{betterAtoi(match[1]), match[2]}
}

type recipe struct {
	needed []ingredient
	prod   int
}

func oreNeeded(fuel int, recipes map[string]recipe) int {
	have := make(map[string]int)
	ore := 0
	var process func(string, int)
	process = func(name string, amt int) {
		if name == "ORE" {
			ore += amt
			return
		}
		if have[name] >= amt {
			have[name] -= amt
			return
		}

		amt -= have[name]
		have[name] = 0
		r := recipes[name]
		prodNeeded := int(math.Ceil(float64(amt) / float64(r.prod)))
		for _, i := range r.needed {
			process(i.name, i.amt*prodNeeded)
		}
		have[name] += prodNeeded*r.prod - amt
	}
	process("FUEL", fuel)

	return ore
}

func day14() {
	file, err := os.Open("../input/day14.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	recipeFmt := regexp.MustCompile(`(.*) => (.*)`)
	recipes := make(map[string]recipe)
	for scanner.Scan() {
		raw := scanner.Text()
		match := recipeFmt.FindStringSubmatch(raw)
		var ingredients []ingredient
		for _, i := range strings.Split(match[1], ",") {
			ingredients = append(ingredients, parseIngredient(i))
		}
		result := parseIngredient(match[2])
		recipes[result.name] = recipe{ingredients, result.amt}
	}

	p1Ore := oreNeeded(1, recipes)

	fuelLower := 0
	fuelHigher := math.MaxInt32
	p2Fuel := 0
	for fuelLower <= fuelHigher {
		fuelMid := (fuelLower + fuelHigher) / 2
		oreReq := oreNeeded(fuelMid, recipes)
		if oreReq <= p2OreAmt {
			p2Fuel = fuelMid
			fuelLower = fuelMid + 1
		} else {
			fuelHigher = fuelMid - 1
		}
	}

	fmt.Printf("amt of ore for 1 fuel unit: %v\n", p1Ore)
	fmt.Printf("amt of fuel you can get w/ %v ore: %v\n", p2OreAmt, p2Fuel)
}
