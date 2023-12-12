use std::fs;
use std::collections::{HashMap, HashSet};
use regex::Regex;

fn even_weight(
    at: &String,
    supporting: &HashMap<String, (u32, Vec<String>)>
) -> (u32, Option<u32>) {
    let weight = supporting[at].0;
    if supporting[at].1.is_empty() {
        return (weight, None)
    }

    let mut branches: HashMap<u32, Vec<u32>> = HashMap::new();
    let mut branch_res = Vec::new();
    let mut total = weight;
    for s in &supporting[at].1 {
        let (b_weight, b_res) = even_weight(s, supporting);
        branches.entry(b_weight).or_default().push(supporting[s].0);
        branch_res.push(b_res);
        total += b_weight;
    }

    if let Some(changed) = branch_res.iter().find(|r| r.is_some()) {
        assert!(branches.len() <= 1);
        return (total, *changed);
    }
    match branches.len() {
        1 => (total, None),
        2 => {
            let weights: Vec<&u32> = branches.keys().collect();
            let first = branches[weights[0]].len();
            let second = branches[weights[1]].len();
            assert_ne!((first != 1), (second != 1));

            let bad = branches[weights[if first < second { 0 } else { 1 }]][0];
            let mut change = (weights[1] - weights[0]) as i32;
            change *= if first < second { 1 } else { -1 };
            ((total as i32 + change) as u32, Some((bad as i32 + change) as u32))
        },
        _ => panic!("this is bad, very bad")
    }
}

fn main() {
    let tower = fs::read_to_string("../input/day7.txt").expect("bruh");

    let prog_fmt = Regex::new(r"([a-z]+) \((\d+)\) -> ([a-z,\s]+)").unwrap();
    let prog_leaf_fmt = Regex::new(r"([a-z]+) \((\d+)\)").unwrap();

    let mut supporting = HashMap::new();
    for t in tower.lines() {
        if let Some(m) = prog_fmt.captures(t) {
            let s = m[3].split(",")
                .map(|t| t.trim().to_string())
                .collect::<Vec<String>>();
            supporting.insert(
                m[1].to_string(),
                (m[2].parse::<u32>().unwrap(), s)
            );
        } else if let Some(m) = prog_leaf_fmt.captures(t) {
            supporting.insert(m[1].to_string(),
                              (m[2].parse::<u32>().unwrap(), Vec::new())
            );
        }
    }

    let mut not_bottom = HashSet::new();
    for (_, (_, above)) in &supporting {
        not_bottom.extend(above.into_iter());
    }
    for t in supporting.keys() {
        if !not_bottom.contains(t) {
            println!("bottom of tower: {t}");
            let new_weight = even_weight(t, &supporting).1.unwrap();
            println!("adjusted program weight: {}", new_weight);
            break;
        }
    }
}
