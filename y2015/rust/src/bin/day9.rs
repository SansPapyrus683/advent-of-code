use std::fs;
use std::collections::{HashMap, HashSet};
use regex::Regex;
use itertools::Itertools;

fn main() {
    let dist_fmt = Regex::new(r"([a-z]+) to ([a-z]+) = (\d+)").unwrap();

    let read = fs::read_to_string("../input/day9.txt").expect("bruh");
    let mut adj: HashMap<String, HashMap<String, i32>> = HashMap::new();
    let mut cities = HashSet::new();
    for l in read.lines() {
        let lc = l.to_lowercase();
        if let Some(m) = dist_fmt.captures(&lc) {
            let (c1, c2) = (m[1].to_string(), m[2].to_string());
            let d: i32 = m[3].parse().unwrap();

            cities.insert(c1.clone());
            cities.insert(c2.clone());
            adj.entry(c1.clone()).or_default().insert(c2.clone(), d);
            adj.entry(c2).or_default().insert(c1, d);
        }
    }

    let mut min_dist = i32::MAX;
    let mut max_dist = i32::MIN;
    for order in cities.iter().permutations(cities.len()) {
        let start = order[0];
        let mut dist = 0;
        for i in 1..order.len() - 1 {
            dist += adj[order[i]][order[i + 1]];
        }
        dist += adj[*order.last().unwrap()][start];

        min_dist = min_dist.min(dist);
        max_dist = max_dist.max(dist);
    }

    println!("shortest path: {min_dist}");
    println!("longest path: {max_dist}");
}
