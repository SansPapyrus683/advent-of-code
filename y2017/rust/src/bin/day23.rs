use std::fs;
use std::collections::HashMap;

//copied right fromm day 23
fn parse_val(v: &String, reg: &HashMap<String, i64>) -> i64 {
    let val = v.parse::<i64>();
    match val {
        Ok(i) => i,
        Err(_) => *reg.get(v).unwrap_or(&0)
    }
}

#[derive(Eq, PartialEq)]
enum Op {
    Set(String, String),
    Sub(String, String),
    Mul(String, String),
    Jnz(String, String)
}

impl Op {
    /// errors like a true manly function if something goes wrong
    fn from_str(s: &str) -> Self {
        let split: Vec<&str> = s.split(' ').collect();
        let reg = split[1].to_string();
        let val = split.get(2).map(|s| s.to_string());
        let op = match split[0].to_lowercase().as_str() {
            "set" => Self::Set,
            "sub" => Self::Sub,
            "mul" => Self::Mul,
            "jnz" => Self::Jnz,
            _ => unreachable!("hell yeah")
        }(reg, val.unwrap());
        op
    }
}

fn is_prime(n: i32) -> bool {
    if n <= 1 {
        return false;
    }
    (2..n).all(|a| n % a != 0)
}

fn main() {
    let read = fs::read_to_string("../input/day23.txt").expect("bruh");
    let mut ops = Vec::new();
    for i in read.lines() {
        ops.push(Op::from_str(i));
    }

    let mut at = 0;
    let mut mul_called = 0;
    let mut reg = HashMap::new();
    while 0 <= at && at < ops.len() as i64 {
        match &ops[at as usize] {
            Op::Set(x, y) => { reg.insert(x.to_string(), parse_val(y, &reg)); },
            Op::Sub(x, y) => {
                *reg.entry(x.to_string()).or_default() -= parse_val(y, &reg);
            }
            Op::Mul(x, y) => {
                mul_called += 1;
                *reg.entry(x.to_string()).or_default() *= parse_val(y, &reg);
            }
            Op::Jnz(x, y) => {
                if parse_val(x, &reg) != 0 {
                    at += parse_val(y, &reg);
                    at -= 1;
                }
            }
        };
        at += 1;
    }
    println!("the mul op was called {mul_called} times");

    // sauce: https://todd.ginsberg.com/post/advent-of-code/2017/day23/#d23p2
    // from first line of input file
    let mut b = read.split_whitespace().collect::<Vec<&str>>()[2].parse().unwrap();
    b = b * 100 + 100000;
    let mut not_prime = 0;
    for _ in 0..=1000 {
        not_prime += if !is_prime(b) { 1 } else { 0 };
        b += 17;
    }
    println!("answer to part 2: {not_prime}");
}
