use std::fs;
use std::collections::HashMap;
use regex::Regex;

enum Condition {
    Gt, Lt,
    Geq, Leq,
    Neq, EQ
}

impl Condition {
    fn from_str(s: &str) -> Option<Self> {
        match s {
            ">" => Some(Self::Gt),
            "<" => Some(Self::Lt),
            ">=" => Some(Self::Geq),
            "<=" => Some(Self::Leq),
            "!=" => Some(Self::Neq),
            "==" => Some(Self::EQ),
            _ => None
        }
    }

    fn eval(&self, i1: i32, i2: i32) -> bool {
        match self {
            Self::Gt => i1 > i2,
            Self::Lt => i1 < i2,
            Self::Geq => i1 >= i2,
            Self::Leq => i1 <= i2,
            Self::Neq => i1 != i2,
            Self::EQ => i1 == i2
        }
    }
}

enum Op { Inc(i32), Dec(i32) }
impl Op {
    fn from_str(s: &str) -> Option<fn(i32) -> Op> {
        match s {
            "inc" => Some(Self::Inc),
            "dec" => Some(Self::Dec),
            _ => None
        }
    }
}

struct Instruction { reg: String, op: Op, l: String, cond: Condition, r: i32 }

fn main() {
    let raw_prog = fs::read_to_string("input/day8.txt").expect("bruh");

    let inc_fmt = Regex::new(
        r"([a-z]+) (inc|dec) (-?\d+) if ([a-z]+) (>=|<=|>|<|!=|==) (-?\d+)"
    ).unwrap();

    let mut prog = Vec::new();
    for i in raw_prog.lines() {
        if let Some(m) = inc_fmt.captures(i) {
            prog.push(Instruction {
                reg: m[1].to_string(),
                op: Op::from_str(&m[2]).unwrap()(m[3].parse().unwrap()),
                l: m[4].to_string(),
                cond: Condition::from_str(&m[5]).unwrap(),
                r: m[6].parse().unwrap()
            });
        }
    }

    let mut regs: HashMap<String, i32> = HashMap::new();
    let mut highest = 0;
    for i in &prog {
        let cond_val = *regs.get(&i.l).unwrap_or(&0);
        if i.cond.eval(cond_val, i.r) {
            let reg = i.reg.to_string();
            *regs.entry(reg).or_default() += match i.op {
                Op::Inc(v) => v,
                Op::Dec(v) => -v
            };
            highest = highest.max(regs[&i.reg]);
        }
    }

    println!("highest at the end: {}", regs.values().max().unwrap());
    println!("highest of all time: {highest}");
}
