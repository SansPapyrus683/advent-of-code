use std::fs;
use std::collections::HashMap;

fn main() {
    let mut blocks: Vec<u32> = fs::read_to_string("../input/day6.txt")
        .expect("bruh")
        .split_whitespace()
        .map(|i| i.parse::<u32>().unwrap())
        .collect();
    let len = blocks.len();

    let mut seen = HashMap::from([(blocks.clone(), 0)]);
    loop {
        let mut to_redist = (0, 0);
        for i in 0..blocks.len() {
            if blocks[i] > to_redist.1 {
                to_redist = (i, blocks[i]);
            }
        }

        blocks[to_redist.0] = 0;
        for i in 1..=to_redist.1 as usize {
            blocks[(to_redist.0 + i) % len] += 1;
        }

        if seen.contains_key(&blocks) {
            break;
        }
        seen.insert(blocks.clone(), seen.len());
    }

    println!("# of cycles before something's seen again: {}", seen.len());
    println!("loop size: {}", seen.len() - seen[&blocks]);
}
