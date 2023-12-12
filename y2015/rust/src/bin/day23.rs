use std::fs;
use std::collections::HashMap;
use regex::Regex;

enum Op {
    Hlf(char), Tpl(char), Inc(char),
    Jmp(i32),
    Jie(char, i32), Jio(char, i32)
}

fn exec(reg: &HashMap<char, i32>, ops: &Vec<Op>) -> HashMap<char, i32> {
    let mut ret = reg.clone();
    let mut at = 0;
    while 0 <= at && at < ops.len() as i32 {
        match ops[at as usize] {
            Op::Hlf(r) => *ret.entry(r).or_insert(0) /= 2,
            Op::Tpl(r) => *ret.entry(r).or_insert(0) *= 3,
            Op::Inc(r) => *ret.entry(r).or_insert(0) += 1,
            // the -1 is because i add 1 to at at the end of the loop
            Op::Jmp(o) => at += o - 1,
            Op::Jie(r, o) => if *ret.entry(r).or_insert(0) % 2 == 0 {
                at += o - 1
            }
            Op::Jio(r, o) => if *ret.entry(r).or_insert(0) == 1 {
                at += o - 1
            }
        }
        at += 1;
    }
    ret
}

fn main() {
    // bruh
    let hlf_fmt = Regex::new("hlf ([a-z])").unwrap();
    let tpl_fmt = Regex::new("tpl ([a-z])").unwrap();
    let inc_fmt = Regex::new("inc ([a-z])").unwrap();
    let jmp_fmt = Regex::new(r"jmp ([+\-\d]+)").unwrap();
    let jie_fmt = Regex::new(r"jie ([a-z]), ([+\-\d]+)").unwrap();
    let jio_fmt = Regex::new(r"jio ([a-z]), ([+\-\d]+)").unwrap();

    let read = fs::read_to_string("../input/day23.txt").expect("bruh");
    let mut ops = Vec::new();
    for i in read.lines() {
        if let Some(m) = hlf_fmt.captures(i) {
            ops.push(Op::Hlf(m[1].chars().next().unwrap()));
        } else if let Some(m) = tpl_fmt.captures(i) {
            ops.push(Op::Tpl(m[1].chars().next().unwrap()));
        } else if let Some(m) = inc_fmt.captures(i) {
            ops.push(Op::Inc(m[1].chars().next().unwrap()));
        } else if let Some(m) = jmp_fmt.captures(i) {
            ops.push(Op::Jmp(m[1].parse().unwrap()));
        } else if let Some(m) = jie_fmt.captures(i) {
            ops.push(Op::Jie(m[1].chars().next().unwrap(), m[2].parse().unwrap()));
        } else if let Some(m) = jio_fmt.captures(i) {
            ops.push(Op::Jio(m[1].chars().next().unwrap(), m[2].parse().unwrap()));
        }
    }

    println!("b val (p1): {}", exec(&HashMap::new(), &ops)[&'b']);
    println!("b val (p2): {}", exec(&HashMap::from([('a', 1)]), &ops)[&'b']);
}
