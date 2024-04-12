use std::collections::HashSet;
use std::fs;

fn main() {
    let chances: Vec<_> = fs::read_to_string("../input/day1.txt")
        .unwrap()
        .split_whitespace()
        .map(|i| i.parse::<i32>().unwrap())
        .collect();

    let mut curr_freq = 0;
    let mut seen_freqs = HashSet::from([curr_freq]);
    let mut seen_twice = i32::MIN;
    'simulation:
    loop {
        for f in &chances {
            curr_freq += f;
            if seen_freqs.contains(&curr_freq) && seen_twice == i32::MIN {
                seen_twice = curr_freq;
                break 'simulation;
            }
            seen_freqs.insert(curr_freq);
        }
    }

    println!("final frequency: {}", chances.iter().sum::<i32>());
    println!("first frequency seen twice: {seen_twice}");
}
