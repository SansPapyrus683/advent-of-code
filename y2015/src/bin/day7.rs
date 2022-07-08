use std::fs;
use regex::Regex;
use std::collections::{HashMap, HashSet};

#[derive(Debug)]
enum Signal {
    Raw(String),
    And(String, String),
    Or(String, String),
    LShift(String, u8),
    RShift(String, u8),
    Not(String),
}

impl Signal {
    fn eval(&self, vars: &HashMap<String, i32>) -> i32 {
        match self {
            Signal::Raw(a) => get_val(a, vars).unwrap(),
            Signal::And(a1, a2) => get_val(a1, vars).unwrap() & get_val(a2, vars).unwrap(),
            Signal::Or(a1, a2) => get_val(a1, vars).unwrap() | get_val(a2, vars).unwrap(),
            Signal::LShift(a, v) => get_val(a, vars).unwrap() << v,
            Signal::RShift(a, v) => get_val(a, vars).unwrap() >> v,
            Signal::Not(a) => !get_val(a, vars).unwrap()
        }
    }
}

fn get_val(v: &str, vars: &HashMap<String, i32>) -> Option<i32> {
    match v.parse::<i32>() {
        Ok(val) => Some(val),
        _ => if vars.contains_key(v) { Some(vars[v]) } else { None }
    }
}

fn eval_circuit(wires: &HashMap<String, Signal>) -> HashMap<String, i32> {
    let mut res = HashMap::new();
    let mut remaining = HashSet::new();
    for (w, _) in wires {
        remaining.insert(w);
    }
    while res.len() < wires.len() {
        let mut to_remove: HashSet<&String> = HashSet::new();
        for r in &remaining {
            let valid = match &wires[*r] {
                Signal::Raw(a) => get_val(a, &res).is_some(),
                Signal::And(a1, a2) => get_val(a1, &res).is_some()
                    && get_val(a2, &res).is_some(),
                Signal::Or(a1, a2) => get_val(a1, &res).is_some()
                    && get_val(a2, &res).is_some(),
                Signal::LShift(a, _) => get_val(a, &res).is_some(),
                Signal::RShift(a, _) => get_val(a, &res).is_some(),
                Signal::Not(a) => get_val(a, &res).is_some()
            };
            if valid {
                to_remove.insert(*r);
                res.insert((*r).to_string(), wires[*r].eval(&res));
            }
        }
        for r in &to_remove {
            remaining.remove(r);
        }
    }
    res
}

fn main() {
    // regex sauce: https://github.com/alokmenghrajani/adventofcode/blob/master/src/year_2015/day07.rs
    let raw_fmt = Regex::new(r"^(\w+) -> (\D+)$").unwrap();
    let and_fmt = Regex::new(r"^(\w+) AND (\w+) -> (\D+)$").unwrap();
    let or_fmt = Regex::new(r"^(\w+) OR (\w+) -> (\D+)$").unwrap();
    let ls_fmt = Regex::new(r"^(\w+) LSHIFT (\d+) -> (\D+)$").unwrap();
    let rs_fmt = Regex::new(r"^(\w+) RSHIFT (\d+) -> (\D+)$").unwrap();
    let not_fmt = Regex::new(r"^NOT (\w+) -> (\D+)$").unwrap();

    let read = fs::read_to_string("input/day7.txt").expect("you done messed up");
    let mut wires: HashMap<String, Signal> = HashMap::new();
    for i in read.lines() {
        if let Some(m) = raw_fmt.captures(i) {
            wires.insert(m[2].to_string(), Signal::Raw(m[1].to_string()));
        } else if let Some(m) = and_fmt.captures(i) {
            wires.insert(m[3].to_string(), Signal::And(m[1].to_string(), m[2].to_string()));
        } else if let Some(m) = or_fmt.captures(i) {
            wires.insert(m[3].to_string(), Signal::Or(m[1].to_string(), m[2].to_string()));
        } else if let Some(m) = ls_fmt.captures(i) {
            wires.insert(m[3].to_string(), Signal::LShift(m[1].to_string(), m[2].parse().unwrap()));
        } else if let Some(m) = rs_fmt.captures(i) {
            wires.insert(m[3].to_string(), Signal::RShift(m[1].to_string(), m[2].parse().unwrap()));
        } else if let Some(m) = not_fmt.captures(i) {
            wires.insert(m[2].to_string(), Signal::Not(m[1].to_string()));
        }
    }

    let wire_a = eval_circuit(&wires)["a"];
    println!("init value of wire a: {}", wire_a);
    wires.insert("b".to_string(), Signal::Raw(wire_a.to_string()));
    let wire_a = eval_circuit(&wires)["a"];
    println!("new value of wire a: {}", wire_a);
}
