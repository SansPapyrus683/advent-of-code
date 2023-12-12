use std::fs;
use itertools::Itertools;

const EGGNOG: u32 = 150;

fn main() {
    let read = fs::read_to_string("../input/day17.txt").expect("bruh");
    let mut containers = Vec::new();
    for c in read.lines() {
        containers.push(c.parse::<u32>().unwrap());
    }

    let mut comb_num = 0;
    let mut min_comb_num = 0;
    let mut found_min = false;
    for sz in 1..=containers.len() {
        let mut this_comb_num = 0;
        for sub in containers.iter().combinations(sz) {
            if sub.iter().copied().sum::<u32>() == EGGNOG {
                comb_num += 1;
                this_comb_num += 1;
            }
        }
        
        if this_comb_num != 0 && !found_min {
            found_min = true;
            min_comb_num = this_comb_num;
        }
    }

    println!("total # of combinations: {comb_num}");
    println!("# of minimal combinations: {min_comb_num}");
}
