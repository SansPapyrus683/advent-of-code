use std::collections::HashSet;
use std::fs;
use regex::Regex;

const P2_ROUNDS: u32 = 1e9 as u32;

enum Move {
    Spin(usize),
    Exchange(usize, usize),
    Swap(char, char)
}

impl Move {
    fn exec(&self, progs: &mut Vec<char>) {
        match self {
            Move::Spin(x) => progs.rotate_right(*x),
            Move::Exchange(a, b) => progs.swap(*a, *b),
            Move::Swap(a, b) => {
                let a = progs.iter().position(|p| p == a).unwrap();
                let b = progs.iter().position(|p| p == b).unwrap();
                progs.swap(a, b);
            }
        }
    }
}

fn main() {
    let read = fs::read_to_string("input/day16.txt")
        .expect("bruh");
    let read: Vec<&str> = read.split(',').collect();

    let spin_fmt = Regex::new(r"s(\d+)").unwrap();
    let exc_fmt = Regex::new(r"x(\d+)/(\d+)").unwrap();
    let swap_fmt = Regex::new("p([a-z])/([a-z])").unwrap();

    let mut moves = Vec::new();
    for d in read {
        if let Some(m) = spin_fmt.captures(d) {
            moves.push(Move::Spin(m[1].parse().unwrap()));
        } else if let Some(m) = exc_fmt.captures(d) {
            moves.push(Move::Exchange(
                m[1].parse().unwrap(), m[2].parse().unwrap()
            ));
        } else if let Some(m) = swap_fmt.captures(d) {
            // have you seen anything stupider
            moves.push(Move::Swap(
                m[1].chars().nth(0).unwrap(), m[2].chars().nth(0).unwrap()
            ));
        }
    }

    let initial: Vec<char> = ('a'..='p').collect();
    let mut progs = initial.clone();
    for m in &moves {
        m.exec(&mut progs);
    }
    let p1_final = progs.iter()
        .fold(String::new(), |acc, &c| format!("{}{}", acc, c));
    println!("state after 1 dance: {p1_final}");

    let mut progs = initial.clone();
    let mut prog_hist = HashSet::new();
    let mut prog_order = Vec::new();
    while prog_hist.insert(progs.clone()) {
        prog_order.push(progs.clone());
        for m in &moves {
            m.exec(&mut progs);
        }
    }

    let p2_final = prog_order[(P2_ROUNDS as usize) % prog_hist.len()].iter()
        .fold(String::new(), |acc, &c| format!("{}{}", acc, c));
    println!("state after {P2_ROUNDS} dances: {p2_final}");
}
