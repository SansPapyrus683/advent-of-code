use aoc_rust_2018::assembly::Op;
use regex::Regex;
use std::fs;

const P2_RUN_AMT: u32 = 100;

fn main() {
    // YOU'RE ADOPTED, RUST.
    let read = fs::read_to_string("../input/day19.txt").unwrap();
    let mut lines = read.lines();
    let ip_fmt = Regex::new("#ip ([0-5])").unwrap();
    let instruct_fmt = Regex::new(r"([a-zA-Z]+) (\d+) (\d+) (\d+)").unwrap();
    let ip = ip_fmt.captures(lines.next().unwrap()).unwrap()[1].parse::<usize>().unwrap();
    let mut instructions = Vec::new();
    for i in lines {
        if let Some(m) = instruct_fmt.captures(i) {
            instructions.push((
                Op::from_str(&m[1]).unwrap(),
                m[2].parse::<i32>().unwrap(),
                m[3].parse::<i32>().unwrap(),
                m[4].parse::<i32>().unwrap(),
            ));
        }
    }

    let mut ip_val: i32 = 0;
    let mut registers = vec![0; 6];
    while 0 <= ip_val && ip_val < instructions.len() as i32 {
        let (op, a, b, c) = instructions[ip_val as usize];
        registers[ip] = ip_val;
        registers = op.apply(registers.clone(), a, b, c);
        ip_val = registers[ip];
        ip_val += 1;
    }

    println!("p1 register 0 val: {}", registers[0]);

    ip_val = 0;
    registers = vec![0; 6];
    registers[0] = 1;
    for _ in 0..P2_RUN_AMT {
        // yeah, this code is duplicated. unfortunate, really
        let (op, a, b, c) = instructions[ip_val as usize];
        registers[ip] = ip_val;
        registers = op.apply(registers.clone(), a, b, c);
        ip_val = registers[ip];
        ip_val += 1;
    }

    let giant_num = *registers.iter().max().unwrap();
    let mut total = 0;
    for i in 1..=giant_num {
        if giant_num % i == 0 {
            total += i;
        }
    }

    println!("p2 register 0 val: {total}");
}
