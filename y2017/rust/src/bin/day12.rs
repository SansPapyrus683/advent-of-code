use std::collections::HashMap;
use std::fs;
use regex::Regex;

const MAIN: u32 = 0;

fn main() {
    let read =  fs::read_to_string("../input/day12.txt").expect("bruh");

    let pipe_fmt = Regex::new(r"(\d+) <-> ([\d\s,]+)").unwrap();

    let mut village = HashMap::new();
    for p in read.lines() {
        if let Some(m) = pipe_fmt.captures(p) {
            let start = m[1].parse::<u32>().unwrap();
            let connected: Vec<u32> = m[2]
                .split(',')
                .map(|p| p.trim().parse::<u32>().unwrap())
                .collect();
            village.insert(start, connected);
        }
    }

    let mut visited = vec![false; village.len()];
    let mut group_num = 0;
    for start in 0..village.len() as u32 {
        if visited[start as usize] {
            continue;
        }
        visited[start as usize] = true;
        let mut frontier = vec![start];
        let mut curr_visited = 0;
        while !frontier.is_empty() {
            let curr = frontier.pop().unwrap();
            for n in &village[&curr] {
                let n = *n;
                if !visited[n as usize] {
                    visited[n as usize] = true;
                    frontier.push(n);
                    curr_visited += 1;
                }
            }
        }

        if start == MAIN {
            println!("# of programs in group of {MAIN}: {curr_visited}");
        }
        group_num += 1;
    }

    println!("total # of groups: {group_num}");
}
