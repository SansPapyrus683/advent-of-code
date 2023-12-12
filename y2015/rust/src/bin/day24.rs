use std::fs;
use std::collections::HashSet;
use itertools::Itertools;

fn split_half(v: &Vec<i32>) -> bool {
    let mut poss = HashSet::from([0]);
    for i in v {
        let mut to_insert = HashSet::new();
        for p in &poss {
            to_insert.insert(p + i);
        }
        poss.extend(to_insert);
    }
    let total = v.iter().sum::<i32>();
    total % 2 == 0 && poss.contains(&(total / 2))
}

fn main() {
    let read = fs::read_to_string("input/day24.txt").expect("bruh");
    // assumes divisibility by 3 & 4- also assumes all elements are distinct
    let mut packages = Vec::new();
    for p in read.lines() {
        packages.push(p.parse::<i32>().unwrap());
    }


    let total_weight = packages.iter().sum::<i32>();
    let p1_weight = total_weight / 3;

    let mut found_min_len = false;
    let mut min_entanglement = i64::MAX;
    for sz1 in 0..=packages.len() {
        if found_min_len {
            break;
        }
        for group1 in packages.iter().combinations(sz1) {
            if group1.iter().copied().sum::<i32>() != p1_weight {
                continue;
            }

            let mut remaining = Vec::new();
            for p in &packages {
                if !group1.contains(&p) {
                    remaining.push(*p);
                }
            }

            if split_half(&remaining) {
                let mut prod = 1;
                for p in group1 {
                    prod *= *p as i64;
                }
                min_entanglement = min_entanglement.min(prod);
                found_min_len = true;
            }
        }
    }

    println!("min entanglement for 3 groups: {min_entanglement}");

    let p2_weight = total_weight / 4;
    let mut found_min_len = false;
    let mut min_entanglement = i64::MAX;
    for sz1 in 1..packages.len() {
        if found_min_len {
            break;
        }
        for group1 in packages.iter().combinations(sz1) {
            if group1.iter().copied().sum::<i32>() != p2_weight {
                continue;
            }

            let mut rem1 = Vec::new();
            for p in &packages {
                if !group1.contains(&p) {
                    rem1.push(*p);
                }
            }

            'check: for sz2 in 0..packages.len() - sz1 {
                for group2 in rem1.iter().combinations(sz2) {
                    if group2.iter().copied().sum::<i32>() != p2_weight {
                        continue;
                    }
                    let mut rem2 = Vec::new();
                    for p in &rem1 {
                        if !group2.contains(&p) {
                            rem2.push(*p);
                        }
                    }

                    if split_half(&rem2) {
                        let mut prod = 1;
                        for p in group1 {
                            prod *= *p as i64;
                        }
                        min_entanglement = min_entanglement.min(prod);
                        found_min_len = true;
                        break 'check;
                    }
                }
            }
        }
    }

    println!("min entanglement for 4 groups: {min_entanglement}");
}
