/// this takes really long to run, sorry

use std::collections::{HashMap, VecDeque};
use std::fs;
use regex::Regex;

fn next_state<'a>(scanners: &mut HashMap<&'a u32, (u32, bool)>,
              firewall: &'a HashMap<u32, u32>) {
    for l in firewall.keys() {
        let (mut pos, mut down) = scanners[l];
        if (pos == firewall[l] - 1) && down || (pos == 0 && !down) {
            down = !down;
        }
        pos = if down { pos + 1 } else { pos - 1 };
        scanners.insert(l, (pos, down));
    }
}

fn main() {
    let read = fs::read_to_string("input/day13.txt").expect("bruh");

    let layer_fmt = Regex::new(r"(\d+): (\d+)").unwrap();
    let mut firewall = HashMap::new();
    for l in read.lines() {
        if let Some(m) = layer_fmt.captures(l) {
            let layer = m[1].parse::<u32>().unwrap();
            let range = m[2].parse::<u32>().unwrap();
            if firewall.insert(layer, range).is_some() {
                panic!("what you can't have multiple scanners");
            }
        }
    }

    let walls: Vec<u32> = firewall.keys().map(|&l| l).collect();
    let mut scanners = HashMap::new();
    for l in &walls {
        scanners.insert(l, (0, true));
    }

    let mut stuff = VecDeque::new();
    for _ in 0..*walls.iter().max().unwrap() + 1 {
        stuff.push_back(scanners.clone());
        next_state(&mut scanners, &firewall);
    }

    let mut severity = 0;
    for (time, s) in stuff.iter().enumerate() {
        let time = &(time as u32);
        if let Some((0, _)) = s.get(time) {
            severity += time * firewall[time];
        }
    }
    println!("initial trip severity: {severity}");

    let mut delay = 0;
    loop {
        let mut caught = false;
        for (time, s) in stuff.iter().enumerate() {
            let time = &(time as u32);
            if let Some((0, _)) = s.get(time) {
                caught = true;
                break;
            }
        }

        if !caught {
            break;
        }

        stuff.pop_front();
        stuff.push_back(scanners.clone());
        next_state(&mut scanners, &firewall);
        delay += 1;
    }
    println!("min delay to not get caught: {delay}");
}
