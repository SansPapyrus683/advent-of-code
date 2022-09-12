use std::collections::HashMap;
use std::fs;
use regex::Regex;
use ndarray::prelude::*;
use ndarray::Array2;

const SEP: char = '/';
const START: &str = ".#./..#/###";
const P1_STEPS: u32 = 5;
const P2_STEPS: u32 = 18;

fn parse_img(s: &str) -> Array2<char> {
    let mut col_num = 0;
    let mut row_num = 0;
    let mut vec = Vec::new();
    for r in s.split(SEP) {
        vec.extend(r.chars());
        col_num = r.len();
        row_num += 1;
    }
    Array2::from_shape_vec((row_num, col_num), vec).unwrap()
}

pub fn vflip<T: Clone>(img: &Array2<T>) -> Array2<T> {
    img.slice(s![..;-1, ..]).to_owned()
}

pub fn combs<T: Clone>(img: &Array2<T>) -> Vec<Array2<T>> {
    let mut combs = vec![img.to_owned()];
    combs.push(vflip(&combs[0]));
    let mut curr = (combs[0].clone(), combs[1].clone());
    for _ in 0..3 {
        // apparently this can give you a rotation
        combs.push(vflip(&curr.0.clone().reversed_axes()));
        combs.push(vflip(&curr.1.clone().reversed_axes()));
        curr = (combs[combs.len() - 2].clone(), combs[combs.len() - 1].clone());
    }
    combs
}

fn main() {
    let read = fs::read_to_string("input/day21.txt").expect("bruh");
    let rule_fmt = Regex::new(&*format!("([.#{SEP}]+) => ([.#{SEP}]+)")).unwrap();

    let mut rules = HashMap::new();
    for r in read.lines() {
        if let Some(m) = rule_fmt.captures(r) {
            let from = parse_img(&m[1]);
            let to = parse_img(&m[2]);
            match from.shape() {
                [2, 2] => assert_eq!(to.shape(), [3, 3]),
                [3, 3] => assert_eq!(to.shape(), [4, 4]),
                _ => panic!("invalid array dimensions for rule")
            }

            for c in combs(&from) {
                rules.insert(c, to.clone());
            }
        }
    }

    let mut img = parse_img(START);
    let mut side = img.shape()[0];
    assert_eq!(side, img.shape()[1]);
    for i in 0..P1_STEPS.max(P2_STEPS) {
        let (new_side, step) = if side % 2 == 0 {
            (side / 2 * 3, (2, 3))
        } else {  (side / 3 * 4, (3, 4)) };

        let mut new = Array2::from_shape_vec(
            (new_side, new_side), vec!['a'; new_side * new_side]
        ).unwrap();
        for r in (0..side).step_by(step.0) {
            for c in (0..side).step_by(step.0) {
                let curr = img.slice(s![r..r + step.0, c..c + step.0]);
                let next = &rules[&curr.to_owned()];
                let nrc = (r / step.0 * step.1, c / step.0 * step.1);
                new.slice_mut(
                    s![nrc.0..nrc.0 + step.1, nrc.1..nrc.1 + step.1]
                ).assign(next);
            }
        }
        img = new;
        side = new_side;

        if i == P1_STEPS - 1 || i == P2_STEPS - 1 {
            let on = img.iter().map(|&c| if c == '#' { 1 } else { 0 }).sum::<i32>();
            if i == P1_STEPS - 1 {
                println!("# on after {P1_STEPS} (p1): {on}");
            }
            if i == P2_STEPS - 1 {
                println!("# on after {P2_STEPS} (p2): {on}");
            }
        }
    }
}
