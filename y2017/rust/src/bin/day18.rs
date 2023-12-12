use std::fs;
use std::collections::{HashMap, VecDeque};

fn parse_val(v: &String, reg: &HashMap<String, i64>) -> i64 {
    let val = v.parse::<i64>();
    match val {
        Ok(i) => i,
        Err(_) => *reg.get(v).unwrap_or(&0)
    }
}

#[derive(Eq, PartialEq)]
enum Op {
    Snd(String),
    Set(String, String),
    Add(String, String),
    Mul(String, String),
    Mod(String, String),
    Rcv(String),
    Jgz(String, String),
}

impl Op {
    /// errors like a true manly function if something goes wrong
    fn from_str(s: &str) -> Self {
        let split: Vec<&str> = s.split(' ').collect();
        let reg = split[1].to_string();
        let val = split.get(2).map(|s| s.to_string());
        match split[0].to_lowercase().as_str() {
            "snd" => Self::Snd(reg),
            "set" => Self::Set(reg, val.unwrap()),
            "add" => Self::Add(reg, val.unwrap()),
            "mul" => Self::Mul(reg, val.unwrap()),
            "mod" => Self::Mod(reg, val.unwrap()),
            "rcv" => Self::Rcv(reg),
            "jgz" => Self::Jgz(reg, val.unwrap()),
            _ => unreachable!("hell yeah")
        }
    }
}

fn main() {
    let read = fs::read_to_string("../input/day18.txt").expect("bruh");

    let mut ops = Vec::new();
    for i in read.lines() {
        ops.push(Op::from_str(i));
    }

    let mut at = 0;
    let mut sound = None;
    let mut reg = HashMap::new();
    while 0 <= at && at < ops.len() as i64 {
        match &ops[at as usize] {
            Op::Snd(x) => sound = Some(parse_val(x, &reg)),
            Op::Set(x, y) => { reg.insert(x.to_string(), parse_val(y, &reg)); },
            Op::Add(x, y) => {
                *reg.entry(x.to_string()).or_default() += parse_val(y, &reg);
            },
            Op::Mul(x, y) => {
                *reg.entry(x.to_string()).or_default() *= parse_val(y, &reg);
            },
            Op::Mod(x, y) => {
                *reg.entry(x.to_string()).or_default() %= parse_val(y, &reg);
            },
            Op::Rcv(x) => {
                if parse_val(x, &reg) != 0 {
                    println!("first recalled sound: {}", sound.unwrap());
                    break;
                }
            }
            Op::Jgz(x, y) => {
                if parse_val(x, &reg) > 0 {
                    at += parse_val(y, &reg);
                    at -= 1;
                }
            },
        };
        at += 1;
    }

    let mut at = vec![0; 2];
    let mut queues = vec![VecDeque::new(); 2];
    let mut regs = vec![HashMap::new(); 2];
    for (i, r) in regs.iter_mut().enumerate() {
        r.insert("p".to_string(), i as i64);
    }

    let mut prog1sent = 0;
    while at.iter().any(|&i| 0 <= i && i < ops.len() as i64) {
        let mut waiting = vec![false; 2];
        for i in 0..2 {
            let other = if i == 0 { 1 } else { 0 };
            let reg = regs.get_mut(i).unwrap();
            match &ops[at[i] as usize] {
                Op::Snd(x) => {
                    prog1sent += if i == 1 { 1 } else { 0 };
                    queues[other].push_back(parse_val(x, reg))
                },
                Op::Set(x, y) => {
                    reg.insert(x.to_string(), parse_val(y, reg));
                },
                Op::Add(x, y) => {
                    *reg.entry(x.to_string()).or_default() += parse_val(y, reg)
                },
                Op::Mul(x, y) => {
                    *reg.entry(x.to_string()).or_default() *= parse_val(y, reg)
                },
                Op::Mod(x, y) => {
                    *reg.entry(x.to_string()).or_default() %= parse_val(y, reg)
                },
                Op::Rcv(x) => {
                    if !queues[i].is_empty() {
                        reg.insert(x.to_string(), queues[i].pop_front().unwrap());
                    } else {
                        waiting[i] = true;
                        at[i] -= 1;
                    }
                }
                Op::Jgz(x, y) => {
                    if parse_val(x, reg) > 0 {
                        at[i] += parse_val(y, reg);
                        at[i] -= 1;
                    }
                }
            };
            at[i] += 1;
        }
        if waiting.iter().all(|&i| i) {
            break;
        }
    }

    println!("# of times program 1 sent a value: {prog1sent}");
}
